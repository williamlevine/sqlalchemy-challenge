# SQLAlchemy Challenge - Module 10
This repository contains my code and the resource files for the SQLAlchemy challenge. All files can be found within the `SurfsUp` folder. The jupyter notebook file used for the analysis is titled `climate.ipynb` and the python file used for the Flask API is titled `app.py`. The starter code can be found in the folder titled `StarterCode`, with accompanying files titled `climate_starter.ipynb` and `app_starter.py`, respectively.

The SQLite file used as the main database file for both `climate.ipynb` and `app.py` is titled `hawaii.sqlite` and can be found in the `Resources` folder. Also in this folder are `hawaii_measurements.csv` and `hawaii_stations.csv`, both of which are included in the `.sqlite` file and which can be inspected for column names, column lengths, and so on.

Most of my coding was accomplished through referencing the in-class activities from module 10, which demonstrate how to reflect tables, how to set up the session and engine variables, and how to query using the SQLAlchemy ORM.

I did stray from the lessons a bit in the climate data exploration and analysis section. When creating the precipitation chart, I was having trouble setting up the x-axis ticks to match how it was in the starter code. I thus consulted ChatGPT which provided the `set_major_locator(mdates.MonthLocator())` method. This worked to cleanly establish x-ticks at every month throughout the year-long data query.
