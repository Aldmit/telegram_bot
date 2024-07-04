# CHI_BOT

This bot was created to learn Chinese characters using the flashcard method. 

## It works on a simple principle:

1. A user is created in database with base settings.
2. It is assigned entry-level parameters.
3. And the generator produces words, if spelled correctly the user is awarded points.
4. When there are enough points, a new word is revealed to the user, according to its order in the dictionary.
5. The user can hide learned words from the search results and switch to repetition mode, or remain in study mode.

## File system structure

- core
    - db_functions
    - handlers
    - help_functions
    - level_system
    - word_generator
- .env
- config.py
- database.sql
- main.py
- requirments.txt

### Description

- **db_functions** - description of database functions.
- **handlers** - handler functions that make up the core application logic.
- **help_functions** - functions for testing and debugging that set user values.
- **level_system** - functions that implement the business logic of the application and organize the system of user levels.
- **word_generator** - word and phrase generation functions.

- **.env** - bot token and user chat ID.
- **config.py** - associates the access point with the bot token in the .env file.
- **database.sql** - bot database where all user data is storedю.
- **main.py** - main entry point that logs actions within the programю.
- **requirments.txt** - requirments and dependencies for the bot to work correctly.

## Commands inside the bot

- **/chi** - launches the bot.
- **/status** - shows the user's status.
- **/skip** - removes a word from the main dictionary output.
- **/wordlist** - shows all words removed from the search results.
- **/restore** [handzi] - restores the word according to the Chinese character in the output.
- **/info** [handzi] - shows information on Chinese characters.
- **/exit** - terminates the application.

