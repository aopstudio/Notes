from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
import json
from multiprocessing import Process, Manager, Pool
from gne import GeneralNewsExtractor, ListPageExtractor
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def save_json(file_path, news_list):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(news_list, ensure_ascii=False, indent=2))


chrome_options = Options()
chrome_options.add_argument("--mute-audio") 
chrome_options.add_argument("--headless")
# 添加header
# chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options, executable_path='../Chromedriver/chromedriver')


def Crawl_people(kw): #人民网
    print("########Crawl 人民网########")
    # driver = webdriver.Chrome(options=chrome_options,executable_path='../Chromedriver/chromedriver')
    BASE_URL = 'http://search.people.cn/s/?keyword='
    suffix = '&st=1&_=1694138532657'

    SEARCH_URL = BASE_URL + kw + suffix
    requirePageNum = 2

    driver.get(SEARCH_URL)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="list-wrapper"]'))
        )
    except Exception as e:
        print("元素还未渲染出来：", e.args)

    link_list = []
    html_list = []

    for i in range(0, requirePageNum):
        # 获得一页中所有文章链接，一般都是10条，可能不足
        sleep(0.5)
        try:
            main_element = driver.find_element(By.CLASS_NAME, "list-wrapper")

        except Exception as e:
            print(e.args)
            break

        html = driver.execute_script("return document.documentElement.outerHTML")

        html_list.append(html)
        # 等待元素加载完成

        try:
            wait = WebDriverWait(driver, 10)
            arr = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'page-next')))
            next_btn = driver.find_element(By.XPATH, "//div[@class='page']/span[last()]")
            # 获取最后一个元素并点击它（跳到下一页）
            # next_btn.click()
            driver.execute_script("arguments[0].click();", next_btn)
        except Exception as e:
            print(i)
            print(e.args)

    print(len(html_list))


    for html in html_list:
        list_extractor = ListPageExtractor()
        each_page_list = list_extractor.extract(html,
                                                feature='//*[@id="rmw-search"]/div/div[2]/div[2]/div[1]/div/ul/li[1]/div/div[1]/a')
        try:
            for item in each_page_list:
                link_list.append(item["url"])
        except:
            continue
    """
    根据新闻链接获取文章内容
    """
    article_list = []
    extractor = GeneralNewsExtractor()

    for link in link_list:

        driver.get(link)
        sleep(0.2)
        print(link)
        try:

            html = driver.execute_script("return document.documentElement.outerHTML")
            result = extractor.extract(html,
                                    # body_xpath='//div[@class="layout rm_txt cf"]',
                                    noise_node_list=['//div[@class="comment-list"]',
                                                        '//div[@class="statement"]',
                                                        '//*[@style="display:none"]'])
            result["url"] = link
            print(result["title"])
            article_list.append(result)
        except Exception as e:
            print(e.args)
            continue

    # driver.quit()
    unique_keys = set(d["title"] for d in article_list)
    result_list = [next(d for d in article_list if d["title"] == k) for k in unique_keys]
    print(len(result_list))
    # save_json(kw + '-人民网-' + str(len(result_list)) + '条.json', result_list)

    return result_list

