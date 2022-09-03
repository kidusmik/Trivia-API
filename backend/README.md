# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

# API Reference

## Getting Started
- Base URL: Currently the app can only be run locally and is not hosted at a base URL. The default backend host address is `127.0.0.1:5000`
- Authentication: Currently the API does not require authentication of API keys.

## Error Handling
The API will return these errors when request fails:
- 404: Bad Request
- 405: Request Not Found
- 422: Unprocessable

Errors are returned as JSON objects in the following format:
```
{
    'success': False,
    'error': 404,
    'message': 'resource could not be found'
}
```
```
{
    'success': False,
    'error': 405,
    'message': 'method not allowed'
}
```
```
{
    'success': False,
    'error': 422,
    'message': 'unprocessable'
}
```

## Endpoints

### GET /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with two keys, `success` with value `True` and `categories`, that contains an object of `id: category_string` key: value pairs.
- `curl 127.0.0.1:5000/categories`
```
{  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

### GET /questions
- Fetches a list of questions in which the items are dictionary of formatted `Question` objects.
- Request Arguments: None
- Returns: An object with five keys:
-- `success`: with value `True`
-- `questions`: contains a list of paginated questions
-- `total_questions`: an integer with the total number of questions
-- `categories`: contains an object of `id: category_string` key: value pairs.
- `curl 127.0.0.1:5000/questions`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "Science", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

### DELETE /questions/{question_id}
- General:
-- Deletes the question of the given ID if it exists, Returns success value and a message.
-- `curl -X DELETE http://127.0.0.1:5000/questions/4`

```
{  "message": "question successfully deleted", 
  "success": true
}
```

### POST /questions
- General:
-- Creates a new question using the submitted `question`, `answer`, `category` and `difficulty` values. On success it returns a success value and a message. If any of the keys is missing or any of the values is either empty string or `None` it returns an error with code `422`. 

- `curl 127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Which country is known as the Horn of Africa?", "answer": "Ethiopia", "category": 3, "difficulty": 4}'`
Returns success:
```
{
  "message": "question successfully created", 
  "success": true
}
```
- `curl 127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Which country is known as the Horn of Africa?", "category": 3, "difficulty": 4}'`
Returns with an error because it is missing the `answer` field:
```
{
  "error": 422, 
  "message": "unprocessable", 
  "success": false
}
```

### POST /questions/search
- General: Searches for a question based on the search term passed through the key `searchTerm` returns a success value, all the questions that match the search term and the total number of questions matching the search term.
- `curl 127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Tom"}'`
```
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

### GET /categories/{category_id}/questions
- General: Fetches all questions of a specific category based on the `category_id` passed through the URL. Returns a success value, all the questions inside that category and  the total number of questions inside the category. 
- `curl 127.0.0.1:5000/categories/1/questions`
```
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

### POST /quizzes
- General: Sends a POST request in order to get the next question. Returns a success value, and a single question object.
- `curl 127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 7, 12, 5], "quiz_category": 2}'`
```
{
  "question": {
    "answer": "One", 
    "category": 2, 
    "difficulty": 4, 
    "id": 18, 
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  }, 
  "success": true
}
```

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
