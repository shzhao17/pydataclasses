Python Data Classes for Humans
==============================

Python Data Classes support Python 2 and 3 with many human-friendly features.

This project is under active development and has been tested in Python 2.7 and Python 3.4+.
It is not related to the ``dataclasses`` module introduced in Python 3.7.


Feature Support
---------------

Python Data Classes generally support

- untyped data, typed data, and typed data list
- arbitrary attribute names in the dictionary input
- no python attribute naming conflict or pollution
- lazy and auto object creation on-the-fly
- lazy loading of the dict input (default: enabled)
- synchronous updates of the dict input (default: disabled)


Getting Started
---------------

- Install the Python Data Classes

.. code-block::

    pip install pydataclasses


- Create the Python Data Classes

.. code-block:: python

    from pydataclasses import DataClass


    class TT(DataClass):

        attr = None


    class ONCE(DataClass):

        data = None


    class TWICE(ONCE):

        tear = TT
        tears = [TT]

        def __init__(self, *args, **kwargs):

            super(TWICE, self).__init__(*args, **kwargs)

            self.pair = TWICE
            self.pairs = [TWICE]


- Play with the Python Data Classes

.. code-block:: python

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


Best Practices
---------------

Please

- read and refer to ``pydataclasses.utils.JSONData`` as an example
- put a tailored subclass between ``pydataclasses`` and your project
- write (or copy from ``pydataclasses``) as many tests as possible for this subclass

.. code-block:: python

    from pydataclasses import DataClass


    class ProjectDataClass(DataClass):

        def as_dict(self, dict_class=OrderedDict):
            return self.__as_dict__(dict_class, 0)
