import requests

# OpenWeatherMap API: https://openweathermap.org/current

OWM_API_KEY = 'eea08d1ae70611d0938f089aa4d93e8b'  # OpenWeatherMap API Key

DEFAULT_ZIP = 90007

def get_weather(zip_code):
    params = {
        'appid': OWM_API_KEY,
        'zip': zip_code,
        'units': 'imperial'
    }

    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params)

    if response.status_code == 200: # Status: OK
        data = response.json()

        # TODO: Extract the temperature & humidity from data, and return as a tuple
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        clouds = data['clouds']['all']
        #rain = data[1]['main']
        return temp, humidity, clouds

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return 0.0, 0.0, 0.0


def weather_init():
    zip_code = DEFAULT_ZIP
    return get_weather(zip_code)


if __name__ == '__main__':
    weather_init()