from worker import Crawler
import pymysql
from selenium import webdriver

baseUrl = "http://www.sxfj.gov.cn/"
indexUrl = baseUrl + "PageShowNext.aspx?ID=24"
browser = webdriver.Chrome("d:/chromedriver.exe")


class HNCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("div", attrs={"style": "float:left;width:15%;padding-top:6px;"})
        href = a.text[4:]
        return int(href)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl + "articles/news/subindex/ID:24/page:" + str(i+1)
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("ul", id="li")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.get("href")[1:]
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        browser.get(url)
        info_result.url = url
        title = browser.find_element_by_class_name("title")
        info_result.title = title.text
        info_result.time = browser.find_element_by_id("edate").text
        info_result.source = browser.find_element_by_id("efrom").text
        article = browser.find_element_by_id("frameContent")
        ps = article.find_elements_by_tag_name("p")
        text = ""
        for p in ps:
            text = text + p.text.replace("\t", "") + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "湖南"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "").replace("发表时间", "")
        info.postion = "审查调查"
        return info

c = HNCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
browser.quit()
# print(c.get_num())
# print(c.join_url(1))
# print(c.get_urls("http://www.sxfj.gov.cn/articles/news/subindex/ID:24/page:10"))
# c.get_info("http://www.hbjwjc.gov.cn/ajcc/101809.htm")
