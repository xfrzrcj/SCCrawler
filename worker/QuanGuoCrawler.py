from worker import Crawler
import pymysql
import urllib.request
import re

baseUrl = "http://www.dcqjw.gov.cn"
indexUrl = "http://www.dcqjw.gov.cn/ywdt.jsf?id=8"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/66.0.3359.117 Safari/537.36')]


class QGCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl, opener)
        a = soup.find_all("script")[4]
        num = re.findall("total: \d+", a.text)[0]
        return int(num[6:])

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl + "/ywdt.jsf?page="+str(i)+"&id=8"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url, opener)
        lists = soup.find("div", id="list2", class_="list2")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            info_url = baseUrl + "/" + tag.find("a").get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url, opener)
        all_ss = soup.find("div", class_="defaultTitle")
        title_all = all_ss.find("h2")
        info_result.title = title_all.text
        time_source = all_ss.find("div")
        ts = time_source.text.split("\n\t\t\t\t\t\t")
        info_result.time = ts[0]
        info_result.source = ts[1]
        article = soup.find("div", class_="defaultContent")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "全国"
        info.source = info.source.replace("来源：", "").replace("时间", "")
        info.time = info.time.replace("发表时间：", "")
        info.postion = "纪律审查"
        return info


c = QGCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.dcqjw.gov.cn/ywdt.jsf?id=8"))
# c.get_info("http://www.dcqjw.gov.cn/default.jsf?id=29128")

