from worker import Crawler
import pymysql

baseUrl = "http://www.ahjjjc.gov.cn/"
TjgbIndexUrl = "http://www.ahjjjc.gov.cn/sggb/index.html"
XjgbIndexUrl = "http://www.ahjjjc.gov.cn/sggb286/index.html"


class AHTjgbCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        return 5

    def get_index(self):
        return TjgbIndexUrl

    def join_url(self, i):
        url = baseUrl + "sggb/index_" + str(i+1) + ".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", class_="news_row")
        tags = lists.find_all("dt")
        urls = []
        for tag in tags:
            info_url = tag.find("a").get("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        all_s = soup.find("div", class_="article")
        title = all_s.find("h2")
        info_result.title = title.text
        time_source = all_s.find("div", class_="fl")
        ts = time_source.text.replace("\t", "").split("    ")
        info_result.time = ts[0]
        info_result.source = ts[1]
        article = soup.find("div", class_="article_content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "安徽"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("时间：", "")
        info.postion = "厅局级干部"
        return info


class AHXjgbCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        return 5

    def get_index(self):
        return XjgbIndexUrl

    def join_url(self, i):
        url = baseUrl + "sggb286/index_" + str(i+1) + ".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", class_="news_row")
        tags = lists.find_all("dt")
        urls = []
        for tag in tags:
            info_url = tag.find("a").get("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        all_s = soup.find("div", class_="article")
        title = all_s.find("h2")
        info_result.title = title.text
        time_source = all_s.find("div", class_="fl")
        ts = time_source.text.replace("\t", "").split("    ")
        info_result.time = ts[0]
        info_result.source = ts[1]
        article = soup.find("div", class_="article_content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "安徽"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("时间：", "")
        info.postion = "县处级及以下干部"
        return info


c = AHXjgbCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.join_url(1))
# print(c.get_urls("http://www.ahjjjc.gov.cn/sggb/index_2.html"))
# c.get_info("http://www.ahjjjc.gov.cn/sggb/p/51488.html")
