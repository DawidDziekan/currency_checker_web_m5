import aiohttp
import asyncio
import datetime
import platform
import sys
import time


class ExchangeRateFetcher:
    async def fetch(self, start_date, end_date):
        url = f'http://api.nbp.pl/api/exchangerates/tables/A/{start_date}/{end_date}/'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        rates_dict = {}
                        for rates_entry in data[0]['rates']:
                            if rates_entry['code'] in ['EUR', 'USD']:
                                rates_dict[rates_entry['code']] = rates_entry['mid']
                        return rates_dict
                    else:
                        print(f"Error status: {response.status} for {url}")
            except aiohttp.ClientConnectorError as err:
                print(f'Connection error: {url}', str(err))

class DaysChecker:
    def check(self, days):
        if days >= 1 and days <= 10:
            return True
        else:
            print("Input must be a number of days between 1 and 10.")
            exit
            
async def get_exchange_rates_for_last_n_days(fetcher, n):
    current_date = datetime.date.today()
    exchange_rates = {}
    for i in range(n):
        date = current_date - datetime.timedelta(days=i)
        formatted_date = date.strftime("%Y-%m-%d")
        rates = await fetcher.fetch(formatted_date, formatted_date)
        if rates:
            exchange_rates[formatted_date] = rates
    return exchange_rates

async def main(days):
    start_time = time.time()
    fetcher = ExchangeRateFetcher()
    exchange_rates = await get_exchange_rates_for_last_n_days(fetcher, days)

    for date, rates in exchange_rates.items():
        print(date, ":", rates)
        
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time: {execution_time}")
        
if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    checker = DaysChecker()
    if len(sys.argv) == 2:
        try:
            number_of_days = int(sys.argv[1])
            if checker.check(number_of_days):
                asyncio.run(main(number_of_days))
        except ValueError:
            print("Input must be a number of days between 1 and 10.")
            exit
    else:
        print("Input must be a number of days between 1 and 10.")
        sys.exit(1)