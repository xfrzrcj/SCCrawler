from worker import Crawler
import pymysql
import re

baseUrl = "http://www.qinfeng.gov.cn/"
sggbZjscIndexUrl = baseUrl + "scdc/sggb/zjsc.htm"
sggbDjcfIndexUrl = "http://www.qinfeng.gov.cn/scdc/sggb/djzwcf.htm"
qtgbZjscIndexUrl = baseUrl + "scdc/qtgb/zjsc.htm"
sqtgbDjcfIndexUrl = "http://www.qinfeng.gov.cn/scdc/qtgb/djzwcf.htm"


class SXSggbZjscCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(sggbZjscIndexUrl)
        a = soup.find("td", id="fanye1948")
        num = a.text
        num = re.findall("[0-9]+/[0-9]*", num)
        num = num[0].split("/")[1]
        return int(num)

    def get_index(self):
        return sggbZjscIndexUrl

    def join_url(self, i):
        url = baseUrl+"scdc/sggb/zjsc/"+str(i)+".htm"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("ul", class_="xsxc_index_center_list")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.get('href').replace("../", "")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", class_="article_title")
        info_result.title = title.text
        info_result.time = soup.find("div", class_="article_date").text
        article = soup.find("div", class_="v_news_content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text.replace("\t", "") + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "陕西"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "省管干部，执纪审查"
        return info


class SXSggbDjcfCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(sggbDjcfIndexUrl)
        a = soup.find("td", id="fanye1948")
        num = a.text
        num = re.findall("[0-9]+/[0-9]*", num)
        num = num[0].split("/")[1]
        return int(num)

    def get_index(self):
        return sggbDjcfIndexUrl

    def join_url(self, i):
        url = baseUrl+"scdc/sggb/djzwcf/"+str(i)+".htm"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("ul", class_="xsxc_index_center_list")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.get('href').replace("../", "")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", class_="article_title")
        info_result.title = title.text
        info_result.time = soup.find("div", class_="article_date").text
        article = soup.find("div", class_="v_news_content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text.replace("\t", "") + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "陕西"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "省管干部，党纪政务处分"
        return info


class SXQtgbDjcfCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(sqtgbDjcfIndexUrl)
        a = soup.find("td", id="fanye1948")
        num = a.text
        num = re.findall("[0-9]+/[0-9]*", num)
        num = num[0].split("/")[1]
        return int(num)

    def get_index(self):
        return sqtgbDjcfIndexUrl

    def join_url(self, i):
        url = baseUrl+"scdc/qtgb/djzwcf/"+str(i)+".htm"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("ul", class_="xsxc_index_center_list")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.get('href').replace("../", "")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", class_="article_title")
        info_result.title = title.text
        info_result.time = soup.find("div", class_="article_date").text
        article = soup.find("div", class_="v_news_content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text.replace("\t", "") + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "陕西"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "其他干部，党纪政务处分"
        return info


class SXQtgbZjscCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(qtgbZjscIndexUrl)
        a = soup.find("td", id="fanye1948")
        num = a.text
        num = re.findall("[0-9]+/[0-9]*", num)
        num = num[0].split("/")[1]
        return int(num)

    def get_index(self):
        return qtgbZjscIndexUrl

    def join_url(self, i):
        url = baseUrl+"scdc/qtgb/zjsc/"+str(i)+".htm"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("ul", class_="xsxc_index_center_list")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.get('href').replace("../", "")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", class_="article_title")
        info_result.title = title.text
        info_result.time = soup.find("div", class_="article_date").text
        article = soup.find("div", class_="v_news_content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text.replace("\t", "") + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "陕西"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "其他干部，执纪审查"
        return info


c = SXQtgbZjscCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.qinfeng.gov.cn/scdc/sggb/zjsc.htm"))
# c.get_info("http://www.qinfeng.gov.cn/info/1896/76730.htm")

