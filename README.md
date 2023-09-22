# Introduction
This is a project to demostrate the use of a langchain chatbot with fastapi. The funcionality is
a bot that will get the user name, id and simptomps and will do the following:
- Generate a json with the user data, urgency and specialty
- Generate the response to the user

# Frontend
The frontend is a simple UI using gradio to display the chatbot.

# Backend
The backend is a fastapi server that uses the langchain chatbot to generate responses.

# How to run
With VS Code just launch backend and frontend, then go to http://127.0.0.1:7860 and start chatting.

# Best practices
- Virtual environment generated through pipenv. To start the environment just run `pipenv shell` and to install the dependencies `pipenv install`

- pre-commit hooks to validate stuff before commiting. To install the hooks run `pre-commit install`
