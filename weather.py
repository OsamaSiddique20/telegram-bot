import requests
import time
# Define the API URL
def getWeather():
    api_url = 'http://api.weatherapi.com/v1/current.json?key=ee42a59c745946199a2173755231203&q=doha&aqi=no'

    # Make a GET request to fetch weather data
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        weather_data = response.json()

        # Extract weather information
        condition_text = weather_data['current']['condition']['text']
        temp_c = weather_data['current']['temp_c']
        humidity = weather_data['current']['humidity']

        # Create the message content as a string
        message_content = f'The condition is {condition_text}.\nThe current weather is {temp_c} degrees\nHumidity: {humidity}'

        # Print the message content
        print(message_content)
    else:
        print('Failed to fetch weather data.')


    return message_content
