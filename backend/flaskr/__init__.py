import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        categories_formatted =\
            {category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'categories': categories_formatted
        })

    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories_response = get_categories()
        categories_data = json.loads(json.dumps(categories_response.json))

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'categories': categories_data.get('categories'),
                'current_category': 'Science'
            })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question =\
          Question.query.filter(Question.id == question_id).one_or_none()

        if not question:
            abort(404)
        question.delete()

        return jsonify({
            'success': True,
            'message': 'question successfully deleted',
            'deleted': question_id
        })

    @app.route('/questions', methods=['POST'])
    def add_new_question():
        body = request.get_json()
        new_question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        try:
            if new_question == '' or new_question is None\
              or answer == '' or answer is None\
              or int(category) not in \
              [category.id for category in Category.query.all()]\
              or int(difficulty) not in [1, 2, 3, 4, 5]:
                raise ValueError

            question = Question(
                question=new_question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            question.insert()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'message': 'question successfully created'
        })

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm')
        search_query = '%{0}%'.format(search_term)
        questions =\
            Question.query.filter(Question.question.ilike(search_query)).all()

        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': 'Science'
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        category =\
          Category.query.filter(Category.id == category_id).one_or_none()

        if not category:
            abort(404)
        questions =\
            Question.query.filter(Question.category == category_id).all()

        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': category.type
        })

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')
        questions = []
        category_ids = [category.id for category in Category.query.all()]

        if quiz_category:
            category_id = int(quiz_category['id'])
            if category_id == 0:
                questions = Question.query.all()
            elif category_id not in category_ids:
                abort(422)
            else:
                questions = Question.query\
                  .filter(Question.category == category_id).all()
        else:
            questions = Question.query.all()

        if len(previous_questions) == len(questions):
            return jsonify({
                'success': True,
                'question': None
            })

        question = random.choice(questions)
        while question.id in previous_questions:
            question = random.choice(questions)

        return jsonify({
            'success': True,
            'question': question.format()
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'requested resource not found'
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unporcessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
