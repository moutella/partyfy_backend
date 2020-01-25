Tired of having your friends ask for you to unlock your phone while having a party so they can select a song to be played? Well, I am

# How to use it
- clone this repository
- install dependencies
    - it's recommended that you use a virutal environment
- create a symbolic link on partyfy_backend
    - `ln -s settings.dev.py settings.py`
- create a database thats going to be used in the project
- create your .env file and fill it
    - `cp .env.example .env`
- run migrations
- create a super user that is going to be allowed to start a new session
