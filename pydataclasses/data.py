
from __future__ import absolute_import

import inspect
import functools
import itertools

from collections import OrderedDict

import six
import six.moves as sm


class _DataNone(object):

    def __setattr__(self, _k, _v):
        raise AttributeError('nothing is wrong')

    def __getattribute__(self, _k):
        return self

    def __setitem__(self, _i, _v):
        pass

    def __getitem__(self, _i):
        return self

    def __call__(self, *args, **kwargs):
        return self

    # pylint: disable=non-iterator-returned
    def __iter__(self):
        yield self

    # noinspection PyMethodMayBeStatic
    def __next__(self):
        return self

    # noinspection PyMethodMayBeStatic
    def __bool__(self):
        return False

    __nonzero__ = __bool__


InitNone = _DataNone()
DataNone = _DataNone()


class DataList(list):

    def __init__(
        self,
        seq=(),
        __it_cls__=None,
        __origin__=None,
        __lazy__=True,
        __sync__=False,
        __link__=None,
    ):
        list.__init__(self, seq)

        self.__it_cls__ = __it_cls__ or DataCore
        self.__origin__ = __origin__
        self.__waited__ = __lazy__
        self.__synced__ = __sync__
        self.__relink__ = __link__

        if self.__len__():
            self.__auto_sync__(0, self.__len__())

    def __list__(self):
        return DataList(
            __it_cls__=self.__it_cls__,
            __lazy__=self.__waited__,
            __sync__=self.__synced__,
        )

    # ===== public =====

    def append(self, _item):

        if (
            self.__synced__ and
            isinstance(_item, DataCore) and
            not _item.__synced__
        ):
            raise ValueError('missing __sync__')

        _len = self.__len__()
        self.__setitem__(_len, _item)

    def extend(self, _iterable):
        for _item in _iterable:
            self.append(_item)

    def insert(self, _index, _item):
        _len = self.__len__()
        list.insert(self, _index, _item)
        self.__auto_sync__(_index, _len + 1)

    def sort(self, _cmp=None, key=None, reverse=False):
        if key is None and _cmp is not None:
            key = functools.cmp_to_key(_cmp)
        list.sort(self, key=key, reverse=reverse)
        self.__auto_sync__(0, self.__len__())

    def reverse(self):
        list.reverse(self)
        self.__origin__.reverse()

    def pop(self, _i=None):
        _len = self.__len__()
        self.__auto_sync__(_len - 1, _len)
        self.__origin__.pop(_i)
        return list.pop(self, _i)

    def clear(self):
        self.__setitem__(slice(0, self.__len__()), self.__list__())

    def remove(self, _v):
        list.remove(self, _v)
        self.__init_sync__()

    # ===== private =====

    def __iter__(self):
        for _i, _v in enumerate(list.__iter__(self)):
            _v = self.__getitem__(_i)
            yield _v

    def __setitem__(self, _i, _v):

        if isinstance(_i, slice):
            list.__setitem__(self, _i, _v)
            self.__init_sync__()
        else:
            self.__auto_sync__(_i, _i + 1)
            list.__setitem__(self, _i, _v)
            self.__auto_sync__(_i, _i + 1)

    def __getitem__(self, _i):

        if isinstance(_i, slice):
            _start, _outer = _i.start, _i.stop
            _start = 0 if _start is None else _start
            _outer = 2 ** 63 - 1 if _outer is None else _outer
            _outer = min(_outer, self.__len__())
            _v = self.__list__()
            for _oi in sm.range(_start, _outer):
                _ov = list.__getitem__(self, _oi)
                _ov = self.__init_item__(_oi, _ov)
                self.__auto_sync__(_oi, _oi + 1)
                _v.__setitem__(_oi, _ov)
                _ov = _v.__getitem__(_oi)
                _v.append(_ov)
        else:
            self.__auto_sync__(_i, _i + 1)
            _v = list.__getitem__(self, _i)
            _v = self.__init_item__(_i, _v)
            self.__auto_sync__(_i, _i + 1)

        return _v

    def __delitem__(self, _i):
        if isinstance(_i, slice):
            self.__setitem__(_i, [])
        else:
            self.pop(_i)

    def __delslice__(self, _i, _j):
        self.__setitem__(slice(_i, _j), [])

    def __setslice__(self, _i, _j, _iterator):
        self.__setitem__(slice(_i, _j), _iterator)

    def __getslice__(self, _i, _j):
        return self.__getitem__(slice(_i, _j))

    def __iadd__(self, _iterable):
        raise NotImplementedError

    def __imul__(self, y):
        raise NotImplementedError

    # ===== item, sync =====

    def __init_item__(self, _i, _v):

        if _v is not DataNone:
            return _v

        _item_cls = self.__it_cls__

        if (
            inspect.isclass(_item_cls) and
            issubclass(_item_cls, DataCore)
        ):
            if self.__synced__:
                _v_origin = _item_cls().__as_dict__(dict, 1)
                _v = _item_cls(_v_origin, __sync__=True)
            elif self.__waited__:
                _v = _item_cls(__lazy__=True)
            else:
                _v = _item_cls()
        else:
            _v = _item_cls()

        list.__setitem__(self, _i, _v)
        return _v

    def __init_sync__(self):

        _len = self.__len__()
        del self.__origin__[_len:]
        self.__auto_sync__(0, _len)

    def __auto_sync__(self, _start, _outer):

        _len = self.__len__()
        _more = max(0, _outer - _len)
        list.extend(self, [DataNone] * _more)

        if not self.__synced__:
            return

        _origin = self.__origin__

        if (
            _origin is DataNone or
            _origin is None
        ):
            _origin = self.__origin__ = []

        if self.__relink__:
            self.__relink__(self.__origin__)

        _len_o = len(_origin)
        _more_o = max(0, _outer - _len_o)
        _origin.extend([None] * _more_o)

        _start = max(0, min(_start, _len, _len_o))

        _item_cls = self.__it_cls__
        _is_class = inspect.isclass(_item_cls)
        _is_data = _is_class and issubclass(_item_cls, DataCore)

        for _i in sm.range(_start, _outer):

            _obj = list.__getitem__(self, _i)
            _obj = self.__init_item__(_i, _obj)
            _origin[_i] = (
                _obj.__origin__ if _is_data and _obj is not DataNone else
                _obj if _obj is not DataNone else
                _item_cls() if _is_class else
                None
            )


