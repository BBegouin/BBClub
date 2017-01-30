__author__ = 'Bertrand'
from unittest.mock import MagicMock
import facebook

def getAdapter():
    fb_mock = MagicMock(spec=facebook)
    grph = MagicMock()
    fb_mock.GraphAPI = grph
    get_obj_mock = MagicMock(return_value=3)
    fb_mock.GraphAPI.get_object = get_obj_mock
    return fb_mock



