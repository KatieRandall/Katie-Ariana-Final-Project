# import statements that allow us to use HTTP requests and access the JSON response
import requests
import json

WEATHER_API_KEY = 'd7a59e119eec41cabdf05038212211'  # API key for the Weather API

DEFAULT_ZIP = 90007 #Los Angeles ZIP

# this function makes an HTTP GET request to the API to gather the weather data that is relevant to our signal processing
def get_weather(zip_code):
    params = {
        'key': WEATHER_API_KEY,
        'q': zip_code,
        'days': 7,
    }

    # making get request to the API
    response_cloud = requests.get('http://api.weatherapi.com/v1/current.json', params)
    response_vis = requests.get('http://api.weatherapi.com/v1/forecast.json', params)

    if response_cloud.status_code == 200 and response_vis.status_code == 200: # status: OK
        data_cloud = response_cloud.json() # data_cloud now stores the response from the current API in JSON format
        data_vis = response_vis.json() #data_vis stores the response from the forecast API in JSON format

        # here, we extract the cloud cover percentage, visibility and integer representing whether it is day or not from the JSON response
        clouds = data_cloud['current']['cloud']
        day_or_not = data_cloud['current']['is_day']
        visibility = data_vis['current']['vis_km']

        # returning a tuple with these values
        return clouds, day_or_not, visibility

    else:
        # error handling
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return 0.0, 0.0, 0.0

def weather_init():
    zip_code = DEFAULT_ZIP # assigns zip code to default zip which is Los Angeles, 90007
    return get_weather(zip_code) # calling the above function that returns the relevant weather values

if __name__ == '__main__':
    weather_init() # calling our initialization function above
