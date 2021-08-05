# disc-score-bot

Scorebot for uDisc

Will store .csv files uploaded and responds to commands in order to view these in the discord channel!

Currently supported commands:

%files
> Lists files stored in the channel


%scores
> Lists all scorecards and total scores
%scores course coursename
> Search for all scorecards with coursename
%scores date 01.12.1990
> Search for all scorecards with given date
%scores date 01.12.1990 01.01.1991
> Search for all scorecards between dates


%dates
> Lists all dates for scorecards


Get started:

Based on guide posted here: https://realpython.com/how-to-make-a-discord-bot-python/

1. Setup a new bot from the guide
2. Install python from python.org
3. Install discord.py (pip install -U discord.py)
4. Install python-dotenv (pip install python-dotenv)
5. Create a file called 'token.env' in the root folder and add the token generated from the guide referenced above.
