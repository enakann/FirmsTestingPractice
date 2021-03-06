"""All the patchers have start and stop methods. These make it simpler to do patching in setUp methods or where you want to do multiple patches without nesting decorators or with statements.

To use them call patch, patch.object or patch.dict as normal and keep a reference to the returned patcher object. You can then call start to put the patch in place and stop to undo it.

If you are using patch to create a mock for you then it will be returned by the call to patcher.start.
"""

 patcher = patch('package.module.ClassName')
 from package import module
 original = module.ClassName
 new_mock = patcher.start()
 assert module.ClassName is not original
 assert module.ClassName is new_mock
 patcher.stop()
 assert module.ClassName is original
 assert module.ClassName is not new_mock
"""A typical use case for this might be for doing multiple patches in the setUp method of a TestCase:"""

 class MyTest(TestCase):
    def setUp(self):
        self.patcher1 = patch('package.module.Class1')
        self.patcher2 = patch('package.module.Class2')
        self.MockClass1 = self.patcher1.start()
        self.MockClass2 = self.patcher2.start()
    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
    def test_something(self):
        assert package.module.Class1 is self.MockClass1
        assert package.module.Class2 is self.MockClass2
 MyTest('test_something').run()
"""Caution If you use this technique you must ensure that the patching is “undone” by calling stop. This can be fiddlier than you might think, because if an exception is raised in the setUp then tearDown is not called. unittest2 cleanup functions make this easier."""

 class MyTest(TestCase):
    def setUp(self):
        patcher = patch('package.module.Class')
        self.MockClass = patcher.start()
        self.addCleanup(patcher.stop)
    def test_something(self):
        assert package.module.Class is self.MockClass
 MyTest('test_something').run()
"""As an added bonus you no longer need to keep a reference to the patcher object."""

"""It is also possible to stop all patches which have been started by using patch.stopall."""

patch.stopall()
"""Stop all active patches. Only stops patches started with start"""