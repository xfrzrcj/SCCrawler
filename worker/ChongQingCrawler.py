from worker import Crawler
import pymysql
import urllib.request
import re

baseUrl = "http://jjc.cq.gov.cn"
indexUrl = "http://jjc.cq.gov.cn/html/node_282706.htm"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/66.0.3359.117 Safari/537.36')]


class CQCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl, opener)
        a = soup.find("div", id="displaypagenum").find_all("a")
        return len(a)-1

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl + "/html/node_282706_"+str(i+1)+".htm"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url, opener)
        lists = soup.find("div", id="list")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            info_url = baseUrl + "/html/" + tag.find("a").get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url, opener)
        all_ss = soup.find("div", id="text")
        title_all = all_ss.find("h1")
        info_result.title = title_all.text
        time_source = all_ss.find("div", class_="ls")
        ts = time_source.text
        info_result.time = re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}", ts)[0]
        info_result.source = re.findall("来源：.*? ", ts)[0]
        article = soup.find("div", class_="nr")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "重庆"
        info.source = info.source.replace("来源：", "").replace("时间", "")
        info.time = info.time.replace("时间：", "")
        info.postion = "纪律审查"
        return info


c = CQCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://jjc.cq.gov.cn/html/node_282706_3.htm"))
# c.get_info("http://jjc.cq.gov.cn/html/2018-02/13/content_43845874.htm")

