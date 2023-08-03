## Project links
<a href="https://t.me/MakserMultiBot" target="_blank"> <img src="https://www.vectorlogo.zone/logos/telegram/telegram-tile.svg" alt="Telegram" width="60" height="60"/></a> 
<a href="https://mak5er.github.io/Multi-Bot/" target="_blank"> <img src="https://bischrob.github.io/images/githubpages/githubpages.jpeg" alt="GitHub Pages" width="65" height="60" style="border-radius: 10px;"></a> 
    

## Project description

This project is a Telegram bot - multitool where users can perform various daily tasks. 
The bot is implemented using the Python programming language and uses the Aiogram framework to interact with the Telegram API.

## Usage

After successfully launching the program and connecting the bot to Telegram, you can run the following commands:

    /start - start interacting with the bot and receive a welcome message.
    /language - change language.

## Functionality

### User

    Generate QR - code.
    View the weather forecast.
    Generate random number.
    Generate password.
    Save their tasks.
    Play built-in telegram games in "Entertainment" section.

### Administrator

    Sending messages on behalf of the bot to all users.
    Ban/unban users from admin pannel.

## Database

The bot uses a SQLite database with the following tables:

    users - stores the identifiers of users who use the bot.
    tasks - stores tasks that the user will save in the "Tasks" section.
