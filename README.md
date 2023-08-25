# SCRUMP.CFD
The entire Scrump.CFD website for your... Pleasure? Criticism? Either one

Running docker compose on the docker-compose.yml file will start up an nginx server and make everything in the html folder accesible. The backend of the website needs the following to run:
1. main_state_plots.py
2. ndfd_point_sky.py

That's really it. Those make sure the images containing forecast model data and the forecast of clouds (which comes from a forecast model) are up to date. The first one will fire off
some other scripts in the python folder to get things settled. Make sure you look through the python files and change file paths. Those are important.

Deep in one of the links on the weather page are pictures of my cat which are deleted from the github. You'll have to add pics of your own cat there I guess.
