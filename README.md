# Patrick's LoL App

__Note__

This site is unfortunately now obsolete. Ongoing changes to the League of Legends API have made my site no longer work. Since this was create as a learning project I have not taken the time to update the project to keep it in line with the current LoL API.  

If I chose to continue work on this the goal would be to update, clean up, and incorporate this project into my portfolio page. If that occurs future development will happen in that repo. This project also needs to be modernized to work with new game modes and champions added by Riot.

__Welcome to my PDX CodeGuild capstone project.__

League of Legends is a video game played, typically, between two teams of 5 people. The goal of the game is to fight the other team and to destroy their base. There are over 120 champions (playable characters) in the game and each of them can be configured many, many different ways. Knowing more about your opponents and your team can help you to play better and win more games.

My app provides current game information about both the skill level of your opponents and the champions they playing as well as how that champion is configured.

Use
-----
To use Patrick's LoL App simply enter a League of Legends summoner name into the box on the home page. If that player is currently playing a game you will be taken to the dashboard where game data is displayed. Click any player to get more detailed info. 

Built with:
-----
* Django 1.9.13
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
The root directory of this repository contains a "Requirements file", requirements.txt.

To set up the environment required to run this web app first install [python](https://www.python.org/downloads/), [virtualenv and virtualenv wrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/).  

Type the following command to create a virtual environment using python 3.4:  
$ mkvirtualenv \<env name> -ppython3.4

Activate the virtual environment.  
$ workon \<env name>

Install all of the required packages.  
$ pip3 install -r requirements.txt

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

From the repo's root directory (/lolapp/) run the following command to launch this web app.

$ python3 manage.py runserver

To-Do
-----
### Refactors & Minor improvements
* Add input validation and sanitization
* Refactor to add template inheritance
* Add nav menu collapse
* Refactor secrets file from two to opponents

### New features
* Include ranked data for previous season
* Add much more robust history data
    * Games played/won/lost
    * Average Kills/Deaths/Assists per game
* Build new database with average stats per rank tier
* Compare player stats to their ranked tier.  


Screenshots
-----
[Home page](https://github.com/Pjmcnally/lolapp/blob/master/screenshots/Patricks%20LoL%20App%20Home.png)  
[Dashboard](https://github.com/Pjmcnally/lolapp/blob/master/screenshots/Patricks%20lol%20app%20dashboard.png)  
[Slide in panel](https://github.com/Pjmcnally/lolapp/blob/master/screenshots/Patricks%20LoL%20app%20slide%20in.png)
