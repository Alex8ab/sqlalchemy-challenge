# sqlalchemy-challenge
Climate analysis on Honolulu, Hawaii to planning a vacation trip from 2017-04-11 to 2017-04-25.

**Objetive:** use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. Using:
  - SQLAlchemy ORM
  - Pandas
  - Matplotlib
  - Flask API

## Step 1 - Climate Analysis and Exploration

### Precipitation Analysis

  - Use SQLAlchemy ORM to retrieve the last 12 months of precipitation data.
  - Select only the date and precipitation values.
  - Sort the DataFrame values by date.
  - Plot the results using the DataFrame plot method.
  - Use Pandas to print the summary statistics for the precipitation data.

![Precipitation](Images/precipitation.png)

### Station Analysis

  - Design a query to calculate the total number of stations.
  - Design a query to find the most active stations.
  - Design a query to retrieve the last 12 months of temperature observation data (TOBS).
  - Plot the results as a histogram

![Histogram](Images/Temp_Histograms.png)

## Step 2 - Climate App
Design a Flask API based on the queries below.

  - Homepage route:
	  - Listing all available routes

  - /api/v1.0/precipitation route:
	  - Returning a JSON representation of a dictionary of dates and precipitation values for all stations from precipitation data for the dates between 08/23/2016 to 08/23/2017

- `/api/v1.0/stations` route:
	- Returning a JSON list of stations with station and station name from the dataset

- `/api/v1.0/tobs` route:
	- Returning a JSON list of temperature observations(TOBS) for the previous year of the most active station last year
	(Date range: 08/23/2016 to 08/23/2017 for active station USC00519281 located in Waihee, HI)
	
- `/api/v1.0/<start>` route:
	- User is able to specify a date and is returned a JSON list of the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date from active station USC00519281

- `/api/v1.0/<start>/<end>` route:
	- User is able to specify a start and end date and is returned a JSON list of the minimum temperature, the average temperature, and the max temperature for that specific date range from active station USC00519281
