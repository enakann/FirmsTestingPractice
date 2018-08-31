>>> @patch.object(SomeClass, 'class_method')
... @patch.object(SomeClass, 'static_method')
... def test(mock1, mock2):
...     assert SomeClass.static_method is mock1
...     assert SomeClass.class_method is mock2
...     SomeClass.static_method('foo')
...     SomeClass.class_method('bar')
...     return mock1, mock2
...
>>> mock1, mock2 = test()
>>> mock1.assert_called_once_with('foo')
>>> mock2.assert_called_once_with('bar')

>>> from contextlib import nested
>>> with nested(
...         patch('package.module.ClassName1'),
...         patch('package.module.ClassName2')
...     ) as (MockClass1, MockClass2):
...     assert package.module.ClassName1 is MockClass1
...     assert package.module.ClassName2 is MockClass2
...