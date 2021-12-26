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

## Steps to Run the application

### Python (Django) Backend - Web Server

Open a command-prompt/terminal in the following location

<..>/AIML_Capstone_Project/backend

Activate the virtual environment. This will create a vitrual environment if not present 

```
pipenv shell
```
