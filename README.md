## About

This is an API for an app that lets friends know when they cross paths. 

The simulated mobile client sends the user's lat/long to a post endpoint at
random intervals of less than 1 second. 

The user can open the app at any point and see the people they've crossed paths with.

## Usage

Open up two separate terminals and go into a virtualenv with:

    $ pipenv shell

In one terminal, set up the server:

    (Fumblr-t3LBUAy-) bash-3.2$ gunicorn fumble:app
    
In the other terminal, run the app to simulate users roaming for ~10 seconds:

    (Fumblr-t3LBUAy-) bash-3.2$ python3 fumble.py

Watch the server in action as the simulated users roam around, then view the
results of GET requests for each user. 

Exit the virtualenvs with: 

    (Fumblr-t3LBUAy-) bash-3.2$ exit