def Crawl_toutiao(kw): #今日头条
    print("########Crawl 今日头条########")
    # driver = webdriver.Chrome(options=chrome_options,executable_path='../Chromedriver/chromedriver')
    # 今日头条需添加header
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    driver = webdriver.Chrome(options=chrome_options,executable_path='../Chromedriver/chromedriver')
    BASE_URL = 'https://so.toutiao.com/search?dvpf=pc&source=input&keyword='
    suffix = '&pd=information&action_type=pagination&page_num=1&search_id=20230807162908B1B5B5110E8602C4230F'

    link = BASE_URL + kw + suffix
    requirePageNum = 2

    # 等待页面加载完成
    driver.implicitly_wait(5)

    driver.get(link)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'main'))
        )
    except Exception as e:
        print("元素还未渲染出来：", e.args)

    link_list = []
    html_list = []
    list_extractor = ListPageExtractor()

    for i in range(0, requirePageNum):
        for j in range(10):  # 获得一页中所有文章链接，一般都是10条，可能不足
            try:
                main_element = driver.find_element(By.CLASS_NAME, "main")

            except Exception as e:
                print(e.args)
                break

        html = driver.execute_script("return document.documentElement.outerHTML")
        html_list.append(html)
        # 等待元素加载完成
        wait = WebDriverWait(driver, 5)
        try:
            arr = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cs-button-wrap')))

            # 获取最后一个元素并点击它（跳到下一页）
            nextPage = arr[-1]
            nextPage.click()
        except Exception as e:
            print(e.args)
            continue

    print(len(html_list))

    for html in html_list:

        each_page_list = list_extractor.extract(html,
                                                feature='/html/body/div[2]/div[2]/div[1]/div/div/div/div/div[1]/div/a')
        try:
            for item in each_page_list:
                url = "https://www.toutiao.com" + item["url"]
                link_list.append(url)
        except:
            continue

    article_list = []
    extractor = GeneralNewsExtractor()
    wait = WebDriverWait(driver, 5)
    for link in link_list:
        likeNum = 0
        commentNum = 0
        driver.get(link)
        print(link)
        try:

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "main")))
            html = driver.execute_script("return document.documentElement.outerHTML")
            result = extractor.extract(html,
                                    noise_node_list=['//div[@class="comment-list"]',
                                                        '//div[@class="statement"]',
                                                        '//*[@style="display:none"]'])
            
            try:
                likeNum = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div/div[2]/div/div[1]/span').text
                commentNum = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]/div/div[2]/div/div[3]/span').text
                if likeNum.isdigit():
                    likeNum = int(likeNum)
                else:
                    likeNum = 0
                if commentNum.isdigit():
                    commentNum = int(commentNum)
                else:
                    commentNum = 0

                print("点赞数:", likeNum)
                print("评论数：", commentNum)
                readNum = likeNum + commentNum
            except Exception as e:
                print(e.args)
            
            result["url"] = link
            result["read_num"] = readNum
            print(result["title"])
            article_list.append(result)
        except Exception as e:
            print(e.args)
            continue

    unique_keys = set(d["title"] for d in article_list)
    result_list = [next(d for d in article_list if d["title"] == k) for k in unique_keys]
    print(len(result_list))
    # save_json(kw + '-今日头条-' + str(len(result_list)) + '条.json', result_list)
    return result_list

def Crawl_thepaper(kw): #澎湃新闻
    print("########Crawl 澎湃新闻########")
    # driver = webdriver.Chrome(options=chrome_options,executable_path='../Chromedriver/chromedriver')

    DOMAIN_URL = 'https://www.thepaper.cn'
    BASE_URL = 'https://www.thepaper.cn/searchResult?id=' # 澎湃新闻

    SEARCH_URL = BASE_URL + kw
    Cycles = 5 # 点击底部”查看更多“按钮的次数


    driver.get(SEARCH_URL)
    link_list = []
    html_list = []
    driver.implicitly_wait(10)

    """
    滚到底部，点击更多
    """
    for i in range(0, Cycles):

        sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("#" * (i + 1))

    html = driver.execute_script("return document.documentElement.outerHTML")


    list_extractor = ListPageExtractor()
    page_list = list_extractor.extract(html,
                                    feature='//*[@id="__next"]/main/div[2]/div[1]/div/div[5]/div[1]/ul/li[1]/div/a')
    for item in page_list:
        url = DOMAIN_URL + item["url"]
        link_list.append(url)
    """
    根据新闻链接获取文章内容
    """
    article_list = []
    extractor = GeneralNewsExtractor()

    for link in link_list:

        driver.get(link)
        print(link)
        try:

            html = driver.execute_script("return document.documentElement.outerHTML")
            result = extractor.extract(html,
                                    body_xpath='//div[@class="index_cententWrap__Jv8jK"]',
                                    noise_node_list=['//div[@class="comment-list"]',
                                                        '//div[@class="statement"]',
                                                '//*[@style="display:none"]'])

            result["url"] = link
            print(result["title"])
            article_list.append(result)
        except Exception as e:
            print(e.args)
            continue

    unique_keys = set(d["title"] for d in article_list)
    result_list = [next(d for d in article_list if d["title"] == k) for k in unique_keys]
    print(len(result_list))
    # save_json(kw+'-澎湃新闻-'+str(len(result_list))+'条.json', result_list)
    return result_list

