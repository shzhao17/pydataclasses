# -*- coding: utf-8 -*-

# pylint: disable=invalid-name
# pylint: disable=unused-import
# pylint: disable=line-too-long
# pylint: disable=too-many-lines

import copy
import random
import timeit
import unittest

from collections import OrderedDict

from typing import (
    Any,
    Dict,
    List,
    Text,
)

import six

from pydataclasses import DataClass


class Const(object):

    BOOL = True
    BOOL_NEW = not BOOL

    INT = 2 ** 64
    INT_NEW = 0

    FLOAT = 1e-12
    FLOAT_NEW = 1e+12

    ASCII = 'Hello World'
    ASCII_NEW = 'Heal The World'

    UTF8 = 'Hello World 你好世界'
    UTF8_NEW = 'Heal The World 治愈世界'

    UNICODE = u'Hello World 你好世界'
    UNICODE_NEW = u'Heal The World 治愈世界'

    DICT = {'__dict__': {UTF8: ASCII}}
    DICT_NEW = {ASCII_NEW: UTF8_NEW, UTF8_NEW: FLOAT_NEW}

    LIST = [DICT, [DICT, DICT], []]
    LIST_NEW = [INT_NEW, FLOAT_NEW, [ASCII_NEW, [UTF8_NEW, DICT_NEW]]]

    ORIGIN = {
        'none': None,
        'bool': BOOL,
        'int': INT,
        'ascii': ASCII,
        'utf8': UTF8,
        'unicode': UNICODE,
        'dict': DICT,
        'list': LIST,
        'fixed': DICT,
        'tear': {'str': ASCII},
        'tears': [{'str': UTF8}],
        'pair': {'ascii': ASCII, 'fixed': DICT},
        'pairs': [{'fixed': DICT}, {'utf8': UTF8, 'fixed': DICT}],
        '__class__': UTF8,
        '__dict__': {'str': ASCII},
        '__module__': [{'unicode': UNICODE, 'fixed': DICT}],
    }

    LEGEND = copy.deepcopy(ORIGIN)

    _data = LEGEND
    for _i in range(20):
        _data['pair'] = copy.deepcopy(ORIGIN)
        _data = _data['pair']


class TT(DataClass):

    str = None                                                                       # type: str

    _class_private = None                                                            # ignored

    def __init__(self, *args, **kwargs):

        super(TT, self).__init__(*args, **kwargs)

        self.pair = TWICE                                                            # type: TWICE
        self.pairs = [TWICE]                                                         # type: List[TWICE]

        self._instance_private = None                                                # ignored
        self._instance_property = None                                               # ignored

    @property
    def instance_property(self):                                                     # ignored
        return self._instance_property

    @instance_property.setter
    def instance_property(self, _value):                                             # ignored
        self._instance_property = _value

    @staticmethod
    def static_method():
        pass

    @staticmethod
    def _static_method():
        pass

    @staticmethod
    def __static_method__():
        pass

    @classmethod
    def class_method(cls):
        pass

    @classmethod
    def _class_method(cls):
        pass

    @classmethod
    def __class_method__(cls):
        pass

    def instance_method(self):
        pass

    def _instance_method(self):
        pass

    def __instance_method__(self):
        pass


class ONCE(DataClass):

    utf8 = str                                                                       # type: str
    unicode = six.text_type                                                          # type: Text
    dict = None                                                                      # type: Dict

    _class_private = None                                                            # ignored

    def __init__(self, *args, **kwargs):

        super(ONCE, self).__init__(*args, **kwargs)

        self.bool = bool                                                             # type: bool
        self.int = int                                                               # type: int
        self.ascii = str                                                             # type: str

        self.list = Any                                                              # type: List
        self.fixed = Const.DICT                                                      # type: Dict

        self._instance_private = None                                                # ignored
        self._instance_property = None                                               # ignored

    @property
    def instance_property(self):                                                     # ignored
        return self._instance_property

    @instance_property.setter
    def instance_property(self, _value):                                             # ignored
        self._instance_property = _value

    @staticmethod
    def static_method():
        pass

    @staticmethod
    def _static_method():
        pass

    @staticmethod
    def __static_method__():
        pass

    @classmethod
    def class_method(cls):
        pass

    @classmethod
    def _class_method(cls):
        pass

    @classmethod
    def __class_method__(cls):
        pass

    def instance_method(self):
        pass

    def _instance_method(self):
        pass

    def __instance_method__(self):
        pass


