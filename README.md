# AIML_Capstone_Project
## Great Learning Capstone Project - RSNA Pneumonia Detection Challenge

Penumonia Detection application using Django and Angular.

All coding/implementation contributions and comments are welcome. 
Releases should be ready for deployment otherwise download the code and install dependencies using **pip** and **npm**.

## Prerequisites
### Install Node.js

Download the latest version of [Node.js](https://nodejs.org/en/download/) and install it.
After installing Node.js, check the version of the node and npm using the following command in command prompt/terminal:

```
node -v

npm -v
```

### Install Angular
The frontent is created using [Angular](https://angular.io/). To install Angular run the following command in the command-prompt/terminal:

```
npm install =g @angular/cli
```

We have also use Angular Material UI components which needs to be installed seperately.
Execute the below command to install Angulae Material UI components

```
npm install -g @angular/material

npm install -g material-icons
```

### Python

This version of the application is built using Python 3.9.x version.
Ensure that you have the latest pip version.
Update the pip version using the following command:

```
pip install --upgrade pip
```
or, on Windows the recommended command is:
```
python -m pip install --upgrade pip
```

We will be using the Python virtual environment in order to run the application.
We will install pipenv using pip using the following command:

```
pip install pipenv
```
**Note**: For Mac - install pipenv with [Homebrew](https://brew.sh/).
```
brew install pipenv
```

## Steps to Run the application

### Python (Django) Backend - Web Server

Open a command-prompt/terminal in the following location

<..>/AIML_Capstone_Project/backend

Activate the virtual environment. This will create a vitrual environment if not present 

```
pipenv shell
```

Install all dependencies 

```
pipenv install -r requirements.txt
pip freeze
```

**Note**: Required only for fresh install. Skip for existing project.

Before you can run the application you need to place your saved keras model in the following location:

<..>/AIML_Capstone_Project/backend/library/model

**Note** Currently the model is named as following:
* Classification.h5 - DenseNet201 classification model
* DetectionModel.h5 - YOLO Image object detection model

If you want to change the model name you need to update the following params in **backend/backend_app/settings.py**

```
CLASSIFICATION_MODEL_NAME = 'Classification.h5'
DETECTION_MODEL_NAME = 'DetectionModel.h5'
```

Build the application:
```
cd backend
python manage.py makemigrations
python manage.py migrate
```

Run the server
```
python manage.py runserver
```

### Angular Application - Frontend
Open a command-prompt/terminal in the following location

<..>/AIML_Capstone_Project/frontend

Install dependencies
```
npm install
```
Update the project
```
ng update
```

Update NPM
```
npm update
```

Run the application:
```
ng serve
```
Now open the following site in a browser to access the application:
```
http://localhost:4200
```
