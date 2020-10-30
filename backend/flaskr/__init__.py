import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from cerberus import Validator
from models import setup_db, Question, Category
from sqlalchemy import func

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  setup_db(app)


  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r'api/*': {'origins': '*'}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# pagination function that list 10 items by default
  def pagination(request, selection, list_per_page=10):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * list_per_page
    end = start + list_per_page

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/categories')
  def retrieve_categories():
    query = Category.query.order_by(Category.type).all()
    query_count = len(query)
    paginated_data = pagination(request, query, list_per_page=query_count)

    if len(paginated_data) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in query},
      'count': query_count
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/api/questions')
  def retrieve_questions():
    question_query = Question.query.order_by(Question.id).all()
    category_query = Category.query.order_by(Category.type).all()
    question_query_count = len(question_query)
    question_paginated_data = pagination(request, question_query)
    # data = {'questions': question_paginated_data, 'categories': {category.id:category.type for category in category_query}}
    # print(data['categories'])

    if len(question_paginated_data) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': question_paginated_data,
      'categories': {category.id: category.type for category in category_query},
      'currentCategory': None,
      'total_questions': question_query_count
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      query = Question.query.filter(Question.id == question_id).one_or_none()
      if query is None:
        abort(404)

      query.delete()
      question_query = Question.query.order_by(Question.id).all()
      paginated_data = pagination(request, question_query)
      question_query_count = len(question_query)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'data': paginated_data,
        'count': question_query_count
      })

    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/api/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    # new_question = body.get('question', None)
    # new_answer = body.get('answer', None)

    # check if the answer and category are integer value
    try:
      new_difficulty = int(body.get('difficulty', None))
      new_category = int(body.get('category', None))
    except Exception as e:
      abort(422, {'message': e})

    # schema validation
    schema = {'question': {'type': 'string', 'required': True, 'minlength': 5},
              'answer': {'type': 'string', 'required': True, 'minlength': 1},
              'category': {'type': 'integer', 'required': True, 'minlength': 1},
              'difficulty': {'type': 'integer', 'required': True, 'minlength': 1}
              }
    v = Validator(schema)
    # data formated as dict to validate as cerberus validator
    request_data = {'question': body.get('question', None),
                    'answer': body.get('answer', None),
                    'category': new_category,
                    'difficulty': new_difficulty
                    }
    # print(v.validate(request_data))
    # print(v.errors)
    if v.validate(request_data):
      try:
        query = Question(**request_data)
        query.insert()

        return jsonify({
          'success': True,
          'data': query.format(),
        })

      except Exception as e:
        print(e)
        abort(422)
    else:
      abort(422, {'message': v.errors})


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/api/search', methods=['POST'])
  def search_question():
    body = request.get_json()

    # schema validation
    schema = {'search_term': {'type': 'string', 'required': True, 'minlength': 3}}
    v = Validator(schema)

    # data formated as dict to validate as cerberus validator
    request_data = {'search_term': body.get('searchTerm', None)}
    # print(v.validate(request_data))
    # print(v.errors)
    if v.validate(request_data):
      try:
        query = Question.query.order_by(Question.id).filter(
                Question.question.ilike(f'%{request_data["search_term"]}%')).all()
        paginated_data = pagination(request, query)
        query_count = len(query)

        return jsonify({
          'success': True,
          'questions': paginated_data,
          'totalQuestions': query_count,
          'currentCategory': None
        })


      except Exception as e:
        print(e)
        abort(422)
    else:
      abort(422, {'message': v.errors})

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/api/categories/<int:category_id>/questions')
  def category_question(category_id):
    query = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
    query_count = len(query)
    paginated_data = pagination(request, query, list_per_page=query_count)

    if len(paginated_data) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': paginated_data,
      'totalQuestions': query_count,
      'currentCategory': category_id
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/api/quizzes', methods=['POST'])
  def quizzes():
    body = request.get_json()

    try:
      quiz_category_dict = body.get('quiz_category', None)
      quiz_category = int(quiz_category_dict['id'])
    except Exception as e:
      abort(422)

    # schema validation
    schema = {'previous_questions': {'type': ['list'], 'schema': {'type': 'integer'}},
              'quiz_category': {'type': 'integer', 'required': True, 'minlength': 1}
    }
    v = Validator(schema)

    # data formated as dict to validate as cerberus validator
    request_data = {'previous_questions': body.get('previous_questions', None),
                    'quiz_category': quiz_category}
    # print(v.validate(request_data))
    # print(v.errors)
    if v.validate(request_data):
      try:
        query = Question.query.filter(Question.category == request_data['quiz_category'])\
                              .filter(Question.id.notin_(request_data['previous_questions']))\
                              .order_by(func.random()).first()
        print(query)
        # paginated_data = pagination(request, query)
        # query_count = len(query)

        return jsonify({
          'success': True,
          'question': query.format() if query else None
          # 'count': query_count
        })

      except Exception as e:
        print(e)
        abort(422)
    else:
      abort(422, {'message': v.errors})

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_fount(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found.'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    message = 'unprocessable.'
    return jsonify({
      'success': False,
      'error': 422,
      'message': message if error.description['message'] is None else error.description['message']
    }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed.'
    }), 405

  return app
