"""Graph traversal preserves real edges, multiple parents and disconnected nodes."""
import pytest
from streamlit.testing.v1 import AppTest
from app.core.context import AppContext
from app.features.learning_geometry.services.knowledge_graph import focus_graph, graph_dot
from app.features.learning_geometry.repositories.taxonomy import TaxonomyRepository
from tests.fakes import FakeIdentity, FakeAssessment

GRAPH = {
    'nodes': [{'id':key,'name':name} for key,name in
              [('square','Hình vuông'),('rectangle','Hình chữ nhật'),
               ('rhombus','Hình thoi'),('parallelogram','Hình bình hành'),
               ('isolated','Hình chưa liên kết')]],
    'edges': [{'id':str(i),'source':source,'target':target,'type':'IS_A'}
              for i,(source,target) in enumerate([
                  ('square','rectangle'),('square','rhombus'),
                  ('rectangle','parallelogram'),('rhombus','parallelogram')])],
}


class Content:
    def geometry_graph(self): return GRAPH


def context(): return AppContext(FakeIdentity(),Content(),FakeAssessment())
def empty_context():
    class Empty:
        def geometry_graph(self): return {'nodes':[],'edges':[]}
    return AppContext(FakeIdentity(),Empty(),FakeAssessment())


def test_multiple_parents_and_multihop_keep_original_edges_only():
    one = focus_graph(GRAPH,'square','parents',1)
    assert {node['id'] for node in one['nodes']} == {'square','rectangle','rhombus'}
    assert len(one['edges']) == 2
    two = focus_graph(GRAPH,'square','parents',2)
    assert len(two['nodes']) == 4 and len(two['edges']) == 4
    assert not any(edge['source']=='square' and edge['target']=='parallelogram' for edge in two['edges'])
    children = focus_graph(GRAPH,'parallelogram','children',2)
    assert children == two
    assert focus_graph(GRAPH,'isolated','both',8)['edges'] == []


def test_all_nodes_and_empty_dataset_are_preserved():
    assert focus_graph(GRAPH) == GRAPH
    assert focus_graph({'nodes':[],'edges':[]}) == {'nodes':[],'edges':[]}
    with pytest.raises(ValueError): focus_graph(GRAPH,'unknown')


def test_cycle_terminates_without_inventing_nodes():
    cyclic = dict(GRAPH,edges=GRAPH['edges']+[{'source':'parallelogram','target':'square','type':'IS_A'}])
    assert len(focus_graph(cyclic,'square','parents',8)['nodes']) == 4


def test_dot_escapes_database_names_and_ids():
    graph = {'nodes':[{'id':'x"; injected','name':'Tên "hình"\nxuống dòng'}],'edges':[]}
    dot = graph_dot(graph)
    assert '"x\\"; injected"' in dot
    assert 'Tên \\"hình\\"\\nxuống dòng' in dot


def test_database_failure_is_not_an_empty_mock_graph():
    class Broken:
        def read(self,*args,**kwargs): raise RuntimeError('Neo4j unavailable')
    with pytest.raises(RuntimeError,match='Neo4j unavailable'):
        TaxonomyRepository().geometry_graph(Broken())


def test_page_filters_diagram_and_counts_without_database():
    page=AppTest.from_string('''
from app.features.learning_geometry.tests.test_knowledge_graph import context
from app.features.learning_geometry.pages.knowledge_graph import render
render(context())
''').run()
    assert not page.exception
    assert [item.value for item in page.metric] == ['5','4']
    page.radio[0].set_value('Tập trung một hình').run()
    next(item for item in page.selectbox if item.label=='Hình cần khám phá').set_value('square').run()
    next(item for item in page.selectbox if item.label=='Hướng khám phá').set_value('Loại tổng quát hơn').run()
    page.slider[0].set_value(1).run()
    assert not page.exception
    assert [item.value for item in page.metric] == ['3','2']
    assert page.get('graphviz_chart')


def test_empty_graph_shows_explicit_empty_state():
    page=AppTest.from_string('''
from app.features.learning_geometry.tests.test_knowledge_graph import empty_context
from app.features.learning_geometry.pages.knowledge_graph import render
render(empty_context())
''').run()
    assert not page.exception
    assert any('Chưa có dữ liệu' in item.value for item in page.info)
    assert not page.get('graphviz_chart')
