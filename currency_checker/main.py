import aiohttp
import asyncio
import datetime
import platform


class ExchangeRateFetcher:
    async def fetch(self, date):
        url = f'http://api.nbp.pl/api/exchangerates/tables/A/{date}/'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        rates = {entry['code']: entry['mid'] for entry in data[0]['rates'] if entry['code'] in ['EUR', 'USD']}
                        return rates
                    else:
                        print(f"Error status: {response.status} for {url}")
            except aiohttp.ClientConnectorError as err:
                print(f'Connection error: {url}', str(err))

async def get_exchange_rates_for_last_n_days(fetcher, n):
    current_date = datetime.date.today()
    exchange_rates = []
    for i in range(n):
        date = current_date - datetime.timedelta(days=i)
        formatted_date = date.strftime("%Y-%m-%d")
        rates = await fetcher.fetch(formatted_date)
        if rates:
            exchange_rates.append({formatted_date: rates})
    return exchange_rates

async def main():
    try:
        days = int(input("Enter number of days: "))
        if days < 1 or days > 10:
            raise ValueError("Number of days must be between 1 and 10.")
    except ValueError as e:
        print("Invalid input. Please enter a number between 1 and 10.")
        return

    fetcher = ExchangeRateFetcher()
    exchange_rates = await get_exchange_rates_for_last_n_days(fetcher, days)
    
    for item in exchange_rates:
        print(item)

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())