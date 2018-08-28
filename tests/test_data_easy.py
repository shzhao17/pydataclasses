# -*- coding: utf-8 -*-

import unittest
from typing import List
from pydataclasses import DataClass


class TT(DataClass):

    attr = None


class ONCE(DataClass):

    data = None


class TWICE(ONCE):

    tear = TT                                                                        # type: TT
    tears = [TT]                                                                     # type: List[TT]

    def __init__(self, *args, **kwargs):

        super(TWICE, self).__init__(*args, **kwargs)

        self.pair = TWICE                                                            # type: TWICE
        self.pairs = [TWICE]                                                         # type: List[TWICE]


# noinspection PyProtectedMember
class TestDataEasy(unittest.TestCase):

    def test_data_easy(self):

        old_data = 'hello'
        new_data = 'world'
        old_dict = {'data': old_data}
        new_dict = {'data': new_data}

        # lazy and auto object creation on-the-fly
        twice = TWICE()
        assert twice.pairs[1].tear.attr is None
        twice.pairs[1].tear.attr = old_data
        assert old_data == twice.pairs[1].tear.attr

        # lazy loading of the dict input (default: enabled)
        twice = TWICE(old_dict)
        assert old_data == twice.data
        assert old_dict == twice.__as_dict__(dict, 0)

        # synchronous updates of the dict input (default: disabled)
        assert old_dict != new_dict
        twice = TWICE(old_dict, __sync__=True)
        twice.data = new_data
        assert old_dict == new_dict
        self.assertEqual(old_dict, new_dict)