class TWICE(ONCE):

    class Nested(DataClass):

        __qualname__ = 'TWICE.Nested'                                                # required in Python 2

        class Nested(DataClass):

            __qualname__ = 'TWICE.Nested.Nested'                                     # required in Python 2

            none = None
            int = int                                                                # type: int
            tear = TT                                                                # type: TT
            tears = List[TT]                                                         # type: List[TT]

            _class_private = None                                                    # ignored

            def __init__(self, *args, **kwargs):

                super(TWICE.Nested.Nested, self).__init__(*args, **kwargs)

                self.pair = TWICE                                                    # type: TWICE
                self.pairs = [TWICE]                                                 # type: List[TWICE]

                self._instance_private = None                                        # ignored

    none = None
    float = float                                                                    # type: float
    tear = TT                                                                        # type: TT
    tears = [TT]                                                                     # type: List[TT]

    _class_private = None                                                            # ignored

    def __init__(self, *args, **kwargs):

        super(TWICE, self).__init__(*args, **kwargs)

        self.dict = Dict                                                             # type: Dict
        self.list = List                                                             # type: List

        self.nest = TWICE.Nested.Nested                                              # type: TWICE.Nested.Nested
        self.nests = [TWICE.Nested.Nested]                                           # type: List[TWICE.Nested.Nested]

        self.pair = TWICE                                                            # type: TWICE
        self.pairs = List[TWICE]                                                     # type: List[TWICE]

        self.value = self.__data__('__class__')                                      # type: str
        self.object = self.__data__('__dict__', TT)                                  # type: TT
        self.objects = self.__list__('__module__', TWICE)                            # type: List[TWICE]

        self._instance_private = None                                                # ignored
        self._instance_property = None                                               # ignored

    @property
    def instance_property(self):                                                     # ignored
        return self._instance_property

    @instance_property.setter
    def instance_property(self, _value):                                             # ignored
        self._instance_property = _value

    @staticmethod
    def static_method():
        return Const.UTF8

    @staticmethod
    def _static_method():
        pass

    @staticmethod
    def __static_method__():
        pass

    @classmethod
    def class_method(cls):
        return Const.UTF8

    @classmethod
    def _class_method(cls):
        pass

    @classmethod
    def __class_method__(cls):
        pass

    def instance_method(self):
        return self.class_method()

    def _instance_method(self):
        pass

    def __instance_method__(self):
        pass


