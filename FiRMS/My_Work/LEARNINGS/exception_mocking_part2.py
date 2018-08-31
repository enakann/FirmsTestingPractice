import Logging_my
from mock import patch
import unittest
def square_value(a):
   """
   Returns the square value of a.
   """
   try:
       out = a*a
   except TypeError:
       raise TypeError("Input should be a string:")

   return out

def square_value2(a):
   """
   Returns the square value of a.
   """
   log=Logging_my.Log().init_logger_singleton()
   out=None
   try:
       out = a*a
   except TypeError:
       log.warn("this should be a string")
       print("this should be string")
   return out



import unittest
class Test(unittest.TestCase):
   """
      The class inherits from unittest
      """
   def setUp(self):
       """
       This method is called before each test
       """
       self.false_int = "A"

   def tearDown(self):
       """
       This method is called after each test
       """
       pass
      #---
         ## TESTS
   def test_square_value(self):
       # assertRaises(excClass, callableObj) prototype
       self.assertRaises(TypeError, lambda:square_value(self.false_int))

   @patch('Logging_my.logging')
   def test_square_value2(self,mocklog):
       square_value2(self.false_int)
       mocklog.warn.assert_called_with("this should be a string")





   if __name__ == "__main__":
       unittest.main()