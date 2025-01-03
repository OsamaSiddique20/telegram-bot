import requests

def tConvert(time):
    # Check correct time format and split into components
    time = str(time)
    time_components = time.split(':')
    
    if len(time_components) > 1:  # If time format correct
        hours = int(time_components[0])
        minutes = int(time_components[1])
        am_pm = ' AM' if hours < 12 else ' PM'
        hours = hours % 12 or 12  # Adjust hours
        return f"{hours}:{minutes:02d}{am_pm}"
    return time

def get_prayers_time_list():
    prayer_list = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    timings = []
    try:
        response = requests.get('http://0.0.0.0:8080/db.json')
        data = response.json()
        
        for prayer in prayer_list:
            time = tConvert(data[prayer]['time'])  # Convert time format
            timings.append(time)
        
        output = ''
        for count, element in enumerate(timings):
            output += '☽︎  ' + prayer_list[count] + ' ' + element
            if count != len(timings) - 1:  # Check if it's not the last element
                output += '\n'
        
        return output
    except Exception as e:
        print(e)
        return []

# Example usage:
print(get_prayers_time_list())
