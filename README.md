# Actavius by Wong-Ray-Down-a-One-Lin-Street

## Roster
* Raymond Wu (Project Manager)
* Tina Wong
* Jason Lin
* Ray Onishi

## Video
* [Watch our video demo here]("/") This is temporary for now.

## Overview
Actavius combines all of the services that a student uses to keep track of their college application activities, such that it is accessible all on one website. In addition to exploring different colleges and looking up details about universities, the user is able to keep track of where they are on a timeline with the help of a to-do list that is populated with deadlines. There is a financial aid page which will allow the user to calculate how much money they might need to spend on a college as well.

## Launch Instructions
### Install and run on localhost
1. First, clone this repository:
```
$ git clone https://github.com/raywu6/Wong-Ray-Down-a-One-Lin-Street.git
```
2. Next, change your directory to go into your local copy of the repository:
```
$ cd Wong-Ray-Down-a-One-Lin-Street
```
3. Activate your virtual environment. If you do not have one set up, you may create one in the current working directory, and activate it like so:
```
$ python3 -m venv venv
$ . venv/bin/activate
```
4. Run the following command to install all the packages needed for the data visualization to display on the Flask server:
```
(venv) $ pip install -r requirements.txt
```
5. Now, activate your virtual environment and run the python file to start the Flask server:
```
(venv) $ python3 app.py
```
6. Visit the website at [http://localhost:5000/](http://localhost:5000/)

### Install and run on Apache2

Visit the website at [http://142.93.69.78/](http://142.93.69.78/)
