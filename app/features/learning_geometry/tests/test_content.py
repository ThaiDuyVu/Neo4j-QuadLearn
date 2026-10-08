import pytest
from app.features.learning_geometry.services.content import ContentService
from app.features.learning_geometry.services.geometry import rectangle

class FakeContent:
    def lessons(self, grade): return [grade]

def test_valid_grade():
    assert ContentService(FakeContent()).lessons(8) == [8]

@pytest.mark.parametrize("grade", [5, 10, None, "8"])
def test_invalid_grade(grade):
    with pytest.raises(ValueError): ContentService(FakeContent()).lessons(grade)

def test_rectangle_geometry_and_measurements():
    points, area, perimeter = rectangle(4, 3)
    assert points == [(0,0), (4,0), (4,3), (0,3)]
    assert area == 12 and perimeter == 14

@pytest.mark.parametrize("width,height", [(0,3), (3,-1)])
def test_degenerate_rectangle(width, height):
    with pytest.raises(ValueError): rectangle(width, height)
