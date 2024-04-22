import asyncio
import aiohttp

urls = [
    f'https://www.cnblogs.com/#p{page}' for page in range(1,50+1)
]

async def async_craw(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.text()
            print(f"craw url: {url},{len(result)}")
loop = asyncio.get_event_loop()
tasks = [
    loop.create_task(async_craw(url)) for url in urls
]

import time
start = time.time()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()
print("use time seconds: ",end-start)