def Crawl_guancha(kw): #观察者网
    print("########Crawl 观察者网########")

    BASE_URL = 'https://www.guancha.cn/api/search.htm?click=news&keyword=' # 观察者网

    SEARCH_URL = BASE_URL + kw
    Cycles = 2 # 点击底部”查看更多“按钮的次数

    driver.get(SEARCH_URL)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="main-tow"]'))
        )
    except Exception as e:
        print("元素还未渲染出来：", e.args)

    link_list = []
    html_list = []
    driver.implicitly_wait(10)

    """
    滚到底部，点击更多
    """
    for i in range(0, Cycles):

        sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("#" * (i + 1))
        try:
            Btns = driver.find_elements(By.CLASS_NAME, "add-more")
            if len(Btns) > 0:
                Btns[0].click()
        except Exception as e:
            print(e.args)
            continue

    html = driver.execute_script("return document.documentElement.outerHTML")

    list_extractor = ListPageExtractor()
    page_list = list_extractor.extract(html,
                                    feature='/html/body/div[1]/div[2]/div[4]/div[1]/ul[2]/li[1]/div[1]/h4/a')
    for item in page_list:
        link_list.append(item["url"])
    """
    根据新闻链接获取文章内容
    """
    article_list = []
    extractor = GeneralNewsExtractor()

    for link in link_list:

        driver.get(link)
        print(link)
        try:

            html = driver.execute_script("return document.documentElement.outerHTML")
            result = extractor.extract(html,
                                    noise_node_list=['//div[@class="comment-list"]',
                                                        '//div[@class="statement"]',
                                                '//*[@style="display:none"]'])
            print(result["title"])
            result["url"] = link
            article_list.append(result)
        except Exception as e:
            print(e.args)
            continue


    unique_keys = set(d["title"] for d in article_list)
    result_list = [next(d for d in article_list if d["title"] == k) for k in unique_keys]
    print(len(result_list))
    # save_json(kw+'-观察者网-'+str(len(result_list))+'条.json', result_list)
    return result_list

def Crawl_tencent(kw):
    print("########Crawl 腾讯新闻########")
    # 腾讯新闻需添加header
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
    BASE_URL = 'https://www.qq.com/search.htm?query='
    suffix = '&page=0'

    SEARCH_URL = BASE_URL + kw + suffix
    requirePageNum = 2

    driver.get(SEARCH_URL)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'wrap'))
        )
    except Exception as e:
        print("initial、元素还未渲染出来：", e.args)

    link_list = []
    html_list = []

    for i in range(0, requirePageNum):
        # 获得一页中所有文章链接，一般都是10条，可能不足
        sleep(1)
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'wrap'))
            )
        except Exception as e:
            print("无法定位元素列表：", e.args)
            continue

        html = driver.execute_script("return document.documentElement.outerHTML")

        html_list.append(html)
        # 等待元素加载完成

        try:
            wait = WebDriverWait(driver, 5)
            arr = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item-arrow')))
            next_page = arr[-1]
            next_page.click()
        except Exception as e:
            print(i)
            print(e.args)

    print(len(link_list))

    for html in html_list:

        list_extractor = ListPageExtractor()
        each_page_list = list_extractor.extract(html,
                                                feature='//*[@id="root"]/div/div[1]/div[1]/div[2]/ul/li[1]/a')
        try:
            for item in each_page_list:
                link_list.append("https://new.qq.com" + item["url"])
        except:
            continue


    """
    根据新闻链接获取文章内容
    """
    article_list = []
    extractor = GeneralNewsExtractor()

    for link in link_list:

        driver.get(link)
        print(link)
        try:

            html = driver.execute_script("return document.documentElement.outerHTML")
            result = extractor.extract(html,
                                    body_xpath='//*[@id="ArticleContent"]',
                                    noise_node_list=['//div[@class="comment-list"]',
                                                        '//div[@class="statement"]',
                                                        '//*[@style="display:none"]'])
            result["url"] = link
            print(result["title"])
            article_list.append(result)
        except Exception as e:
            print(e.args)
            continue

    unique_keys = set(d["title"] for d in article_list)
    result_list = [next(d for d in article_list if d["title"] == k) for k in unique_keys]
    
    return result_list

