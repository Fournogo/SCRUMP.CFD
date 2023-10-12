# SCRUMP.CFD
The entire Scrump.CFD website for your... Pleasure? Criticism? Either one

Running docker compose on the docker-compose.yml file will start up an nginx server and make everything in the html folder accesible. The backend of the website needs the following to run somewhat often:

1. new_model_data.py
2. ndfd_point_sky.py
3. sounding.py

The first one runs every hour *EXCEPT* the second hour after an hour divisible by 6 in UTC time. Since that's too confusing here are all the times it would run (all in UTC): 0, 1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 21, 22, 23

That's how I do it currently because every 6 hours a new GFS forecast is dopped and my machine takes 2 hours to do alllllll the plots I currently have enabled. Your milage may vary so consider allowing your machine some extra time, upgrading your computer, or optimizing my code. (Official optimizations coming soon)

The second one runs every hour on the 30 minute mark.

The third one runs at 00:30 and 12:30 UTC time. 

That's really it. Those make sure the images containing forecast model data and the forecasted cloud cover are up to date. The first one will fire off
some other scripts in the python folder to get things settled. Make sure you look through the python files and change any file paths. Those are important.

Yes I know the JavaScript namespace is a nightmare. I'm open to suggestions and improvements through GitHub or avery@scrump.cfd. I just haven't had the time or desire to go through and refactor it all. I did rework the CSS though so don't worry I'll get to it at some point. For now I'm marching on with new features hehe

Deep in one of the links on the weather page (the gif at the bottom of the page) are pictures of my cat which are deleted from the github. You'll have to add pics of your own cat there
