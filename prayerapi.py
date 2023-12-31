import requests
from datetime import datetime
def get_prayers_time_list():
    list = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    timings = []
    date = datetime.now()
    today = f"{date.month}/{date.day}/{date.year}"

    for i in range(6):
        response = requests.get(f"http://localhost:3000/{list[i]}")
        data = response.json()
        
        for element in data:
            if element['Start Date'] == today:
                prayer_time = element['Start Time']
                time_components = prayer_time.split(":")
                hour = time_components[0]
                minute = time_components[1]
                new_time_string = f"{hour}:{minute} {prayer_time[-2:]}"
                timings.append(new_time_string)
                # Add a delay of 2 seconds (optional)
                # await asyncio.sleep(2)

    



    prayer_list = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    output = ''
    count = 0

    for element in timings:
        output += f'☽︎  {prayer_list[count]} {element}\n'
        count += 1

    print(timings)
    return output

# print(get_prayers_time_list())