class DataAttr(object):

    __slots__ = [
        'key',
        'name',
        'value',
        'value_type',
    ]

    def __init__(self, key=None, name=None, value=None, value_type=None):
        """
        :param  key: internal attribute name for python
        :param name: external attribute name for input and output
        :param value: python attribute value
        :param value_type: python attribute value type (e.g., class)
        """
        self.key = key
        self.name = name
        self.value = value
        self.value_type = value_type

    def typed(self):
        return self.value_type is not DataNone


class DataMeta(type):

    def __new__(mcs, name, bases, attrs):
        _class = type.__new__(mcs, name, bases, attrs)
        _class.__fields__ = OrderedDict()
        _class.__ported__ = False
        return _class

    # noinspection PyProtectedMember
    # pylint: disable=protected-access
    def __call__(cls, *args, **kwargs):

        _instance = type.__call__(cls, *args, **kwargs)

        _class = _instance.__class__
        _class.__ported__ = True
        _fields = _class.__fields__
        _instance.__uninit__ = list(six.iterkeys(_fields))
        _instance.__booted__ = True

        if (
            not _instance.__waited__ and
            _instance.__origin__
        ):
            for _k in six.iterkeys(_fields):
                getattr(_instance, _k)

        _instance.__origin__ = _instance.__slot_1__
        _instance.__waited__ = _instance.__slot_2__
        _instance.__synced__ = _instance.__slot_3__

        delattr(_instance, '__slot_1__')
        delattr(_instance, '__slot_2__')
        delattr(_instance, '__slot_3__')

        if (
            _instance.__synced__ and
            _instance.__origin__ is not None
        ):
            for _k in six.iterkeys(_fields):
                if _instance.__is_fixed__(_k):
                    _instance.__origin__[_k] = _fields[_k].value

        return _instance