def Crawl_baidu(kw):
    print("########Crawl 百度新闻########")

    BASE_URL = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word='
    suffix = ''
    
    SEARCH_URL = BASE_URL + kw + suffix
    requirePageNum = 2

    driver.get(SEARCH_URL)
    sleep(1)
    link_list = []
    html_list = []

    for i in range(0, requirePageNum):
        # 获得一页中所有文章链接，一般都是10条，可能不足
        sleep(0.1)

        html = driver.execute_script("return document.documentElement.outerHTML")

        html_list.append(html)
        # 等待元素加载完成

        try:
            wait = WebDriverWait(driver, 5)
            arr = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'page-inner')))
            next_btn = driver.find_element(By.XPATH, "//div[@class='page-inner']/a[last()]")
            # 获取最后一个元素并点击它（跳到下一页）
            next_btn.click()
            # driver.execute_script("arguments[0].click();", next_btn)
        except Exception as e:
            print(i)
            print(e.args)

    print(len(html_list))

    for html in html_list:
        # each_page_list = extract_list(html)

        list_extractor = ListPageExtractor()
        each_page_list = list_extractor.extract(html,
                                                feature='//*[@id="1"]/div/h3/a')
        try:
            for item in each_page_list:
                link_list.append(item["url"])
        except:
            continue
    # """
    # 根据新闻链接获取文章内容
    # """
    article_list = []
    extractor = GeneralNewsExtractor()

    for link in link_list:

        driver.get(link)
        print(link)
        try: 

            html = driver.execute_script("return document.documentElement.outerHTML")
            result = extractor.extract(html,
                                    noise_node_list=['//div[@class="comment-list"]',
                                                        '//div[@class="statement"]',
                                                        '//*[@style="display:none"]'])
            result["url"] = link
            print(result["title"])
            article_list.append(result)
        except Exception as e:
            print(e.args)
            continue

    unique_keys = set(d["title"] for d in article_list)
    result_list = [next(d for d in article_list if d["title"] == k) for k in unique_keys]
    print(len(result_list))
    
    return result_list

