
# Patrick's LoL App
__Welcome to my PDX CodeGuild capstone project.__

League of Legends is a video game played, typically, between two teams of 5 people.  The goal of the game is to fight the other team and to destroy their base.  There are over 120 champions (playable characters) in the game and each of them can be configured many, many different ways.  Knowing more about your opponents and your team can help you to play better and win more games.

My app provides current game information about both the skill level of your opponents and the champions they playing as well as how that champion is configured.

Use
-----
To use Patrick's LoL App simply enter a League of Legends summoner name into the box on the home page.  If that player is currently playing a game you will be taken to the dashboard.

Built with:
-----
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

#### Establish the environment
The root directory of this repository contains two "Requirements files" pip_req.txt and conda_req.txt.

To set up the environment required to run this web app first [install Conda](http://conda.pydata.org/docs/install/quick.html) then run the following terminal commands.  


$ conda create --name \<env> --file conda_req.txt  
$ source activate \<env>  
$ pip install -r pip_req.txt

These commands (in respective order):  
* Create a Conda environment with the required packages installed.  
* Activate that environment.  
* Use pip to install any remaining required packages.  

#### Fork the repository and clone it to your computer

On GitHub, navigate to the [project repo](https://github.com/Pjmcnally/lolapp), click fork to create a personal copy, and then use [this guide](https://help.github.com/articles/fork-a-repo/) to clone your forked copy to your local computer.

#### Create a League of Legends account and create secrets file with your API key.

Go to the [Riot API Getting Started page](https://developer.riotgames.com/docs/getting-started) and follow the instructions to create an account and to get your API key.

Create a file called secrets.py.  The only line in this file should be:  
 API_KEY = 'Put your API Key here (leave the quotes)'

 Copy the secrets file into the the two directories below:
 * lolapp/
 * lolapp/api_query/fixtures

#### Establish and populate the database

Create a postgres user and a database for the app.  The default database name is lolappdb.  If you use a name other than lolappdb change the database section of lolapp/lolapp/settings.txt.

Once the database has been established run the following terminal commands from the root of directory of your fork to populate the database.  

$ python api_query/fixtures/generate_fixtures.py  
$ python manage.py loaddata all_fix.json

#### You are now good to go.

From the repo's root directory (/lolapp/) run the following command to lauch this web app.

$ python3 manage.py runserver

Screenshots
-----
[Home page](https://github.com/Pjmcnally/lolapp/blob/master/screenshots/Patricks%20LoL%20App%20Home.png)  
[Dashboard](https://github.com/Pjmcnally/lolapp/blob/master/screenshots/Patricks%20lol%20app%20dashboard.png)  
[Slide in panel](https://github.com/Pjmcnally/lolapp/blob/master/screenshots/Patricks%20LoL%20app%20slide%20in.png)
