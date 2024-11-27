from concurrent.futures import ProcessPoolExecutor
import asyncio
import math
import aiohttp
import requests
async def get(url, session):
    try:
        async with session.get(url=url) as response:
            resp = await response.read()
            #print("Successfully got url {} with resp of length {}.".format(url, len(resp)))
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))

# async def main(urls):
#     print('t')
#     async with aiohttp.ClientSession() as session:
        
#         ret = await asyncio.gather(*(get(url, session) for url in urls))
def seq_main(urls):
    with requests.Session() as session:
        return [session.get(url) for url in urls]
    
async def async_process_main(urls, n_threads, verbose = True):
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(max_workers=n_threads) as executor:
        

        tasks = [loop.run_in_executor(executor, seq_main, urls[math.ceil(len(urls)/n_threads) * i\
                                                                    :min(len(urls), math.ceil(len(urls)/n_threads) * (i+1))]) for i in range(n_threads)]
        
        # Or we can just use the method asyncio.gather(*tasks)
        for done in asyncio.as_completed(tasks):
            result = await done
        if verbose:
            print(len(result), result[0])