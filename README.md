# rover-pi

Raspberry Pi-powered rover, for the CA Space Grant Scholarship through NASA at San Diego Miramar College.

## Rover

The `/rover` directory contains code focused on the physical rover, including driving, environmental readings, and uploading data to a Google spreadsheet. 

`minute_demo.py` sets the rover on a one minute loop of driving and sensing environmental data.

## Server

The `/server` directory contains code to host a lightweight server and display aggregated data and visualizations of the collected environmental data.

`app.py` runs the server, which can then be accessed locally.