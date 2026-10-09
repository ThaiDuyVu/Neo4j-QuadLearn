"""Validate graph links and answer keys before importing demo fixtures."""
import copy
import json

import pytest
from scripts.demo_data import load_content


def test_demo_pack_covers_grades_and_has_real_explanations():
    data=load_content()
    for grade in (6,7,8,9):
        assert sum(x['grade']==grade for x in data['lessons'])==4
        assert sum(x['grade']==grade for x in data['questions'])==8
        assert sum(x['grade']==grade for x in data['essays'])==1
    assert all(len(x['content_vi'])>150 for x in data['lessons'])
    assert all(x['explanation_vi'] for x in data['questions'])


@pytest.mark.parametrize('fault',['cycle','missing_prerequisite','duplicate_option','ambiguous_answer'])
def test_invalid_demo_pack_is_rejected_before_writes(tmp_path,fault):
    data=copy.deepcopy(load_content())
    if fault=='cycle':
        data['lessons'][0]['prerequisites']=[data['lessons'][0]['id']]
    elif fault=='missing_prerequisite':
        data['lessons'][0]['prerequisites']=['lesson:missing']
    elif fault=='duplicate_option':
        data['questions'][1]['options'][0]['id']=data['questions'][0]['options'][0]['id']
    else:
        data['questions'][0]['options'][1]['correct']=True
    path=tmp_path/'bad.json'
    path.write_text(json.dumps(data),encoding='utf-8')
    with pytest.raises(ValueError):
        load_content(path)
