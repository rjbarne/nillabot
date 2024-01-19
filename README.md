# nillabot
A reference Discord bot for a game "Idle Angels"

# About Nillabot
The bot's name is taken after my dog, Nilla. It accesses a relational database to return useful information to a user in Discord. 
<br><br>
The main bot `nillabot.py` contains all of the code to run the bot. It requires `ia.db` to access data. The script `refresh_db.py` will create the database and update any tables with up-to-date information based on local files. The script `angel_icons.py` creates images that are pushed to an image asset repository which the bot accesses to display images. The `db_edit.ipynb` Jupyter Notebook is used to manually delete rows from tables for any information that is sensitive and not suitable for display (such as premature information before it's officially announced). 
<br><br>
The bot utilizes slash commands, buttons and autocompletion lists. The SQL queries are protected against malicious injection by utilizing placeholders. The community can easily reach me on Discord for any bugs and suggestions. The official community staff on behalf of the game developers have approved the use of the game data for community enrichment. 