class DataCore(six.with_metaclass(DataMeta, object)):

    def __init__(self, _origin=None, **_extras):

        if isinstance(_origin, DataCore):
            _origin = _origin.__as_dict__(dict, 1)

        _extras = _extras or dict()
        _waited = _extras.pop('__lazy__', True)
        _synced = _extras.pop('__sync__', False)
        _relink = _extras.pop('__link__', None)

        if _synced:
            _waited = True
            if _origin is None:
                _origin = dict()

        if _extras:
            _origin = _origin or dict()
            _origin.update(_extras)

        self.__slot_1__ = _origin
        self.__slot_2__ = _waited
        self.__slot_3__ = _synced

        self.__origin__ = _origin
        if _waited:
            self.__origin__ = None

        self.__waited__ = False
        self.__synced__ = False
        self.__relink__ = _relink

    def __new__(cls, *_args, **_kwargs):

        _instance = object.__new__(cls)
        _instance.__booted__ = False
        _instance.__uninit__ = []
        _instance.__locked__ = False

        _class = _instance.__class__

        if not _class.__ported__:

            for _cls in list(_class.__bases__) + [_class]:
                for _k, _v in itertools.chain(
                    six.iteritems(_cls.__dict__),
                    six.iteritems(_cls.__dict__.get('__annotations__', {})),
                ):
                    if (
                        not _k.startswith('_') and
                        _instance.__is_property__(_k, _v)
                    ):
                        setattr(_instance, _k, _v)

        return _instance

    def __setattr__(self, _k, _v):

        if not _k.startswith('_'):

            _cls = self.__class__

            if not _cls.__ported__:
                if self.__is_property__(_k, _v):
                    self.__init_field__(_k, _v)

            if not self.__booted__:
                _v = InitNone

            elif _k in _cls.__fields__:

                _v = self.__type_value__(_k, _v)

                if (
                    self.__synced__ and
                    _k not in self.__uninit__
                ):
                    _is_data = isinstance(_v, (DataCore, DataList))
                    _k_in_origin = _k in self.__origin__

                    _ov = (
                        _v if not _is_data else
                        _v.__origin__
                    )
                    if (
                        _k_in_origin or
                        _ov or
                        _ov in (0, False)
                    ) and not (
                        _is_data and
                        not _v and
                        not _k_in_origin
                    ):
                        self.__link_value__(_k, _ov)

        object.__setattr__(self, _k, _v)

    def __getattribute__(self, _k):

        if (
            not _k.startswith('_') and
            _k in self.__class__.__fields__
        ):
            _v = self.__real_value__(_k)
            _v = self.__view_value__(_v)
            return _v

        return object.__getattribute__(self, _k)

    # ===== field, value, type =====

    def __init_field__(self, _k, _v):

        _fields = self.__class__.__fields__

        if (
            self.__is_any__(_v) or
            self.__is_data__(_v) or
            self.__is_list__(_v)
        ):
            _fields[_k] = DataAttr(_k, _k, DataNone, _v)

        elif isinstance(_v, DataAttr):
            _name = _v.name
            _name = _k if _name is None else _name
            _fields[_k] = DataAttr(_k, _name, _v.value, _v.value_type)

        else:  # preset value, untyped
            _fields[_k] = DataAttr(_k, _k, _v, DataNone)

    def __init_value__(self, _k):

        self.__locked__ = True

        _v = self.__by_origin__(_k)
        setattr(self, _k, _v)

        self.__locked__ = False

    def __type_value__(self, _k, _v):

        _vt = self.__class__.__fields__[_k].value_type

        if self.__is_fixed__(_k):

            pass

        elif self.__is_data__(_vt):

            _vt = self.__data_type__(_vt)
            _v = self.__load_value__(_vt, _v)
            if (
                inspect.isclass(_vt) and
                issubclass(_vt, DataCore)
            ):
                _relink = functools.partial(self.__link_value__, _k)
                _v.__relink__ = _relink

        elif self.__is_list__(_vt):

            _v = _v or []
            _item_type = self.__item_type__(_vt)
            _item_type = self.__data_type__(_item_type)
            _items = [self.__load_value__(_item_type, _item) for _item in _v]
            _relink = functools.partial(self.__link_value__, _k)
            _v = DataList(
                _items,
                __it_cls__=_item_type,
                __origin__=_v,
                __lazy__=self.__waited__,
                __sync__=self.__synced__,
                __link__=_relink,
            )

        elif _v is not DataNone and not self.__is_any__(_vt):

            _err = 'invalid value {} for attribute {} with type {}'.format(_v, _k, _vt)
            raise AttributeError(_err)

        if (
            self.__uninit__ and
            _k in self.__uninit__
        ):
            self.__uninit__.remove(_k)

        return _v

    def __load_value__(self, _vt, _v):

        _vv = None if _v is None or _v is DataNone else _v

        if not (
            inspect.isclass(_vt) and
            issubclass(_vt, DataCore)
        ):
            return (
                _v if _v is DataNone else
                None if _vv is None else
                _vt(_vv)
            )

        if self.__synced__:
            _new = _vt(_vv, __sync__=True)
        elif self.__waited__:
            _new = _vt(_vv, __lazy__=True)
        else:
            _new = _vt(_vv)

        return _new

    def __link_value__(self, _k, _v):

        if not self.__synced__:
            return

        if _v is None:
            return

        if self.__origin__ is None:
            self.__origin__ = dict()

        if self.__relink__:
            self.__relink__(self.__origin__)

        _cls = self.__class__
        _name = _cls.__fields__[_k].name
        self.__origin__[_name] = _v

    def __real_value__(self, _k):

        try:
            if (
                not self.__locked__ and
                self.__booted__ and
                self.__uninit__ and
                _k in self.__uninit__
            ):
                self.__init_value__(_k)

        except AttributeError:
            pass

        return object.__getattribute__(self, _k)

    @classmethod
    def __view_value__(cls, _v):
        return _v if _v is not DataNone else None

    # ===== object, objects =====

    @classmethod
    def __item_type__(cls, _vt):
        return _vt[0]

    @classmethod
    def __data_type__(cls, _vt):
        return _vt

    @classmethod
    def __data__(cls, name=None, value_type=None, default=DataNone):
        return DataAttr(None, name, default, value_type)

    @classmethod
    def __list__(cls, name=None, value_type=None):
        return DataAttr(None, name, DataNone, [value_type])

    @classmethod
    def __is_any__(cls, _vt):  # any value
        return _vt is None

    @classmethod
    def __is_data__(cls, _vt):
        return inspect.isclass(_vt)

    @classmethod
    def __is_list__(cls, _vt):
        return isinstance(_vt, list) and _vt and inspect.isclass(_vt[0])

    @classmethod
    def __is_property__(cls, _k, _v):

        qualified_name = getattr(_v, '__qualname__', '')

        return not (
            inspect.isroutine(_v) or           # any function or method
            isinstance(_v, property) or        # any functional property
            (                                  # any nested class with __qualname__
                _k == getattr(_v, '__name__', None) and
                inspect.isclass(_v) and
                inspect.getmodule(cls) == inspect.getmodule(_v) and (
                    qualified_name.startswith(cls.__name__) or
                    ('.' + cls.__name__ + '.') in qualified_name
                )
            )
        )

    @classmethod
    def __is_fixed__(cls, _k):

        if _k not in cls.__fields__:
            return False

        _field = cls.__fields__[_k]  # type: DataAttr
        return not _field.typed()

    @classmethod
    def __is_assigned__(cls, _k, _v):

        if cls.__is_fixed__(_k):
            _field = cls.__fields__[_k]
            return _v != _field.value

        return bool(_v)

    @classmethod
    def __is_data_none__(cls, _v, _none_level):
        return 0 <= _none_level <= 1 and (
            _v is DataNone or
            (_v is None and _none_level == 0) or
            (isinstance(_v, DataCore) and not _v)
        )

    # ===== origin =====

    def __by_origin__(self, _k):

        _field = self.__class__.__fields__[_k]  # type: DataAttr
        _v = _field.value

        if not _field.typed():
            return _v

        _origin = self.__origin__
        _name = _field.name

        if _origin is None:
            return _v
        elif isinstance(_origin, dict):
            return _origin.get(_name, _v)
        return getattr(_origin, _name, _v)

    # ===== bool =====

    # noinspection PyMethodMayBeStatic
    def __bool__(self):

        _cls = self.__class__

        if not _cls.__ported__ or not self.__booted__:
            return False

        if self.__origin__:
            for _k in self.__origin__:
                _v = self.__origin__[_k]
                if self.__is_assigned__(_k, _v):
                    return True

        for _k in _cls.__fields__:
            if _k in self.__uninit__:
                continue
            _v = getattr(self, _k, None)
            if self.__is_assigned__(_k, _v):
                return True

        return False

    __nonzero__ = __bool__

    # ===== boilerplate =====

    def __copy__(self):
        return self.__class__(self)

    def __deepcopy__(self, memo):
        return self.__copy__()

    def __eq__(self, _obj):
        """
        :type _obj: DataCore
        :rtype: bool
        """
        _this_dict = self.__as_dict__(OrderedDict, 1)
        _that_dict = _obj.__as_dict__(OrderedDict, 1)
        return _this_dict == _that_dict

    def __ne__(self, _obj):
        return not self.__eq__(_obj)

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return '{}'.format(self.__as_dict__(OrderedDict, 1))

    __unicode__ = __str__

    # ===== dict =====

    def __as_none__(self, _k, _v, _none_level):

        if bool(_v):
            return _v

        if isinstance(_v, DataCore):

            if self.__synced__ and _k in self.__origin__:
                _v = _v.__origin__
            if not _v:
                _v = DataNone

        elif isinstance(_v, DataList):

            _v = DataNone if (
                0 <= _none_level <= 1 and not (
                    self.__origin__ and
                    self.__synced__ and
                    _k in self.__origin__
                )
            ) else []

        return _v

    def __as_data__(self, _dict_cls, _v, _none_level):

        if isinstance(_v, DataCore):
            return _v.__as_dict__(_dict_cls, _none_level)

        elif isinstance(_v, list):
            return [self.__as_data__(_dict_cls, _d, _none_level) for _d in _v]

        return _v

    def __as_dict__(self, _dict_class, _none_level):
        """
        :param _dict_class: dict class, dict or OrderedDict
        :param _none_level: 0 (no None at all), 1 (only initialized None), 2 (all fields)
        :type _dict_class: type
        :type _none_level: int
        :rtype: dict or OrderedDict
        """
        _dict = _dict_class()
        _fields = self.__class__.__fields__

        for _k, _field in six.iteritems(_fields):

            _v = self.__real_value__(_k)
            _v = self.__as_none__(_k, _v, _none_level)
            _v = self.__as_data__(_dict_class, _v, _none_level)

            if not self.__is_data_none__(_v, _none_level):
                _n = _field.name
                _dict[_n] = self.__view_value__(_v)

        return _dict

    # ===== self =====

    @classmethod
    def __as_join__(cls, _old, _new):
        """
        :type _old: dict
        :type _new: dict
        :rtype: dict
        """
        _dict = OrderedDict()
        _set = set()
        _keys = list(_old.keys()) + list(_new.keys())
        _keys = [_x for _x in _keys if not (_x in _set or _set.add(_x))]

        for _k in _keys:

            if _k not in _old:
                _dict[_k] = _new[_k]
                continue

            _dv = _dict[_k] = _old[_k]

            if _k not in _new:
                continue

            _nv = _new[_k]

            if (
                not isinstance(_nv, type(_dv)) and
                not isinstance(_dv, type(_nv))
            ) or (
                _dv and
                _nv and
                isinstance(_dv, (list, tuple)) and
                isinstance(_nv, (list, tuple)) and
                not isinstance(_dv[0], type(_nv[0])) and
                not isinstance(_nv[0], type(_dv[0]))
            ):
                _k = '{}_xxx'.format(_k)
                _dict[_k] = _nv
                continue

            if isinstance(_nv, dict):
                _nv = cls.__as_join__(_dv, _nv)
                _dict[_k] = _nv
                continue

            if isinstance(_nv, (list, tuple)) and _nv:

                _nv_item = _nv[0]
                if isinstance(_nv_item, dict):
                    _dv_item = _dv[0] if _dv else {}
                    for _nit in [_dv_item] + _nv[1:]:
                        _nv_item = cls.__as_join__(_nv_item, _nit)
                    _dict[_k] = [_nv_item]

        return _dict

    @classmethod
    def __as_self__(cls, _dict, _dict_name='Object', _spaces_per_tab=None, _depth=0):
        """
        :type _dict: dict
        :type _dict_name: str
        :type _spaces_per_tab: int
        :type _depth: int
        :rtype: str
        """
        def __type_name__(_v_):
            if isinstance(_v_, six.string_types):
                return 'str'
            elif (
                not isinstance(_v_, bool) and
                isinstance(_v_, six.integer_types)
            ):
                return 'int'
            return type(_v_).__name__

        _self = """
            # pylint: disable=unused-import
            
            from typing import List

        """ if not _depth else ''

        _attrs = ''

        for _k, _v in six.iteritems(_dict):

            _ok = _k
            _k = _k.replace('.', '_').replace('-', '_')

            while True:
                _tk = _k
                _k = _k.strip('_').lstrip('0123456789')
                if _tk == _k:
                    break

            _def = (
                'self.{} = {}'.format(_k, None) if _k == _ok else
                'self.{} = self.__data__(\'{}\')'.format(_k, _ok)
            )
            _type_hint = __type_name__(_v)

            if isinstance(_v, dict):

                _item_name = _dict_name
                _item_name += ''.join(x.capitalize() or '_' for x in _k.split('_'))
                _item_name += 'Item'
                _type_hint = _item_name
                _self += cls.__as_self__(_v, _item_name, _spaces_per_tab, _depth + 1)

                if _k == _ok:
                    _def = 'self.{} = {}'.format(_k, _type_hint)
                else:
                    _def = 'self.{} = self.__data__(\'{}\', {})'.format(_k, _ok, _type_hint)

            elif isinstance(_v, list):

                if not _v:
                    _item_type = None
                    _type_hint = 'List'
                elif isinstance(_v[0], dict):
                    _item_name = _dict_name
                    _item_name += ''.join(x.capitalize() or '_' for x in _k.split('_'))
                    _item_name += 'Item'
                    _item_type = '{}'.format(_item_name)
                    _type_hint = 'List[{}]'.format(_item_name)
                    _self += cls.__as_self__(_v[0], _item_name, _spaces_per_tab, _depth + 1)
                else:
                    _item_name = __type_name__(_v[0])
                    _item_type = None
                    _type_hint = 'List' if _v[0] is None else 'List[{}]'.format(_item_name)

                if _k == _ok and _item_type is None:
                    _def = 'self.{} = None'.format(_k)
                elif _k == _ok:
                    _def = 'self.{} = [{}]'.format(_k, _item_type)
                elif _item_type is None:
                    _def = 'self.{} = self.__list__(\'{}\')'.format(_k, _ok)
                else:
                    _def = 'self.{} = self.__list__(\'{}\', {})'.format(_k, _ok, _item_type)

            _type = '' if _v is None else '# type: {}'.format(_type_hint)
            _attr = """{:<77}{}
                    """.format(_def, _type)
            _attrs += _attr

        _attrs = _attrs and """
                    {}""".format(_attrs)

        _self += """
            class {}({}):
            
                def __init__(self, *args, **kwargs):
            
                    super({}, self).__init__(*args, **kwargs)
                    {}
        """.format(_dict_name, cls.__name__, _dict_name, _attrs)

        _self = _self.replace('\t' * 3, '')

        if _spaces_per_tab:
            _self = _self.replace('\t', ' ' * _spaces_per_tab)

        return _self


DataClass = DataCore
