from worker import Crawler
import pymysql
import urllib.request

baseUrl = "http://www.tjjw.gov.cn"
indexUrl = "http://www.tjjw.gov.cn/html/quanweifabu/shenchadiaocha/tianjin/jlsc/"
djcfUrl = "http://www.tjjw.gov.cn/html/quanweifabu/shenchadiaocha/tianjin/djcf/"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/66.0.3359.117 Safari/537.36')]


class TJCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl, opener)
        a = soup.find("div", id="pages").find_all("a")
        return len(a)-2

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl + "/html/quanweifabu/shenchadiaocha/tianjin/jlsc/"+str(i+1)+".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url, opener)
        lists = soup.find("ul", class_="l-ul-list-other")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            info_url = tag.find("a").get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url, opener)
        title_all = soup.find("div", class_="l-xq-tite bor-2e")
        info_result.title = title_all.find("h1").text
        info_result.time = title_all.find("label", class_="l-time").text
        info_result.source = title_all.find("label", class_="l-from").text
        article = soup.find("div", class_="l-content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "天津"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "纪律审查"
        return info


class TJDwcfCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        return 1

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl + "/html/quanweifabu/shenchadiaocha/tianjin/jlsc/"+str(i+1)+".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url, opener)
        lists = soup.find("ul", class_="l-ul-list-other")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            info_url = tag.find("a").get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url, opener)
        title_all = soup.find("div", class_="l-xq-tite bor-2e")
        info_result.title = title_all.find("h1").text
        info_result.time = title_all.find("label", class_="l-time").text
        info_result.source = title_all.find("label", class_="l-from").text
        article = soup.find("div", class_="l-content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "天津"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "党纪政务处分"
        return info


c = TJDwcfCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.tjjw.gov.cn/html/quanweifabu/shenchadiaocha/tianjin/jlsc/2.html"))
# c.get_info("http://www.tjjw.gov.cn/html/quanweifabu/2016/08/30/4888.html")