# noinspection PyProtectedMember
# pylint: disable=protected-access
class TestDataHard(unittest.TestCase):

    __BASE__ = DataClass
    __TWICE__ = TWICE

    def test_data_init(self):

        twice = self.__TWICE__()
        self.assertFalse(twice)
        self.assertFalse(twice.bool)
        self.assertFalse(twice)  # leave it
        self.assertTrue(twice.fixed)
        self.assertFalse(twice)  # leave it
        self.assertIsNone(twice.none)
        self.assertFalse(twice)  # leave it
        self.assertFalse(twice.int)
        self.assertFalse(twice.ascii)
        self.assertFalse(twice.utf8)
        self.assertFalse(twice.unicode)
        self.assertFalse(twice.dict)
        self.assertFalse(twice.list)
        self.assertFalse(twice.tear)
        self.assertFalse(twice.tears)
        self.assertFalse(twice.pair)
        self.assertFalse(twice.pairs)
        self.assertFalse(twice.tear.str)
        self.assertFalse(twice.tear.pair)
        self.assertFalse(twice.tear.pairs)
        self.assertFalse(twice.tear.pairs[0])
        self.assertFalse(twice.tear.pair.tear)
        self.assertFalse(twice.tear.pairs[0].tear)
        self.assertFalse(twice.tear.pairs[0].tear.str)
        self.assertFalse(twice.tear.pairs[1].pairs[1].dict)
        self.assertFalse(twice.tear.pairs[1].pairs[1].list)

    def test_data_flat(self):

        origin = copy.deepcopy(Const.ORIGIN)
        twice = self.__TWICE__(origin, __lazy__=False)
        origin['int'] = Const.INT_NEW
        self.assertEqual(Const.INT, twice.int)
        self.assertEqual(Const.INT_NEW, origin['int'])
        twice.int = None
        self.assertEqual(None, twice.int)
        self.assertEqual(Const.INT_NEW, origin['int'])

    def test_data_lazy(self):  # by default

        origin = copy.deepcopy(Const.ORIGIN)
        twice = self.__TWICE__(origin)
        self.assertEqual(Const.INT, twice.int)  # loaded
        self.assertEqual(Const.INT, origin['int'])
        twice.int = None
        self.assertEqual(None, twice.int)
        self.assertEqual(Const.INT, origin['int'])

        origin = copy.deepcopy(Const.ORIGIN)
        twice = self.__TWICE__(origin, __lazy__=True)
        origin['int'] = None
        self.assertEqual(None, origin['int'])
        self.assertEqual(None, twice.int)
        self.assertEqual(None, origin['int'])

        origin = copy.deepcopy(Const.ORIGIN)
        origin_pair = origin['pair']  # type: Dict
        snapshot = origin_pair['ascii']
        twice = self.__TWICE__(origin)
        origin_pair.update({'ascii': Const.ASCII_NEW})
        self.assertEqual(Const.ASCII_NEW, origin_pair['ascii'])
        self.assertEqual(Const.ASCII_NEW, twice.pair.ascii)
        self.assertEqual(Const.ASCII_NEW, origin_pair['ascii'])
        self.assertNotEqual(Const.ASCII_NEW, snapshot)

        origin = copy.deepcopy(Const.ORIGIN)
        origin_pair = origin['pairs'][0]  # type: Dict
        snapshot = origin_pair.get('ascii', None)
        twice = self.__TWICE__(origin, __lazy__=True)
        origin_pair.update({'ascii': Const.ASCII_NEW})
        self.assertEqual(Const.ASCII_NEW, origin_pair.get('ascii', None))
        self.assertEqual(Const.ASCII_NEW, twice.pairs[0].ascii)
        self.assertEqual(Const.ASCII_NEW, origin_pair.get('ascii', None))
        self.assertNotEqual(Const.ASCII_NEW, snapshot)

    def test_data_sync(self):

        _TWICE_ = self.__TWICE__

        origin = copy.deepcopy(Const.ORIGIN)
        twice = _TWICE_(origin, __sync__=True)
        twice.pairs.append(_TWICE_(__sync__=True))
        with self.assertRaises(ValueError):
            twice.pairs.append(_TWICE_())  # missing __sync__

        origin = copy.deepcopy(Const.ORIGIN)
        twice = _TWICE_(origin, __sync__=True)
        snapshot = copy.deepcopy(origin)
        self.assertEqual(id(origin), id(twice.__origin__))
        self.assertEqual(snapshot, twice.__origin__)
        self.assertEqual(snapshot, twice.__as_dict__(dict, 1))
        self.assertEqual(snapshot, twice.__as_dict__(OrderedDict, 1))

        extra_attrs = {
            'not_in_twice': Const.UTF8_NEW,
            '_not_in_twice_': Const.UTF8_NEW,
        }
        origin = copy.deepcopy(Const.ORIGIN)
        origin.update(extra_attrs)
        origin['pairs'] = [extra_attrs.copy(), extra_attrs.copy()]
        twice = self.__TWICE__(origin, __sync__=True)
        twice.utf8 = Const.UTF8_NEW
        twice.pairs[1].utf8 = Const.UTF8_NEW
        snapshot = copy.deepcopy(origin)
        twice_dict = twice.__as_dict__(dict, 1)
        twice_dict.update(extra_attrs)
        twice_dict['pairs'][0].update(extra_attrs)
        twice_dict['pairs'][1].update(extra_attrs)
        self.assertEqual(id(origin), id(twice.__origin__))
        self.assertEqual(snapshot, twice.__origin__)
        self.assertEqual(snapshot, twice_dict)
        for _k, _v in six.iteritems(extra_attrs):
            self.assertEqual(origin[_k], _v)
            self.assertEqual(origin['pairs'][0][_k], _v)
            self.assertEqual(origin['pairs'][1][_k], _v)

        for _i in range(2):

            _safe_codes = """
            
                bool(twice.tear)
                bool(twice.tear.str)
                bool(twice.tears)
                bool(twice.tears[1])
                
                len(twice.tears)
                len(twice.pairs)
                len(twice.pairs[2:8])
                
                twice.bool = Const.BOOL_NEW
                twice.int = Const.INT_NEW
                twice.float = Const.FLOAT_NEW
                twice.ascii = Const.ASCII_NEW
                twice.utf8 = Const.UTF8_NEW
                twice.unicode = Const.UNICODE_NEW
                twice.fixed = Const.DICT_NEW
                
                twice.list = Const.LIST_NEW
                twice.list[0] = Const.UTF8_NEW
                twice.list.append(Const.UTF8_NEW)
                twice.dict = Const.DICT_NEW
                twice.dict['__dict__'] = Const.LIST_NEW
                twice.dict.pop('__dict__', None)
                
                twice.tear.str = Const.UTF8_NEW
                twice.tear.pair.tear.pair.objects[1].utf8 = Const.UTF8_NEW
                twice.tear.pairs[1].tear.pair.tears[1].pair.object.str = Const.UTF8_NEW
                
                twice.tears[0].str = Const.UTF8_NEW
                twice.tears[2].str = Const.UTF8_NEW
                twice.tears[3].pair.value = Const.UTF8_NEW
                twice.tears[3].pairs[1].tear.str = Const.UTF8_NEW
                twice.tears[5].pairs[1].object.pair.objects[1].tears[1].str = Const.UTF8_NEW
                
                twice.pair = None
                twice.pair.ascii = Const.ASCII_NEW
                twice.pair.tear.str = Const.UTF8_NEW
                
                twice.pairs = None
                twice.pairs[1].dict = Const.DICT_NEW
                twice.pairs[3].tears[2].pair.tear.pairs[1].object.str = Const.UTF8_NEW
                
                twice.pairs = [p for p in twice.pairs]
                twice.pairs = [_TWICE_(__sync__=True), _TWICE_(__sync__=True), _TWICE_(__sync__=True)]
                twice.pairs = twice.pairs + [_TWICE_(__sync__=True), _TWICE_(__sync__=True)]
                twice.pairs.append(_TWICE_({'int': Const.INT_NEW}, __sync__=True))
                twice.pairs.extend([_TWICE_(__sync__=True), _TWICE_(__sync__=True), _TWICE_(__sync__=True)])
                twice.pairs.insert(1, _TWICE_({'utf8': Const.UTF8_NEW}, __sync__=True))
                twice.pairs.reverse()
                twice.pairs[1].utf8 = Const.UTF8_NEW; twice.pairs.pop(0)
                twice.pairs[2].int = Const.INT_NEW; del twice.pairs[2]
                twice.pairs[3].ascii = Const.ASCII; twice.pairs.remove(twice.pairs[3])
                twice.pairs = []; twice.pairs[0].int = 1; twice.pairs[1].int = 2; twice.pairs[2].int = 0; twice.pairs.sort(key=lambda p: p.int)
                twice.pairs = []; twice.pairs[0].int = 1; twice.pairs[1].int = 2; twice.pairs[2].int = 0; twice.pairs = sorted(twice.pairs, key=lambda p: p.int)
                
                twice.value = Const.UTF8_NEW
                twice.object.pairs[1].dict = Const.DICT_NEW
                twice.objects[1].tears[1].str = Const.UTF8_NEW
                
                twice.pairs[:] = twice.pairs[:]
                twice.pairs[:2] = twice.pairs[:1]
                twice.pairs[2:] = twice.pairs[1:]
                twice.pairs[8:2] = twice.pairs[4:1]
                twice.pairs[2:8] = twice.pairs[1:4]
                
                twice.pairs.clear()
                twice.pairs[:] = []
                twice.pairs[:2] = []
                twice.pairs[2:] = []
                twice.pairs[8:2] = []
                twice.pairs[2:8] = []
                
                twice.pairs[1] = _TWICE_(__sync__=True)
                twice.pairs[:] = [_TWICE_(__sync__=True), _TWICE_(__sync__=True)]
                twice.pairs[:2] = [_TWICE_(__sync__=True), _TWICE_(__sync__=True), _TWICE_(__sync__=True)]
                twice.pairs[2:] = [_TWICE_(__sync__=True)]
                twice.pairs[8:2] = [_TWICE_(__sync__=True), _TWICE_(__sync__=True)]
                twice.pairs[2:8] = [_TWICE_(__sync__=True), _TWICE_(__sync__=True), _TWICE_(__sync__=True)]
                
                del twice.pairs[:]
                del twice.pairs[2:8]
                
            """.split('\n')

            origin = copy.deepcopy(Const.ORIGIN)
            history = copy.deepcopy(origin)
            history_id = id(origin)
            twice = self.__TWICE__(origin, __sync__=True)
            self.assertEqual(origin, twice.__as_dict__(dict, 1))
            self.assertEqual(origin, twice.__as_dict__(OrderedDict, 1))

            if _i:  # shuffled since twice
                random.shuffle(_safe_codes)

            for _safe_code in _safe_codes:

                _safe_code = _safe_code.strip()
                if not _safe_code:
                    continue

                _codes = _safe_code.split(';')
                for _code in _codes:
                    _code = _code.strip()
                    six.exec_(_code)

                snapshot = copy.deepcopy(origin)
                self.assertEqual(history_id, id(origin))
                self.assertEqual(history_id, id(twice.__origin__))
                self.assertEqual(snapshot, twice.__origin__)
                self.assertEqual(snapshot, twice.__as_dict__(dict, 1))

            self.assertEqual(snapshot, twice.__as_dict__(OrderedDict, 1))
            self.assertNotEqual(history, origin)

    def test_data_same(self):

        origin = copy.deepcopy(Const.ORIGIN)
        twice = self.__TWICE__(origin)

        self.assertTrue('none' in origin)
        self.assertIsNone(origin['none'])
        self.assertEqual(origin, twice.__as_dict__(dict, 1))
        self.assertEqual(origin, twice.__as_dict__(OrderedDict, 1))

        origin.pop('none', None)
        self.assertEqual(origin, twice.__as_dict__(dict, 0))
        self.assertEqual(origin, twice.__as_dict__(OrderedDict, 0))

    def test_data_method(self):

        origin = copy.deepcopy(Const.ORIGIN)
        snapshot = copy.deepcopy(origin)
        twice = self.__TWICE__(origin)
        twice.instance_property = Const.UTF8
        self.assertEqual(snapshot, twice.__as_dict__(dict, 1))
        self.assertEqual(snapshot, twice.__as_dict__(OrderedDict, 1))
        self.assertEqual(Const.UTF8, twice.static_method())
        self.assertEqual(Const.UTF8, twice.class_method())
        self.assertEqual(Const.UTF8, twice.instance_method())
        self.assertEqual(Const.UTF8, twice.instance_property)
        self.assertEqual(snapshot, twice.__as_dict__(dict, 1))
        self.assertEqual(snapshot, twice.__as_dict__(OrderedDict, 1))
        self.assertNotIn('instance_property', twice.__as_dict__(dict, 1))

    def test_data_timing(self):
        # pylint: disable=unnecessary-lambda

        legend = copy.deepcopy(Const.LEGEND)
        self.assertGreater(0.1, timeit.timeit(lambda: object(), number=50000))
        self.assertGreater(0.1, timeit.timeit(lambda: self.__TWICE__(), number=500))
        self.assertGreater(0.1, timeit.timeit(lambda: self.__TWICE__(legend), number=500))
        self.assertGreater(0.1, timeit.timeit(lambda: self.__TWICE__(legend, __lazy__=False), number=50))
        self.assertGreater(0.1, timeit.timeit(lambda: self.__TWICE__(legend, __lazy__=True), number=500))
        self.assertGreater(0.1, timeit.timeit(lambda: self.__TWICE__(legend, __sync__=True), number=500))

        origin = copy.deepcopy(Const.ORIGIN)
        twice = self.__TWICE__(origin)
        self.assertGreater(0.1, timeit.timeit(lambda: twice.__as_dict__(dict, 1), number=50))
        self.assertGreater(0.1, timeit.timeit(lambda: twice.__as_dict__(OrderedDict, 1), number=50))

    def test_data_default(self):

        class THRICE(self.__BASE__):

            def __init__(self, *args, **kwargs):

                super(THRICE, self).__init__(*args, **kwargs)

                self.default_int = self.__data__('__int__', default=Const.INT)
                self.default_ascii = self.__data__(default=Const.ASCII)
                self.default_utf8 = self.__data__(value_type=str, default=Const.UTF8)
                self.default_dict = self.__data__('__dict__', value_type=dict, default=Const.DICT)
                self.default_list = self.__data__('__list__', value_type=list, default=Const.LIST)

        thrice = THRICE()
        self.assertEqual(Const.INT, thrice.default_int)
        self.assertEqual(Const.ASCII, thrice.default_ascii)
        self.assertEqual(Const.UTF8, thrice.default_utf8)
        self.assertEqual(Const.DICT, thrice.default_dict)
        self.assertEqual(Const.LIST, thrice.default_list)

        thrice = THRICE(
            {
                'default_ascii': Const.ASCII_NEW,
            },
            default_utf8=Const.UTF8_NEW,
        )
        self.assertEqual(Const.INT, thrice.default_int)
        self.assertEqual(Const.ASCII_NEW, thrice.default_ascii)
        self.assertEqual(Const.UTF8_NEW, thrice.default_utf8)
        self.assertEqual(Const.DICT, thrice.default_dict)
        self.assertEqual(Const.LIST, thrice.default_list)

        thrice = THRICE(
            {
                '__int__': Const.INT_NEW,
                'default_ascii': Const.ASCII_NEW,
                'default_dict': Const.ASCII_NEW,
            },
            default_int=Const.UTF8_NEW,
            default_utf8=Const.UTF8_NEW,
            __dict__=Const.DICT_NEW,
            __list__=Const.LIST_NEW,
        )
        self.assertEqual(Const.INT_NEW, thrice.default_int)
        self.assertEqual(Const.ASCII_NEW, thrice.default_ascii)
        self.assertEqual(Const.UTF8_NEW, thrice.default_utf8)
        self.assertEqual(Const.DICT_NEW, thrice.default_dict)
        self.assertEqual(Const.LIST_NEW, thrice.default_list)

    def test_data_overload(self):

        once = ONCE()
        once.dict = Const.UTF8
        self.assertEqual(Const.UTF8, once.dict)

        twice = self.__TWICE__()
        with self.assertRaises(ValueError):
            twice.dict = Const.UTF8

    def test_data_assignment(self):

        twice = self.__TWICE__(
            {
                'bool': Const.BOOL,
                'ascii': Const.ASCII,
                'dict': Const.DICT,
                'list': Const.LIST,
            },
            int=Const.INT,
            ascii=Const.ASCII_NEW,
            list=Const.LIST_NEW,
            __nothing__=Const.UTF8,
        )
        twice.float = Const.FLOAT
        twice.utf8 = Const.UTF8
        self.assertTrue(twice)
        self.assertIsNone(twice.none)
        self.assertIsNone(twice.unicode)
        self.assertEqual(Const.BOOL, twice.bool)
        self.assertEqual(Const.INT, twice.int)
        self.assertEqual(Const.FLOAT, twice.float)
        self.assertEqual(Const.ASCII_NEW, twice.ascii)
        self.assertEqual(Const.UTF8, twice.utf8)
        self.assertEqual(Const.DICT, twice.dict)
        self.assertEqual(Const.LIST_NEW, twice.list)
        self.assertTrue(str, type(twice.ascii))
        self.assertTrue(str, type(twice.utf8))

    def test_data_attribute_chain(self):

        twice = self.__TWICE__()
        twice.tear.str = Const.UTF8
        twice.tear.pair.dict = Const.DICT
        twice.tear.pairs[1].list = Const.LIST
        self.assertTrue(twice.tear)
        self.assertEqual(Const.UTF8, twice.tear.str)
        self.assertEqual(Const.DICT, twice.tear.pair.dict)
        self.assertEqual(Const.LIST, twice.tear.pairs[1].list)

        twice = self.__TWICE__()
        self.assertFalse(twice.pair)
        self.assertFalse(twice.pair.pair)
        self.assertFalse(twice.pair.pair.tear)
        self.assertFalse(twice.pair.pair.tear.pair)
        self.assertFalse(twice.pair.pair.tear.pair.pairs[0])
        self.assertFalse(twice.pair.pair.tear.pair.pairs[0].tears[0])
        self.assertFalse(twice.pair.pair.tear.pair.pairs[0].tears[0].pairs[1])
        self.assertFalse(twice.pair.pair.tear.pair.pairs[0].tears[0].pairs[1].tears[1])
        tear = twice.pair.pair.tear.pair.pairs[0].tears[0].pairs[1].tears[1]
        tear.str = Const.UTF8
        self.assertEqual(Const.UTF8, tear.str)
        self.assertEqual(str, type(tear.str))
        self.assertTrue(twice.pair)
        self.assertTrue(twice.pair.pair)
        self.assertTrue(twice.pair.pair.tear)
        self.assertTrue(twice.pair.pair.tear.pair)
        self.assertTrue(twice.pair.pair.tear.pair.pairs[0])
        self.assertTrue(twice.pair.pair.tear.pair.pairs[0].tears[0])
        self.assertTrue(twice.pair.pair.tear.pair.pairs[0].tears[0].pairs[1])
        self.assertTrue(twice.pair.pair.tear.pair.pairs[0].tears[0].pairs[1].tears[1])

        for tear in [
            self.__TWICE__().tear.pair.tear,
            self.__TWICE__().pairs[0].tears[0].pairs[0].tear,
            self.__TWICE__().pair.tears[1].pairs[3].pairs[1].tears[4],
            self.__TWICE__().pair.pair.tear.pair.pairs[0].tears[0].pairs[1].tears[1],
        ]:
            tear = tear
            self.assertFalse(tear)
            tear.str = Const.UTF8
            self.assertTrue(tear)
            self.assertEqual(Const.UTF8, tear.str)

    def test_data_as_dict(self):

        twice = self.__TWICE__()
        twice.none = None
        twice.bool = Const.BOOL
        twice.int = Const.INT
        twice.float = Const.FLOAT
        twice.ascii = Const.ASCII
        twice.utf8 = Const.UTF8
        twice.unicode = Const.UNICODE
        twice.dict = Const.DICT
        twice.list = Const.LIST
        twice.tear.str = Const.ASCII
        twice.tears[0].str = Const.UTF8
        twice.nest.tear.str = Const.UTF8
        twice.nests[0].int = Const.INT
        twice.pair.ascii = Const.ASCII
        twice.pair.none = None
        twice.pairs[1].utf8 = Const.UTF8
        twice.value = Const.UTF8
        twice.object.str = Const.ASCII
        twice.objects[0].unicode = Const.UNICODE

        expected_with_none_levels = [dict()] * 3
        expected_with_none_levels[0] = {
            'bool': Const.BOOL,
            'int': Const.INT,
            'float': Const.FLOAT,
            'ascii': Const.ASCII,
            'utf8': Const.UTF8,
            'unicode': Const.UNICODE,
            'dict': Const.DICT,
            'list': Const.LIST,
            'fixed': Const.DICT,
            'tear': {'str': Const.ASCII},
            'tears': [{'str': Const.UTF8}],
            'nest': {'tear': {'str': Const.UTF8}},
            'nests': [{'int': Const.INT}],
            'pair': {'ascii': Const.ASCII, 'fixed': Const.DICT},
            'pairs': [{'fixed': Const.DICT}, {'utf8': Const.UTF8, 'fixed': Const.DICT}],
            '__class__': Const.UTF8,
            '__dict__': {'str': Const.ASCII},
            '__module__': [{'unicode': Const.UNICODE, 'fixed': Const.DICT}],
        }
        expected_with_none_levels[1] = copy.deepcopy(expected_with_none_levels[0])
        expected_with_none_levels[1].update({
            'none': None,
            'pair': {'none': None, 'ascii': Const.ASCII, 'fixed': Const.DICT},
        })
        expected_with_none_levels[2] = {
            'none': None,
            'bool': True,
            'int': Const.INT,
            'float': Const.FLOAT,
            'ascii': Const.ASCII,
            'utf8': Const.UTF8,
            'unicode': Const.UNICODE,
            'dict': Const.DICT,
            'list': Const.LIST,
            'fixed': Const.DICT,
            'tear': {
                'str': Const.ASCII,
                'pair': None,
                'pairs': [],
            },
            'tears': [
                {
                    'str': Const.UTF8,
                    'pair': None,
                    'pairs': [],
                }
            ],
            'nest': {
                'none': None,
                'int': None,
                'tear': {
                    'str': Const.UTF8,
                    'pair': None,
                    'pairs': [],
                },
                'tears': [],
                'pair': None,
                'pairs': [],
            },
            'nests': [
                {
                    'none': None,
                    'int': Const.INT,
                    'tear': None,
                    'tears': [],
                    'pair': None,
                    'pairs': [],
                }
            ],
            'pair': {
                'none': None,
                'bool': None,
                'int': None,
                'float': None,
                'ascii': Const.ASCII,
                'utf8': None,
                'unicode': None,
                'dict': None,
                'list': None,
                'fixed': Const.DICT,
                'tear': None,
                'tears': [],
                'nest': None,
                'nests': [],
                'pair': None,
                'pairs': [],
                '__class__': None,
                '__dict__': None,
                '__module__': [],
            },
            'pairs': [
                {
                    'none': None,
                    'bool': None,
                    'int': None,
                    'float': None,
                    'ascii': None,
                    'utf8': None,
                    'unicode': None,
                    'dict': None,
                    'list': None,
                    'fixed': Const.DICT,
                    'tear': None,
                    'tears': [],
                    'nest': None,
                    'nests': [],
                    'pair': None,
                    'pairs': [],
                    '__class__': None,
                    '__dict__': None,
                    '__module__': [],
                }, {
                    'none': None,
                    'bool': None,
                    'int': None,
                    'float': None,
                    'ascii': None,
                    'utf8': Const.UTF8,
                    'unicode': None,
                    'dict': None,
                    'list': None,
                    'fixed': Const.DICT,
                    'tear': None,
                    'tears': [],
                    'nest': None,
                    'nests': [],
                    'pair': None,
                    'pairs': [],
                    '__class__': None,
                    '__dict__': None,
                    '__module__': [],
                }
            ],
            '__class__': Const.UTF8,
            '__dict__': {
                'str': Const.ASCII,
                'pair': None,
                'pairs': [],
            },
            '__module__': [
                {
                    'none': None,
                    'bool': None,
                    'int': None,
                    'float': None,
                    'ascii': None,
                    'utf8': None,
                    'unicode': Const.UNICODE,
                    'dict': None,
                    'list': None,
                    'fixed': Const.DICT,
                    'tear': None,
                    'tears': [],
                    'nest': None,
                    'nests': [],
                    'pair': None,
                    'pairs': [],
                    '__class__': None,
                    '__dict__': None,
                    '__module__': [],
                }
            ],
        }
        for none_level, cloneable_none_levels in [
            (0, [0, 2]),
            (1, [0, 1, 2]),
            (2, [0, 2]),
        ]:
            for clone in [
                twice,
                copy.copy(twice),
                self.__TWICE__(twice),
                self.__TWICE__(copy.copy(twice)),
                self.__TWICE__(self.__TWICE__(twice)),
                self.__TWICE__(twice.__as_dict__(OrderedDict, none_level)),
                self.__TWICE__(**twice.__as_dict__(OrderedDict, none_level)),
                self.__TWICE__(twice, **twice.__as_dict__(OrderedDict, none_level)),
                self.__TWICE__(twice.__as_dict__(OrderedDict, none_level), **twice.__as_dict__(OrderedDict, none_level)),
                self.__TWICE__(twice.__as_dict__(OrderedDict, none_level), **twice.__as_dict__(OrderedDict, none_level)),
            ]:
                for cnl in cloneable_none_levels:
                    self.assertEqual(expected_with_none_levels[cnl], clone.__as_dict__(dict, cnl))

    def test_data_as_join(self):

        origin_1 = OrderedDict([
            ('none', None),
            ('bool', Const.BOOL),
            ('int', Const.INT),
            ('float', Const.FLOAT),
            ('ascii', Const.ASCII),
            ('utf8', Const.UTF8),
            ('list', [1, 2]),
            ('tear', {'str': Const.ASCII, 'key': Const.UNICODE}),
            ('tears', [{'str': Const.UTF8, 'key': Const.UNICODE}]),
        ])
        origin_2 = OrderedDict([
            ('none', None),
            ('bool', Const.BOOL),
            ('int', Const.INT),
            ('float', Const.FLOAT),
            ('ascii', Const.ASCII),
            ('utf8', Const.UTF8),
            ('list', [Const.UTF8, Const.ASCII]),
            ('tear', {'str': Const.ASCII, 'str1': Const.ASCII, 'str2': Const.ASCII}),
            ('tears', [{'str': Const.UTF8, 'str1': Const.UTF8}, {'str2': [{'str3': Const.UTF8}]}]),
        ])
        expected = OrderedDict([
            ('none', None),
            ('bool', Const.BOOL),
            ('int', Const.INT),
            ('float', Const.FLOAT),
            ('ascii', Const.ASCII),
            ('utf8', Const.UTF8),
            ('list', [1, 2]),
            ('list_xxx', [Const.UTF8, Const.ASCII]),
            ('tear', {'str': Const.ASCII, 'str1': Const.ASCII, 'str2': Const.ASCII, 'key': Const.UNICODE}),
            ('tears', [{'str': Const.UTF8, 'str1': Const.UTF8, 'str2': [{'str3': Const.UTF8}], 'key': Const.UNICODE}]),
        ])
        result = OrderedDict()
        result = self.__BASE__.__as_join__(result, origin_1)
        result = self.__BASE__.__as_join__(result, origin_2)
        self.assertEqual(expected, result)

    def test_data_as_self(self):

        _data_cls = self.__BASE__
        _data_name = _data_cls.__name__

        origin = OrderedDict([
            ('none', None),
            ('bool', Const.BOOL),
            ('int', Const.INT),
            ('float', Const.FLOAT),
            ('ascii', Const.ASCII),
            ('utf8', Const.UTF8),
            ('list', [1, 2]),
            ('tear', {'str': Const.ASCII}),
            ('tears', [{'str': Const.UTF8}]),
            ('_private_', {'str': Const.UTF8}),
            ('__burns__', [{'str': Const.UTF8}]),
            ('-0_3-1_6.utf8-new_', Const.UTF8_NEW),
        ])

        expected = """
            # pylint: disable=unused-import
            
            from typing import List

        
            class TWICETearItem({}):
            
                def __init__(self, *args, **kwargs):
            
                    super(TWICETearItem, self).__init__(*args, **kwargs)
                    
                    self.str = None                                                              # type: str
                    
        
            class TWICETearsItem({}):
            
                def __init__(self, *args, **kwargs):
            
                    super(TWICETearsItem, self).__init__(*args, **kwargs)
                    
                    self.str = None                                                              # type: str
                    
        
            class TWICEPrivateItem({}):
            
                def __init__(self, *args, **kwargs):
            
                    super(TWICEPrivateItem, self).__init__(*args, **kwargs)
                    
                    self.str = None                                                              # type: str
                    
        
            class TWICEBurnsItem({}):
            
                def __init__(self, *args, **kwargs):
            
                    super(TWICEBurnsItem, self).__init__(*args, **kwargs)
                    
                    self.str = None                                                              # type: str
                    
        
            class TWICE({}):
            
                def __init__(self, *args, **kwargs):
            
                    super(TWICE, self).__init__(*args, **kwargs)
                    
                    self.none = None                                                             
                    self.bool = None                                                             # type: bool
                    self.int = None                                                              # type: int
                    self.float = None                                                            # type: float
                    self.ascii = None                                                            # type: str
                    self.utf8 = None                                                             # type: str
                    self.list = None                                                             # type: List[int]
                    self.tear = TWICETearItem                                                    # type: TWICETearItem
                    self.tears = [TWICETearsItem]                                                # type: List[TWICETearsItem]
                    self.private = self.__data__('_private_', TWICEPrivateItem)                  # type: TWICEPrivateItem
                    self.burns = self.__list__('__burns__', TWICEBurnsItem)                      # type: List[TWICEBurnsItem]
                    self.utf8_new = self.__data__('-0_3-1_6.utf8-new_')                          # type: str

        """.format(_data_name, _data_name, _data_name, _data_name, _data_name)

        expected = expected.strip()
        result = _data_cls.__as_self__(origin, 'TWICE', _spaces_per_tab=4).strip()
        self.assertEqual(expected, result)
