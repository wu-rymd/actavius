# Actavius by Wong-Ray-Down-a-One-Lin-Street

## Roster
* Raymond Wu (Project Manager)
* Tina Wong
* Jason Lin
* Ray Onishi

## Video
* [Watch our video demo here]("https://youtu.be/RJNqBX_dWpo")

## Overview
Actavius combines all of the services that a student uses to keep track of their college application activities, such that it is accessible all on one website. In addition to exploring different colleges and looking up details about universities, the user is able to keep track of where they are on a timeline with the help of a to-do list that is populated with deadlines. There is a financial aid page which will allow the user to calculate how much money they might need to spend on a college as well.

## Necessary packages
You can download all of the necessary packages by running `pip install -r requirements.txt`.

* **Flask** (version 7.0): Python web microframework
  * `pip install flask`
* **Jinja2** (version 2.10.1): HTML templating
  * *Included in `pip install flask`*
* **passlib** (version 1.7.1): Hashing passwords in database
  * `pip install passlib`

## Launch Instructions
### Install and run on localhost
Most of our dependencies can be installed through simple pip command listed below, however, you will need Python 3 and SQLite3 on your system which must be installed. Python 3 is the programming language used to run the application while sqlite3 is used to maintain our databases. Both of these are essential. If, in your terminal, running `$ python3` invokes the Python 3 interpreter, and running `$ sqlite3` opens the SQLite3 shell, you are good to go. If not, please follow the links below.
* [Install sqlite3](https://mislav.net/rails/install-sqlite3/ "Install sqlite3")
* [Install python3](https://realpython.com/installing-python/ "Install python3")

First, clone this repository:
```
$ git clone https://github.com/raywu6/actavius.git
```
Activate your virtual environment. If you do not have one set up, you may create one in the current working directory, and activate it like so:
```
$ python3 -m venv dc
$ . dc/bin/activate
```

Next, change your directory to go into your local copy of the repository:
```
(dc)$ cd actavius
```
Now, install all of the requirements needed to run this project. This command simply installs jinja and Flask. Flask is the python framework used to allow for simpler software development. Jinja is used to connect front end HTML/CSS code to back-end Python Flask code.

```
(dc)$ pip install -r requirements.txt
```

Now, run the python file to start the Flask server:
```
(dc)$ python3 __init__.py
```

Finally, open your web browser and open [http://localhost:5000/](http://localhost:5000/).

To terminate your server instance, type <kbd> CTRL </kbd> + <kbd> C </kbd>.

To exit your virtual environment, run the command `$ deactivate`.

### Install and run on Apache2

This application is hosted on our droplet at [http://104.248.13.208/](http://104.248.13.208/).

To host this application on your own droplet, follow the following instructions:

First, create a DigitalOcean droplet running ubuntu v18.04 x64.

* Log in as `root` via ssh
* [Add a new account with superuser access](https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart)
* [Allowing ssh into new account](https://groups.google.com/a/stuy.edu/d/msg/softdev18-19/UIyq_zQXiN0/64EndEQMEAAJ)
* Log out of root account
* Log into your new account, and install the appropriate packages:
```
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install libapache2-mod-wsgi-py3
$ sudo apt install python3-pip
```

* Install apache2
 ```
 $ sudo apt install apache2
 ```

* Change the directory: ```$ cd /var/www```

* Clone this repository into /var/www
```
$ sudo git clone https://github.com/raywu6/actavius.git
```

* Installing pip3 dependencies
```
$ sudo pip3 install -r /var/www/actavius/requirements.txt
```

* Add `www-data` write permissions to folder
```
$ sudo chgrp -R www-data /var/www/actavius
$ sudo chmod -R g+w /var/www/actavius
```

* **You must edit `/var/www/actavius/actavius.conf` so that the IP address after `ServerName` is the IP address of your DigitalOcean droplet.**
  * Note that files in this folder are now write-protected. You must be in `sudo` mode to edit.

* Put `.conf` file in web serving config folder
```
$ sudo mv /var/www/actavius/actavius.conf /etc/apache2/sites-available
```

* Enable apache2
```
$ sudo a2ensite actavius
```

* Enable WSGI module
```
$ sudo a2enmod wsgi
```

* If prompted to activate the new configuration, run
```
$ systemctl reload apache2
```

* Reload and restart apache2
```
$ sudo service apache2 reload
$ sudo service apache2 restart
```

*Credits to [Mr. Brown](https://github.com/tofr) for the original how-to guide on deploying a persistent Flask app on DigitalOcean*
