from worker import Crawler
import pymysql
import re
import urllib.request
from selenium import webdriver

baseUrl = "http://www.jxlz.gov.cn"
indexUrl = "http://www.jxlz.gov.cn/jjjcyw/jlsc/"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/66.0.3359.117 Safari/537.36')]
browser = webdriver.Chrome("d:/chromedriver.exe")


class JXCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl, opener)
        a = soup.text
        nums = re.findall('createPageHTML\(\d+, 0, "index", "htm"\)', a)[0]
        nums = re.findall("\d+", nums)[0]
        return int(nums)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/jjjcyw/jlsc/index_"+str(i)+".htm"
        return url

    def get_urls(self, url):
        print(url)
        soup = self.get_soup(url, opener)
        lists = soup.find("td", class_="red")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            href = tag.get("href")
            if href.startswith("../../"):
                href = href[5:]
            else:
                if href.startswith("./"):
                    href = "/jjjcyw/jlsc" + href[1:]
            info_url = baseUrl + href
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        browser.get(url)
        title = browser.find_element_by_class_name("tit")
        info_result.title = title.text
        info_result.time = browser.find_element_by_xpath('//em[@class="e e2"]').text
        info_result.source = browser.find_element_by_xpath('//em[@class="e e1"]').text
        article = browser.find_element_by_class_name("TRS_Editor")
        ps = article.find_elements_by_tag_name("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "江西"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间:", "")
        info.postion = "审查调查"
        return info

c = JXCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
browser.quit()
# print(c.get_num())
# print(c.get_urls("http://www.jxlz.gov.cn/jjjcyw/jlsc/index_1.htm"))
# c.get_info("http://www.jxlz.gov.cn/gplz/201804/t20180423_87801.htm")
