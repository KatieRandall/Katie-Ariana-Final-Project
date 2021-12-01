# import statements that allow us to use HTTP requests and access the JSON response
import requests
import json

WEATHER_API_KEY = 'd7a59e119eec41cabdf05038212211'  # API key for the Weather API

DEFAULT_ZIP = 90007

# this function makes an HTTP GET request to the API to gather the weather data that is relevant to our signal processing
def get_weather(zip_code):
    params = {
        'key': WEATHER_API_KEY,
        'q': zip_code,
    }

    # making get request to the API
    response = requests.get('http://api.weatherapi.com/v1/current.json', params)

    if response.status_code == 200: # status: OK
        data = response.json() # data now stores the response from the API in JSON format

        # here, we extract the cloud cover percentage, UV index, and integer representing whether it is day or not from the JSON response
        clouds = data['current']['cloud']
        uv = data['current']['uv']
        day_or_not = data['current']['is_day']

        # returning a tuple with these values
        return clouds, uv, day_or_not

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
