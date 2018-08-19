import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from send_email import Mailer
from excel import deal_excel


def get_html(url):
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 启动浏览器，获取网页源代码
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    html = browser.page_source

    # print(f"browser text = {browser.page_source}")
    # browser.quit()

    return html


def get_data_href(html):

    soup = BeautifulSoup(html, 'html.parser')

    target_all_a = soup.find_all('a')
    target_text = '中国外汇交易中心受权公布人民币汇率中间价公告">'
    target_date = []
    target_href = []
    for item in target_all_a:
        item = str(item)
        try:
            target_href_pos = re.search(target_text, item).span()
            if target_href_pos:
                target_href_pos2 = re.search('/zhengcehuobisi/\w*/\w*/\w*/\w*/index.html', item).span()
                target_href.append(item[target_href_pos2[0]:target_href_pos2[1]])
                target_date.append(item[107:target_href_pos[0]])
        except:
            continue

    # 现在直接返回list中最新的0号位置即可，如果以后有改变，再升级优化成时间匹配

    return target_date[0], target_href[0]


def deal_source(target_date, target_href):

    new_url = 'http://www.pbc.gov.cn' + target_href
    html = get_html(new_url)
    soup = BeautifulSoup(html, 'html.parser')
    source_text = str(soup.find_all('p')[0])
    source_text_list = source_text.split('，')
    source_text_str = '*'.join(source_text_list)
    source_text_list = source_text_str.split(', ')
    source_text_str = '*'.join(source_text_list)
    source_text_list = source_text_str.split('：')
    source_text_str = '*'.join(source_text_list)
    source_text_str = re.sub('<p>', '', source_text_str)
    source_text_str = re.sub('。', '', source_text_str)
    source_text_str = re.sub('</p>', '', source_text_str)
    source_text_str = re.sub('对人民币', '*', source_text_str)
    source_text_str = re.sub('人民币1元对', '1元*', source_text_str)
    source_text_list = source_text_str.split('*')
    count = 0
    rate_key = []
    rate_value = []
    for item in source_text_list:
        if count % 2 == 0:
            rate_value.append(item)
        else:
            rate_key.append(item)
        count = count + 1
    rate_dict = dict(zip(rate_key, rate_value))
    for item in rate_dict.keys():
        print(item, ':', rate_dict[item])
    return rate_key, rate_value, target_date


if __name__ == '__main__':

    url = 'http://www.pbc.gov.cn/zhengcehuobisi/125207/125217/125925/index.html'
    html = get_html(url)
    target_date, target_href = get_data_href(html)
    rate_key, rate_value, target_date = deal_source(target_date, target_href)
    deal_excel(rate_key, rate_value)
    # send list
    mail_to_list = ["921348203@qq.com", "hunter.yang@beibei.com"]  # "291796294@qq.com"]
    mail_title = 'Rate'
    mail_content = 'chiara 小主，这是你的汇率报表，请查收。'
    mm = Mailer(mail_to_list, mail_title, mail_content)
    res = mm.send_mail()
    print(res)
