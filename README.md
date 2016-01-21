Welcome to my capstone project.  The code is finished.  The documentation is still in development.  I will add more here shortly.  This is currently a placeholder.

# Patrick's LoL App

#### __Patrick's LoL App is a web app which provides information about a League of Legends game currently being played.__

Built with:
-----
* Python 3.5
* Django 1.8.4
* PostgresSQL
* JavaScript
* jQuery
* Bootstrap 3.3.6
* requests 2.9.1
* simplejson 3.3.1
* selenium 2.48.0
* Conda 3.18.6
* pip 7.1.2
* Sublime Text 3
* [Slide-in_Panel jQuery plugin](https://codyhouse.co/gem/css-slide-in-panel/)

Installation
-----

##### Establish the environment
This repository contains two "Requirements files" pip_req.txt and conda_req.txt.

To set up the enviroment required to run this app first [install Conda](http://conda.pydata.org/docs/install/quick.html) then use the following terminal commands.  

$ conda create --name \<env> --file conda_req.txt  
$ source activate \<env>  
$ pip install -r pip_req.txt

##### Fork the repository to your computer

On GitHub, navigate to the [project repo](https://github.com/Pjmcnally/lolapp), click fork to create a personal copy, and then use (this guide)[https://help.github.com/articles/fork-a-repo/] to pull your forked copy to your local computer.

##### Establish and populate the database

Create a postgres user and a database name for the app (lolappdb).  If you use a name other than lolappdb change the database section of lolapp/lolapp/settings.txt.

Once the database has been established run the following terminal commands from the root of directory of your fork to populate the databse.  

$ python api_query/fixtures/generate_fixtures.py  
$ python manage.py loaddata all_fix.json
