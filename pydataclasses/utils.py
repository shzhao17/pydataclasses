
import json

from functools import wraps
from collections import OrderedDict

import six

from pydataclasses import DataClass


def exception_quiet(exception_return=None):
    def _exception_quiet(func):
        @wraps(func)
        def _func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                assert ex
                return exception_return
        return _func
    return _exception_quiet


class JSONUtils(object):

    @classmethod
    def loads(cls, _json, *args, **kwargs):
        """
        :type _json: str
        :rtype: dict
        """
        return json.loads(_json, *args, **kwargs)

    @classmethod
    @exception_quiet()
    def loads_safe(cls, _json, *args, **kwargs):
        return cls.loads(_json, *args, **kwargs)

    @classmethod
    def dumps(cls, _dict, *args, **kwargs):
        """
        :type _dict: dict
        :rtype: str
        """
        return json.dumps(_dict, *args, **kwargs)

    @classmethod
    @exception_quiet()
    def dumps_safe(cls, _dict):
        return cls.dumps(_dict)


# noinspection PyProtectedMember
# pylint: disable=protected-access
class JSONData(DataClass):

    __utils__ = JSONUtils()

    def __init__(self, _origin=None, **_extras):

        if isinstance(_origin, six.string_types):
            _origin = self.__utils__.loads_safe(_origin)

        super(JSONData, self).__init__(_origin, **_extras)

    def as_dict(self, dict_class=OrderedDict, none_level=0):
        """
        :type dict_class: type
        :type none_level: int
        :rtype: dict
        """
        return self.__as_dict__(dict_class, none_level)

    def as_json(self, dict_class=OrderedDict, none_level=0):
        """
        :type dict_class: type
        :type none_level: int
        :rtype: str
        """
        return self.__utils__.dumps(self.as_dict(dict_class, none_level))
