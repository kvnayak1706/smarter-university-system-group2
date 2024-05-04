import unittest

from app.controllers.quizzes_controller import QuizzesController
from datetime import datetime

class QuizzesTest(unittest.TestCase):

    def setUp(self):
        # Run tests on non-production data
        self.ctrl = QuizzesController('quizzes_test.json')
        
    def test_expose_failure_01(self):
        # Create the timestamps
        avlDate = datetime(2024,10,20,5,00,00)
        dueDate = datetime(2024,10,25,5,00,00)

        # Add a quiz
        # Induce a crash by passing a non string type (ex: int) instead of string to the "title" argument
        # TypeError: unsupported operand type(s) for +: 'int' and 'str'
        # File name : quizzes_controller.py , Line no. : 63
        quiz_id = self.ctrl.add_quiz(1,"Some random text",avlDate,dueDate)
        
        # Gets the quiz id if application hadn't crashed
        q1 = self.ctrl.get_quiz_by_id(quiz_id)

        # Quiz text retrieved should be same as it was set while adding the quiz
        self.assertEquals("Some random text",q1.text)

    def test_expose_failure_02(self):
        # Create the timestamps
        avlDate = datetime(2019,10,25,5,00,00)
        dueDate = datetime(2018,10,25,5,00,00)

        # Add a quiz
        quiz_id = self.ctrl.add_quiz("quiz1","Some random text",avlDate,dueDate)
        
        # Corrupt the quizes attribute of the quiz_controller class to induce a crash
        self.ctrl.quizzes = None
        
        # Invoke remove_quiz() to remove the "quiz1" to trigger the crash
        # AttributeError: 'list' object has no attribute 'id'
        # File name: quizzes_controller.py , Line no.: 110
        self.ctrl.remove_quiz(quiz_id)

        # "quiz1" shouldnt exist as it would've been deleted if the program didn't crash
        self.assertIsNone(self.ctrl.get_quiz_by_id(quiz_id))

    def test_expose_failure_03(self):
        
        # Corrupt the quizes attribute of the quiz_controller class to induce a crash
        self.ctrl.quizzes = [1,2,3,5]

        # Try to add a new quiz to trigger a crash
        # AttributeError: 'int' object has no attribute 'to_json'
        # File name: quizzes_controller.py , Line no.: 54
        avlDate = datetime(2019,10,25,5,00,00)
        dueDate = datetime(2018,10,25,5,00,00)
        quiz_id = self.ctrl.add_quiz("quiz1","Some random text",avlDate,dueDate)

        # "quiz1" would have been successfully added if the program didn't crash
        self.assertIsNotNone(self.ctrl.get_quiz_by_id(quiz_id))

    
if __name__ == '__main__':
    unittest.main()