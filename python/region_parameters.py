# DEFINE STATE PARAMETERS FOR PASSING DATA INTO MULTIPROCESSING POOL
from cartopy import crs as ccrs

region_params = [
    [
    {
        'state': 'texas',
        'lonW': -110,
        'lonE': -90,
        'latS': 24.65, #24
        'latN': 37.65, #37
        'tz': 'America/Chicago',
        'projection': ccrs.LambertConformal(central_longitude=-97.5, central_latitude=40.5)
    },
    {
        'state': 'nm',
        'lonW': -120,
        'lonE': -100,
        'latS': 28,
        'latN': 41,
        'tz': 'America/Denver',
        'projection': ccrs.LambertConformal(central_longitude=-97.5, central_latitude=40.5)
    },
    {
        'state': 'ny',
        'lonW': -88,
        'lonE': -68,
        'latS': 34,
        'latN': 47,
        'tz': 'America/New_York',
        'projection': ccrs.LambertConformal(central_longitude=-97.5, central_latitude=40.5)
    },
    {
        'state': 'mn',
        'lonW': -105,
        'lonE': -85,
        'latS': 37, #37
        'latN': 50, #50
        'tz': 'America/Chicago',
        'projection': ccrs.LambertConformal(central_longitude=-97.5, central_latitude=40.5)
    },
    {
        'state': 'wa',
        'lonW': -128,
        'lonE': -108,
        'latS': 36,
        'latN': 49,
        'tz': 'America/Los_Angeles',
        'projection': ccrs.LambertConformal(central_longitude=-97.5, central_latitude=40.5)
    },
    {
        'state': 'national',
        'lonW': -121,
        'lonE': -73,
        'latS': 24.65,
        'latN': 50,
        'tz': 'America/New_York',
        'projection': ccrs.LambertConformal(central_longitude=-97.5, central_latitude=40.5)
    }
    ],
    [
    {
        'state': 'eastern_europe',
        'lonW': 22.2,
        'lonE': 45.2,
        'latS': 44,
        'latN': 61,
        'tz': 'Europe/Moscow',
        'projection': ccrs.LambertConformal(central_longitude=38, central_latitude=53.2)
    },
    {
        'state': 'northern_hemisphere',
        'lonW': -170,
        'lonE': -70,
        'latS': 10,
        'latN': 70,
        'tz': 'America/New_York',
        'projection': ccrs.LambertConformal(central_longitude=-117, central_latitude=41.7)
    },
    {
        'state': 'western_europe',
        'lonW': -16,
        'lonE': 28,
        'latS': 32,
        'latN': 65,
        'tz': 'Europe/London',
        'projection': ccrs.LambertConformal(central_longitude=4.5, central_latitude=45)
    },
    {
        'state': 'japan',
        'lonW': 118,
        'lonE': 148,
        'latS': 28,
        'latN': 48,
        'tz': 'Asia/Tokyo',
        'projection': ccrs.LambertConformal(central_longitude=133, central_latitude=38.2)
    },
    {
        'state': 'east_china',
        'lonW': 101,
        'lonE': 127,
        'latS': 20,
        'latN': 41,
        'tz': 'PRC',
        'projection': ccrs.LambertConformal(central_longitude=114, central_latitude=30.2)
    },
    {
        'state': 'india',
        'lonW': 66,
        'lonE': 91,
        'latS': 5,
        'latN': 36,
        'tz': 'Asia/Kolkata',
        'projection': ccrs.LambertConformal(central_longitude=78.6, central_latitude=26)
    }
    ]
]