import asyncio
import aiohttp

async def get_games_list():
    string = ''
    async with aiohttp.ClientSession() as session:
        for i in range(1, 150):
            try:
                response = await session.get(f"http://localhost:4050/match{i}")
                data = await response.json()
                
                if 'Pakistan' in data['team1'] or 'Pakistan' in data['team2']:
                    print(data)
                    t = int(data['time'][:2])
                    new_time = str(t + 2) + data['time'][2:]
                    string += '\n⎯⎯⎯⎯⎯⎯ ˳༄꠶ ⎯⎯⎯⎯⎯⎯\n'
                    string += f"{data['team1']} vs {data['team2']}\nDate: {data['date']}\n{data['match']}\nVenue: {data['venue']}\nTime: {new_time}"
            except Exception as error:
                print(error)
    
    return string

async def main():
    print(await get_games_list())

if __name__ == "__main__":
    asyncio.run(main())
