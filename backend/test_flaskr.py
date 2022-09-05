import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from settings import DB_NAME_TEST, DB_USER, DB_PASSWORD, DB_HOST


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME_TEST
        self.database_path =\
            "postgres://{}:{}@{}/{}"\
            .format(DB_USER, DB_PASSWORD, DB_HOST, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_on_deletion_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'requested resource not found')

    def test_deletion_if_question_exist(self):
        res = self.client().delete('/questions/4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'question successfully deleted')

    def test_create_new_question(self):
        new_question = {
            'question': 'Which country is known as the Horn of Africa?',
            'answer': 'Ethiopia',
            'category': 3,
            'difficulty': 3
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'question successfully created')

    def test_422_if_question_creation_fails(self):
        new_question = {
            'question': 'Which country is known as the Horn of Africa?',
            'answer': 'Ethiopia',
            'difficulty': 3
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_405_if_question_creation_not_allowed(self):
        new_question = {
            'question': 'Which country is known as the Horn of Africa?',
            'answer': 'Ethiopia',
            'category': 3,
            'difficulty': 3
        }
        res = self.client().post('/questions/5', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_question_search_with_results(self):
        res =\
            self.client().post('/questions/search', json={'searchTerm': 'Tom'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 1)

    def test_question_search_with_no_results(self):
        res =\
            self.client()\
            .post('/questions/search', json={'searchTerm': 'Duck'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def test_get_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 3)

    def test_get_category_if_questions_category_is_correct(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        questions = data['questions']
        for question in questions:
            self.assertEqual(int(question['category']), 1)

    def test_404_if_category_of_questions_does_not_exist(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'requested resource not found')

    def test_get_single_question_for_quiz(self):
        quiz_request = {
            'previous_questions': [],
            'quiz_category': {'type': 'Sports', 'id': '6'}
        }
        res = self.client().post('/quizzes', json=quiz_request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_return_none_if_question_limit_reached_for_quiz(self):
        quiz_request = {
            'previous_questions': [11, 10],
            'quiz_category': {'type': 'Sports', 'id': '6'}
        }
        res = self.client().post('/quizzes', json=quiz_request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['question'])

    def test_correct_category_of_question_for_quiz(self):
        quiz_request = {
            'previous_questions': [11],
            'quiz_category': {'type': 'Sports', 'id': '6'}
        }
        res = self.client().post('/quizzes', json=quiz_request)
        data = json.loads(res.data)

        question = data['question']
        question_category = int(question['category'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question_category, 6)

    def test_422_if_invalid_category_quiz(self):
        quiz_request = {
            'previous_questions': [11],
            'quiz_category': {'type': 'Trick', 'id': '7'}
        }
        res = self.client().post('/quizzes', json=quiz_request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
