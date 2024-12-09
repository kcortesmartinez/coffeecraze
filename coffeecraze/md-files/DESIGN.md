Coffee Craze is a web application designed to allow users 
to rank and leave a review for this favorite coffee shops. 
The project has a user registration, login, ranking game, 
and a leaderboard. To run, the project uses Flask for the 
web framework,SQLite for the database, and some Bootstrap. 

Actual design:
In order to maintain the leaderboard, we decided to use a
combination of SQLite and Flask, as was used for the last
CS50 pset. For our users we have the following fields: id, 
username, email, password_hash. For coffee shops we have 
the following: id, name, logo_url, description. For rankings,
we have id, user_id, coffee_shop_id, rank. 

The format is meant to be "head to head", designed based off
of common "this or that" games. We get the coffee shops from 
the database to display to the users. The response from the users
will create the leaderboard with the top choices and rankings. 

We opted to allow users to leave reviews for the shops they are
ranking as well. 