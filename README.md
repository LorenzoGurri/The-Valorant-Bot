# The Valorant Bot
The Valorant Bot is a Discord bot that offers a multitude of features relating to the game, Valorant:
- Connect
  - Connect a users Valorant account to their Discord account
  - Stored in our database
- Disconnect
  - Disconnect a users Valorant account to their Discord account
- Stats
  - Display the stats of a user from their last 5 competitive games 
- Lineups
  - Offer lineups for players so they can quickly remember or learn a lineup to help their team 
- Agents
  - Offer quick and accessible information about a specified agent in Valorant

## Running Locally
To run the bot locally you must first clone the repository to your local machine.<br><br>
Once cloned, you have to invite the bot to your Discord server with this link:
https://discord.com/api/oauth2/authorize?client_id=1022956315334680699&permissions=515396459584&scope=bot%20applications.commands <br><br>
When the repository is on your local machine, navigate there through the command prompt and run the bot with
```
> python3 main.py
```

## Making changes or adding features 
When working on a new feature or task, we do not want to push directly to the main or review branches.<br>
To start work on a new feature, check that the main branch is up to date and then create a new branch off of the most recent main.
```
> git checkout -b newBranch
```

## Coding Standards
To add a new feature or make any changes, you must follow our coding standards.

### Naming Conventions
Use meaningful and understandable variable and function names.<br><br>
Local variables should use camel case. (e.g. localVar) <br>
Global variables should start with a capital letter. (e.g. GlobalVar) <br>
Constant names should be formed using only capital letters. (e.g. CONSTANT_VAR) <br>

### Indentation
There must be a space after a comma between two function parameters.<br>
Each nested block must be properly indented and spaced.

### Comments
There must be a comment block before each function explaining its purpose.
