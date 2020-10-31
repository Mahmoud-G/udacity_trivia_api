import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f'postgresql://postgres:rootP@ssw0rd@localhost:5432/{self.database_name}'
        setup_db(self.app, self.database_path)

        self.new_question = {"question": "question1",
                            "answer": "answer",
                            "category": 2,
                            "difficulty": 1
                             }

        self.new_question_wrong_input = {"question": "qu",
                                         "answer": "answer",
                                         "category": "string",
                                         "difficulty": 1
                                         }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # test get categories
    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

    # test get categories with invalid page number
    def test_404_get_categories_requesting_beyond_valid_page(self):
        res = self.client().get('/api/categories?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found.')

    # test get questions
    def test_get_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])

    # test get questions with invalid page number
    def test_404_get_questions_requesting_beyond_valid_page(self):
        res = self.client().get('/api/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found.')

    # test delete questions
    def test_delete_questions(self):
        res = self.client().delete('/api/questions/4')
        data = json.loads(res.data)

        query = Question.query.filter(Question.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 4)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(query, None)

    # test delete questions
    def test_404_while_delete_not_exist_questions(self):
        res = self.client().delete('/api/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # test create questions
    def test_post_questions(self):
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    # test create questions with wrong input
    def test_post_questions_invalid_input(self):
        res = self.client().post('/api/questions', json=self.new_question_wrong_input)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])


    # test search questions
    def test_post_search_questions(self):
        res = self.client().post('/api/search', json={"searchTerm": "who"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    # test search questions with less than 3 letter search
    def test_post_search_questions_invalid_input(self):
        res = self.client().post('/api/search', json={"searchTerm": "w"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # test category question
    def test_get_category_question(self):
        res = self.client().get('/api/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    # test category question with wrong category id
    def test_get_category_question_invalid_category(self):
        res = self.client().get('/api/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # test quiz
    def test_post_quiz(self):
        res = self.client().post('/api/quizzes', json={"previous_questions": [1, 2, 3],
                                                      "quiz_category": {'id': 1, 'type': 'Science'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    # test quiz with invalid input
    def test_post_quiz_invalid_input(self):
        res = self.client().post('/api/quizzes', json={"previous_questions": [1, 2, 3],
                                                       "quiz_category": 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    # test quiz with all pervious questions taken
    def test_post_quiz_full_taken_questions(self):
        res = self.client().post('/api/quizzes', json={"previous_questions": [20, 21, 22, 25],
                                                       "quiz_category": {'id': 1, 'type': 'Science'}})
        data = json.loads(res.data)
        print(data['question'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], None)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()