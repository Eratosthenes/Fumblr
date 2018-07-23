## About

This is an API for an app that lets friends know when they cross paths. 
The simulated mobile client sends the users lat/long to a post endpoint once a second, all day long. 
The user can open the app at any point and see the people they've crossed paths with.

## Usage

Open a terminal and set up the server:

    $gunicorn fumble:app
    
To simulate users, open a separate terminal and run:

    $python3 fumble.py

Then watch the server in action as the simulated users roam around. 
