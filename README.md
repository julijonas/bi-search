# Backend

## Installing the backend
Follow these steps:
1. Make sure you have python 3.6 installed (virtual environment is fine) and are using it.
2. Install pipenv: ```pip install pipenv```
3. Navigate to the backend directory in your terminal
4. Run ```pipenv shell```
5. Once in the new virtual environment run ```pipenv install``` to install the dependencies in the pipfile

## Running the backend
1. Navigate to the backend directory
2. Make sure you have activated the pipenv environment with ```pipenv shell``` (same as you did during the installation process)
3. Run the server with ```python run.py```
4. Navigate to http://127.0.0.1:5000/ and see if the message **Server works fine, congrats!** is returned.

## Installing new backend packages:
Use ```pipenv install <package-name>``` from within the backend directory (while you are in the pipenv shell)


# Frontend

## Installing the frontend
Follow these steps:
1. Install node.js and npm
2. Navigate to the frontend directory
3. Run ```npm install``` to install dependencies

## Running the frontend
1. Navigate to the frontend directory
2. Run ```npm start``` to run the react magic
4. Navigate to http://localhost:3000/ and see if the website is there

## Frontend-backend communication test
Navigate to the webste and press the **Test Server Connection** button. An alert box should appear containing a json with some affirming words. If you get the **Failed** message, something is wrong.

## Installing new frontend node packages
Use ```npm install <package-name>``` from within the frontend directory.
