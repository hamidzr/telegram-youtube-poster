# Youtube to Telegram Poster
Automatically post youtube videos from a certain channel, playlist, etc to a telegram chat. You can easily use a cron job to automatically setup regular posts.

## Configuration
obtain and configure `TARGET_CHAT TARGET_CHANNEL BOT_TOKEN YOUTUBE_API` through `config.ini`

## Installation
1. install `pipenv`
2. issue `pipenv install` to install the dependencies
3. activate the virtualenv by typing `pipenv shell`
4. obtain and configure different configuration options in `/config.ini`


## TODO
- refactor
  - module for posting single posts
  - posting videos from a channel w/ duplicate prevention