def Crawl_aracgtn(kw): 
    print("########Crawl 阿拉伯语版环球电视网########")
    driver.maximize_window()
    BASE_URL = 'https://arabic.cgtn.com/search?keyword=' 

    SEARCH_URL = BASE_URL + kw
    Cycles = 5 # 点击底部”查看更多“按钮的次数

    driver.get(SEARCH_URL)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="search-result-content"]'))
        )
    except Exception as e:
        print("元素还未渲染出来：", e.args)

    link_list = []
    html_list = []

    """
    滚到底部，点击更多
    """
    for i in range(0, Cycles):

        try:
            sleep(0.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("#" * (i + 1))

            Btns = driver.find_elements(By.CLASS_NAME, "add-more")
            if len(Btns) > 0:
                Btns[0].click()
        except:
            continue

    html = driver.execute_script("return document.documentElement.outerHTML")

    list_extractor = ListPageExtractor()
    page_list = list_extractor.extract(html,
                                    feature='//*[@id="search-content-relevance"]/div[1]/div/div[1]/a')
    for item in page_list:
        link_list.append(item["url"])
    """
    根据新闻链接获取文章内容
    """
    article_list = []
    extractor = GeneralNewsExtractor()

    for link in link_list:

        driver.get(link)
        print(link)
        try:

            html = driver.execute_script("return document.documentElement.outerHTML")
            result = extractor.extract(html,
                                    noise_node_list=['//div[@class="comment-list"]',
                                                        '//div[@class="statement"]',
                                                '//*[@style="display:none"]'])
            result["url"] = link
            print(result["title"])
            article_list.append(result)
        except Exception as e:
            print(e.args)
            continue

    unique_keys = set(d["title"] for d in article_list)
    result_list = [next(d for d in article_list if d["title"] == k) for k in unique_keys]
    print(len(result_list))
    return result_list

def Crawl_urduapppk(kw): #乌尔都语网站
    print("########Crawl urdu.app.com.pk########")
    BASE_URL = 'https://urdu.app.com.pk/urdu/?s='

    suffix = ''

    link = BASE_URL + kw + suffix
    requirePageNum = 1

    # 等待页面加载完成
    driver.implicitly_wait(5)
    # body = driver.find_element(By.TAG_NAME, 'body')

    driver.get(link)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="td-ss-main-content"]'))
        )
    except Exception as e:
        print("元素还未渲染出来：", e.args)

    link_list = []
    html_list = []

    for i in range(0, requirePageNum):
        for j in range(10):  # 获得一页中所有文章链接，一般都是10条，可能不足
            try:
                main_element = driver.find_element(By.CLASS_NAME, "td-ss-main-content")

            except Exception as e:
                print(e.args)
                break

        html = driver.execute_script("return document.documentElement.outerHTML")
        html_list.append(html)
        # 等待元素加载完成
        wait = WebDriverWait(driver, 5)
        next_page = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@aria-label="next-page"]')))

        next_page.click()

    for html in html_list:
        # each_page_list = extract_list(html)

        list_extractor = ListPageExtractor()
        each_page_list = list_extractor.extract(html,
                                                feature='//*[@id="td-outer-wrap"]/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/h3/a')
        try:
            for item in each_page_list:
                url = item["url"]
                link_list.append(url)
        except:
            continue
    print(len(link_list))
    article_list = []
    extractor = GeneralNewsExtractor()

    for link in link_list:

        driver.get(link)
        print(link)
        try:

            html = driver.execute_script("return document.documentElement.outerHTML")
            result = extractor.extract(html,
                                    noise_node_list=['//div[@class="comment-list"]',
                                                        '//div[@class="statement"]',
                                                        '//*[@style="display:none"]'])

            result["url"] = link
            print(result["title"])
            article_list.append(result)
        except Exception as e:
            print(e.args)
            continue

    unique_keys = set(d["title"] for d in article_list)
    result_list = [next(d for d in article_list if d["title"] == k) for k in unique_keys]
    print(len(result_list))
    return result_list

def Crawl_chinadaily(kw):
    print("########Crawl chinadaily########")
    BASE_URL = 'https://newssearch.chinadaily.com.cn/en/search?query='

    suffix = ''

    link = BASE_URL + kw + suffix
    requirePageNum = 2
    # 等待页面加载完成
    driver.implicitly_wait(5)
    # body = driver.find_element(By.TAG_NAME, 'body')

    driver.get(link)
    link_list = []
    html_list = []
    wait = WebDriverWait(driver, 5)
    for i in range(0, requirePageNum):
        sleep(0.5)
        try:
            # main_element = driver.find_element(By.CLASS_NAME, "lft_art")
            arr = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'lft_art')))

        except Exception as e:
            print("------无法获取文章列表！------")
            print(e.args)

        html = driver.execute_script("return document.documentElement.outerHTML")
        html_list.append(html)
        # 等待元素加载完成
        try:
            next_page = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'next')))
            next_page.click()
        except Exception as e:
            print("------无法点击下一页！------")
            print(e.args)
            continue

    for html in html_list:
        # each_page_list = extract_list(html)

        list_extractor = ListPageExtractor()
        each_page_list = list_extractor.extract(html,
                                                feature='/html/body/div[5]/div[2]/div[5]/div[3]/div[2]/a')
        try:
            for item in each_page_list:
                link_list.append(item["url"])
        except:
            continue

    article_list = []
    extractor = GeneralNewsExtractor()

    for link in link_list:

        driver.get(link)
        print(link)

        try:

            html = driver.execute_script("return document.documentElement.outerHTML")
            result = extractor.extract(html,
                                    noise_node_list=['//div[@class="comment-list"]',
                                                        '//div[@class="statement"]',
                                                        '//*[@style="display:none"]'])
            result["url"] = link
            print(result["title"])
            article_list.append(result)
        except Exception as e:
            print(e.args)
            continue


    unique_keys = set(d["title"] for d in article_list)
    result_list = [next(d for d in article_list if d["title"] == k) for k in unique_keys]
    print(len(result_list))
    return result_list

