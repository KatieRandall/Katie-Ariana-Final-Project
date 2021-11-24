import requests
import json

# Weather API

WEATHER_API_KEY = 'd7a59e119eec41cabdf05038212211'  # Weather API Key

DEFAULT_ZIP = 90007

def get_weather(zip_code):
    params = {
        'key': WEATHER_API_KEY,
        'q': zip_code,
    }

    response = requests.get('http://api.weatherapi.com/v1/current.json', params)

    if response.status_code == 200: # Status: OK
        data = response.json()
        # print(json.dumps(data, indent=4))

        # TODO: Extract the temperature & humidity from data, and return as a tuple
        clouds = data['current']['cloud']
        uv = data['current']['uv']
        day_or_not = data['current']['is_day']
        return clouds, uv, day_or_not

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return 0.0, 0.0, 0.0


def weather_init():
    zip_code = DEFAULT_ZIP
    return get_weather(zip_code)


if __name__ == '__main__':
    weather_init()
