# Full Stack API Final Project

## Full Stack Trivia

Trivia is a quiz game which have the following features

1) Display questions - both all questions and by category. category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## API Reference
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000 , which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
'success': False,
'error': 404,
'message': 'resource not found.'
}
```
The API will return the following error types when requests fail:
- 404: resource not found.
- 422: unprocessable. or custom validation error.
- 405: method not allowed.
- 400: bad request.

##Endpoints
### GET /api/categories
- General:
    - Returns a list of category objects, success value, and total number of categories.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/api/categories`
- Sample with page number: `curl http://127.0.0.1:5000/api/categories?page=1`

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
    "success": true,
    "total_categories": 6
}
```

### GET /api/questions
- General:
    - Returns a list of questions objects, category objects, questions success value, and total number of questions.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/api/questions`
- Sample with page number: `curl http://127.0.0.1:5000/api/questions?page=2`
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
    "currentCategory": null,
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        .
        .
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 19
}
```

### POST /api/questions
- General:
    - Creates a new Question using the submitted . Returns the success message and the submitted data with its id.
- Sample: `curl --location --request POST 'http://127.0.0.1:5000/api/questions' \
--header 'Content-Type: application/json' \
--data-raw '{
    "question": "What is your name",
    "answer": "Mahmoud",
    "category": 1,
    "difficulty": 4
}'`
```
{
    "data": {
        "answer": "Mahmoud",
        "category": 1,
        "difficulty": 4,
        "id": 26,
        "question": "What is your name"
    },
    "success": true
}
```

### DELETE /api/questions/{question_id}
- General:
    - Deletes the Question of the given ID if it exists. Returns the id of the deleted Question, Success Value and the rest of the questions.
- Sample: `curl --location --request DELETE 'http://127.0.0.1:5000/api/questions/5'`
```
{
    "deleted": 5,
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        .
        .
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        }
    ],
    "success": true,
    "total_questions": 19
}
```
### POST /api/search
- General:
    - Search for Questions using minimum of 3 letters . Returns the success message, Questions and total number of questions.
- Sample: `curl --location --request POST 'http://127.0.0.1:5000/api/search' \
--header 'Content-Type: application/json' \
--data-raw '{
    "searchTerm": "who"
}'`
```
{
    "currentCategory": null,
    "questions": [
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        }
    ],
    "success": true,
    "totalQuestions": 2
}
```

### GET /api/categories/{category_id}/questions
- General:
    - Based on giving category it returns a list of questions objects, category ID, success value, and total number of questions.
- Sample: `curl --location --request GET 'http://127.0.0.1:5000/api/categories/1/questions'`
```
{
    "currentCategory": 1,
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        .
        .
        {
            "answer": "answ",
            "category": 1,
            "difficulty": 4,
            "id": 26,
            "question": "quesww"
        }
    ],
    "success": true,
    "totalQuestions": 5
}
```

### POST /api/quizzes
- General:
    - Based on giving category and previous question solved it returns the rest of questions objects for same category, success value, and total number of questions.
- Sample: `curl --location --request POST 'http://127.0.0.1:5000/api/quizzes' \
--header 'Content-Type: application/json' \
--data-raw '{"previous_questions": [20, 25],
"quiz_category": {"id": 1, "type": "Science"}}'`
```
{
    "question": {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
}
```
## Deploytment N/A
## Authors
Mahmoud Gamal
## Acknowledgements