def time_filter(news_list, start_time='', end_time=''):
    res_list = []
    if start_time != '' and end_time != '': #对时间进行筛选
        start_year, start_month, start_day = start_time.split('-')
        end_year, end_month, end_day = end_time.split('-')
        start_date = datetime(int(start_year), int(start_month), int(start_day))
        end_date = datetime(int(end_year), int(end_month), int(end_day))

        for item in news_list:
            publish_time = item['publish_time'].split(' ')[0]
            timestamp = datetime.strptime(publish_time, '%Y-%m-%d')
            if start_date <= timestamp <= end_date:
                res_list.append(item)

    else:
        res_list = news_list
    
    return res_list

if __name__ == "__main__":


    timestamp = int(time.time())
    _start_time = time.time()

    # 根据来源筛选网站爬取的所有文章列表
    all_crawler_articles_list = []
    # kw = '日本核污水'
    # SAVE_NAME = '克里姆林宫遭袭击'
    # kw = 'هاجم الكرملين'
    # kw = 'روس' #俄罗斯
    # kw = "The Battle of Donbas"

    
    kw = '顿巴斯之战'
    start_time = '' #传入的时间示例 2022-1-1、 2022-6-1
    end_time = ''
    # 来源多选：人民网、今日头条、澎湃新闻、观察者网、腾讯新闻、百度新闻、chinadaily、阿拉伯语环球电视网、；“或”的关系
    # 前端界面选择来源
    source_list = ['今日头条']
    ###################################################
    #多进程爬虫
    manager = Manager()
    article_list = manager.list()
    pool = Pool(processes=len(source_list))

    function_name = "Crawl_toutiao"
    Crawl_toutiao_func = globals()[function_name]

    function_name = "Crawl_people"
    Crawl_people_func = globals()[function_name]

    function_name = "Crawl_thepaper"
    Crawl_thepaper_func = globals()[function_name]

    function_name = "Crawl_guancha"
    Crawl_guancha_func = globals()[function_name]

    function_name = "Crawl_tencent"
    Crawl_tencent_func = globals()[function_name]

    function_name = "Crawl_baidu"
    Crawl_baidu_func = globals()[function_name]

    function_name = "Crawl_aracgtn"
    Crawl_aracgtn_func = globals()[function_name]

    function_name = "Crawl_urduapppk"
    Crawl_urduapppk_func = globals()[function_name]

    function_name = "Crawl_chinadaily"
    Crawl_chinadaily_func = globals()[function_name]

    if '人民网' in source_list:
        pool.apply_async(Crawl_people_func, args=(kw,), callback=article_list.extend)
    if '今日头条' in source_list:
        pool.apply_async(Crawl_toutiao_func, args=(kw,), callback=article_list.extend)
    if '澎湃新闻' in source_list:
        pool.apply_async(Crawl_thepaper_func, args=(kw,), callback=article_list.extend)
    if '观察者网' in source_list:
        pool.apply_async(Crawl_guancha_func, args=(kw,), callback=article_list.extend)
    if '腾讯新闻' in source_list:
        pool.apply_async(Crawl_tencent_func, args=(kw,), callback=article_list.extend)
    if '百度新闻' in source_list:
        pool.apply_async(Crawl_baidu_func, args=(kw,), callback=article_list.extend)
    if '阿拉伯语环球电视网' in source_list:
        pool.apply_async(Crawl_aracgtn_func, args=(kw,), callback=article_list.extend)
    if 'urduapppk' in source_list:
        pool.apply_async(Crawl_urduapppk_func, args=(kw,), callback=article_list.extend)
    if 'chinadaily' in source_list:
        pool.apply_async(Crawl_chinadaily_func, args=(kw,), callback=article_list.extend)

    pool.close()
    pool.join()

    driver.quit()
    
    #返回所有不同来源的文章列表
    all_crawler_articles_list = list(article_list)
    #筛选时间（年月日），可以传参数来筛选；若不传默认为空，返回所有新闻

    res_list = time_filter(all_crawler_articles_list, start_time, end_time)
    save_json(kw+'-爬虫20231031-今日头条.json', res_list)


    _end_time = time.time()
    duration = _end_time - _start_time
    print("时间：{:.2f}秒".format(duration))
