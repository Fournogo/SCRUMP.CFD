# SCRUMP.CFD
The entire Scrump.CFD website for your... Pleasure? Criticism? Either one

Running docker compose on the docker-compose.yml file will start up an nginx server and make everything in the html folder accesible. The backend of the website needs the following to run somewhat often:

1. main_state_plots.py
2. ndfd_point_sky.py

I run them every hour since NOAA releases a new forecast at that frequency.

That's really it. Those make sure the images containing forecast model data and the forecast of clouds (which comes from a forecast model) are up to date. The first one will fire off
some other scripts in the python folder to get things settled. Make sure you look through the python files and change any file paths. Those are important.

Yes I know the JavaScript namespace is a nightmare. I'm open to suggestions and improvements through GitHub or avery@scrump.cfd. I just haven't had the time or desire to go through and refactor it all. I did rework the CSS though so I'm sure I'll get to it at some point. For now I'm marching on with new features. Thank u for the concern.

Deep in one of the links on the weather page (the gif at the bottom of the page) are pictures of my cat which are deleted from the github. You'll have to add pics of your own cat there
