

import threading

import requests
urls = [
    f"https://www.thepaper.cn/searchResult?id=巴以冲突"
]
def craw(url):  # 爬虫代码
    r=requests.get(url)
    print(r.text)
    print(url,len(r.text))
craw(urls[0])

import concurrent.futures


# # craw
# with concurrent.futures.ThreadPoolExecutor() as pool:
#     htmls=pool.map(craw,urls)
#     htmls = list(zip(urls,htmls))
#     for url,html in htmls:
#         print(url,len(html))

# print("craw over")

