import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse(session, url, datalis):
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    
    for i in soup.select('.entry-content > .lcp_catlist li'):
        data = {
            'link': i.find('a')['href'],
            'title': i.text.strip()
        }
        datalis.append(data)
    
    nextpage = soup.select_one('.entry-content .lcp_nextlink')
    if nextpage and nextpage.get('href'):
        next_url = nextpage['href']
        await parse(session, next_url, datalis)

async def main(start_url):
    datalis = []
    async with aiohttp.ClientSession() as session:
        await parse(session, start_url, datalis)
    return datalis

data = asyncio.run(main("https://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0=2#lcp_instance_0"))
pd.DataFrame(data).to_excel('Fitgirl-repacks.xlsx',index = False)