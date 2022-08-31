import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start =  (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        
        return jsonify({
            'categories': [category.format() for category in categories]
        })

    @app.route(/questions)
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_books) == 0:
            abort(404)

            return jsonify({
                'questions': current_questions,
                'total_questions': len(selection),
                'categories': Category.query.order_by(Category.id).all(),
                'current_category': current_books #TODO
            })

    @app.route('/questions/<int:question_id', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        question.delete()

    @app.route('/questions', methods=['POST'])
    def add_new_question():
        body = request.get_json()
        
        new_question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')
        
        try:
            question = Question(
                question=new_question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            question.insert()
        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_venues():
        search_term = request.form['searchTerm']
        search_query = '%{0}%'.format(search_term)
        questions = Question.query.filter(Question.question.ilike(search_query)).all()

        response = jsonify({
            'questions': questions,
            'total_questions': len(questions),
            'current_category': 
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        category = Category.query.get(category_id)
        category_type = category.type
        
        questions = Question.query.filter_by(Question.category==category_type).all()
        return jsonify({
            'questions': questions,
            'total_questions': len(questions),
            'current_category': category_id
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
