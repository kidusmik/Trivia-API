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
        categories_formatted = {category.id: category.type for category in categories}
        
        return jsonify({
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
        question = Question.query.get(question_id)
        question.delete()
        
        return jsonify({
            'message': 'Delete Successful'
        })

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
            return jsonify({
                'message': 'Create Successful'
            })
        except:
            abort(422)
        
        return jsonify({
            'message': 'Create Successful'
        })

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        search_term = request.form['searchTerm']
        search_query = '%{0}%'.format(search_term)
        questions = Question.query.filter(Question.question.ilike(search_query)).all()

        return jsonify({
            'questions': questions,
            'total_questions': len(questions),
            'current_category': 'Science'
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        category = Category.query.get(category_id)
        category_type = category.type
        
        questions = Question.query.filter(Question.category==category_type).all()
        return jsonify({
            'questions': questions,
            'total_questions': len(questions),
            'current_category': category.format()
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
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        quiz_category = body.get('quiz_category')
        quiz_id = quiz_category.get('id', None)
        questions = Question.query.all()
        """
        if quiz_id != None:
            questions = Question.query.filter(Question.category==quiz_id).all()
        else:
            questions = Question.query.all()
        """ 
        questions_formatted = [question.format() for question in questions]
            
        #questions_sent = []
        question = random.choice(questions_formatted)
            
        while question in previous_questions:
            question = random.choice(questions_formatted)
        
        return jsonify({
            'question': question
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'requested resource not found'
        }), 404

    @app.errorhandler(422)
    def unporcessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity'
        }), 422

    return app
