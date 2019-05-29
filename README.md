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

This application is hosted on our droplet at [http://142.93.69.78/](http://142.93.69.78/).

To host this application on your own droplet, follow the following instructions:

First, create a DigitalOcean droplet running ubuntu v18.04 x64.

* Log in as `root`:
  * ```$ssh root@<DROPLET.IP.ADDRESS>```
  * Use the temporary password from an e-mail sent from DigitalOcean
  * Add a new password for the root account as prompted.

* Add a new account with superuser access.
  * ```# add user <NEW_USERNAME>```
  * Add a password for the new account as prompted
  * Enter account information as prompted
  * Add your new account to the `sudo` group
    * ```# usermod -aG sudo <NEW_USERNAME>```

* Testing your new account
  * `su <NEW_USERNAME>`
  * `$ whoami` should show you your new username
  * `$ logout` to return back to the root

* Allowing ssh into new account
```
# mkdir /home/<NEW_USERNAME>/.ssh
# chmod 0700 /root/.ssh /home/<NEW_USERNAME>
# cp -Rfv /root/.ssh /home/<NEW_USERNAME>
# chown -Rfv <NEW_USERNAME>.<NEW_USERNAME> /home/<NEW_USERNAME>/.ssh
# chown -R <NEW_USERNAME>:<NEW_USERNAME> /home/<NEW_USERNAME>
# service ssh restart
# usermod -s /bin/bash <NEW_USERNAME>
```

* Log out of root account
  * `# logout`

* Log into your new account, and install the appropriate packages:
```
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install emacs
$ sudo -H apt install libapache2-mod-wsgi-py3
$ sudo apt install python3-pip
```

* Preparing your project directory
  * Your entire Flask app belongs in a single directory named after your app
  * Put this directory in another of the same name
  * In the outer directory, create `actavius.wsgi` and `actavius.conf`

* Contents in `actavius.wsgi`:
```
#!/usr/bin/python
import sys
sys.path.insert(0,"/var/www/actavius/")
from actavius import app as application
```

* Contents in `actavius.conf`:
```
<VirtualHost *:80>
             ServerName <YOUR.DROPLET.IP.ADDRESS.OR.DOMAIN.URL>
             WSGIScriptAlias / /var/www/actavius/actavius.wsgi
             <Directory /var/www/actavius/actavius/>
                        Order allow,deny
                        Allow from all
             </Directory>
             Alias /static /var/www/actavius/actavius/static
             <Directory /var/www/actavius/actavius/static/>
                     Order allow,deny
                     Allow from all
             </Directory>
</VirtualHost>
```

* Installing pip3 dependencies
  * Change directory to Flask root directory
```
$ sudo -H pip3 install wheel
$ sudo -H pip3 install flask
$ sudo -H pip3 install -r requirements.txt
```

* Typing some Python loose ends
  * Ensure all imports are relative imports, pursuant to python documentation
    * *ex.* ```from .util import students```
  * The files you will need to change relative imports for are ```/__init__.py``` and ```/util/todo.py```
  * Pathnames will cause problems. Ensure you do not use relative paths for opening files. Use the following, and append to `DIR` the file you wish to open:
```
import os
DIR = os.path.dirname(__file__) or '.'
DIR += '/'
```

* Add `www-data` write permissions
  * Change directory to the directory holding the project folder structure (outer directory named `actavius`)
```
$ sudo chgrp -R www-data actavius
$ chmod -R g+w actavius
```

* Move the project folder into `/var/www`
  * Go to the parent directory containing the outer directory of the project file structure (`cd ../`)
```
$ sudo mv actavius /var/www
$ sudo cd /var/www
```
  * Note that files in this folder are now write-protected. You must be in `sudo` mode to edit.

* Put `.conf` file in web serving config folder
  * ```$ sudo mv /var/www/actavius/actavius.conf /etc/apache2/sites-available```

* Install apache2
  * ```$ sudo apt install apache2```

* Enable apache2
  * ```$ sudo a2ensite actavius```

* Enable WSGI module
  * ```$ sudo a2enmod wsgi```

* Reload and restart apache2
```
$ sudo service apache2 reload
$ sudo service apache2 restart
```

* Use the following debugging tools if necessary:
  * Errors, updated in real time:
```
$ sudo tail /var/log/apache2/error.log -f
```
  * All requests, updated in real time:
```
$ sudo tail /var/log/apache2/access.log -f
```

*Credits to [Mr. Brown](https://github.com/tofr) for the original how-to guide on deploying a persistent Flask app on DigitalOcean*
