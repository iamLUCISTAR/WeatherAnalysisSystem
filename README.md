
# Weather Analysis System v1.0.0
Django application that fetches real-time weather data from a public API, processes the data, and provides insights and displays an alert if it's extreme.
1. Backend Technologies Used:
- Django
- SQLite3
2. Frontend Technologies Used:
- HTML, CSS, JS
3. Deployment:
- render.com
3rd party api's for weather data:
- https://open-meteo.com/en/docs

## DB design
The DB consists of two tables,
- Table city: To store the city coordinates which was searched for.
- Table weatherdata: To store the last 24hr weather report of searched city.

![Database Schema](https://github.com/iamLUCISTAR/WeatherAnalysisSystem/blob/main/Screenshot%202024-09-18%20at%2010.58.39%20AM.png?raw=true)


## Code

The application is hosted in render.com endpoint.

Endpoints:
- Search page: https://weatheranalysissystem-u7j9.onrender.com/weather/search/

Working Flow:
  1. User can interact with the Weather Analysis System using the search page.
  2. User can enter a single or multiple city names to search for the weather report.
  3. First the system parses the city names to gather the latitude and longitude coordinates.
  4. Then the corresponding weather reports for each city is retrieved from the public api then processed and stored in the internal db.
  5. Then the processed data is fetched from db and is served to the user with data trends like current weather and average weather condition for last 24 hrs.
  6. If the average temperature of last 24hrs of a city exceeds 30degrees, an alert will be popped up while displaying the search results.

## Author

- [Sharath Bhadrinath](https://github.com/iamLUCISTAR)
