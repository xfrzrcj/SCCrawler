from worker import Crawler
import pymysql
import re

baseUrl = "http://ccdijl.gov.cn/"
indexUrl = baseUrl + "jwjct2018/scdc/scdc_85946/index.html"


class JiLingCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        js = soup.find(text=re.compile(".*var countPage =.*"))
        lines = js.split("\n")
        i = "0"
        for line in lines:
            if re.match(".*var countPage =.*", line):
                i = re.findall("[0-9]+", line, flags=0)[0]
                break
        return int(i)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl + "jwjct2018/scdc/scdc_85946/index_" + str(i) + ".html"
        return url

    def get_urls(self, url):
        print(url)
        soup = self.get_soup(url)
        lists = soup.find("div", class_="scdc_news_lj")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + "jwjct2018/scdc/scdc_85946" + tag.get("href")[1:]
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("h3")
        info_result.title = title.text
        time_source = soup.find("p", class_="pLine")
        ts = time_source.text.replace("\r", "").replace("\n", "").split("     ")
        info_result.time = ts[1]
        source = ts[0]
        s = re.findall('var laiyuan = ".*?";', source)[0]
        if s == 'var laiyuan = "";':
            info_result.source = "吉林省纪委省监委"
        else:
            info_result.source = s.replace('var laiyuan = "', "")[:-2]
        article = soup.find("div", class_="contentMainPage")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "吉林省"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "审查调查"
        return info


indexUrl = "http://ccdijl.gov.cn/jwjct2018/scdc/djzwcf/"


class JiLingChuFengCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        js = soup.find(text=re.compile(".*var countPage =.*"))
        lines = js.split("\n")
        i = "0"
        for line in lines:
            if re.match(".*var countPage =.*", line):
                i = re.findall("[0-9]+", line, flags=0)[0]
                break
        return int(i)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl + "jwjct2018/scdc/djzwcf/index_" + str(i) + ".html"
        return url

    def get_urls(self, url):
        print(url)
        soup = self.get_soup(url)
        lists = soup.find("div", class_="scdc_news_lj")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + "jwjct2018/scdc/djzwcf" + tag.get("href")[1:]
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("h3")
        info_result.title = title.text
        time_source = soup.find("p", class_="pLine")
        ts = time_source.text.replace("\r", "").replace("\n", "").split("     ")
        info_result.time = ts[1]
        source = ts[0]
        s = re.findall('var laiyuan = ".*?";', source)[0]
        if s == 'var laiyuan = "";':
            info_result.source = "吉林省纪委省监委"
        else:
            info_result.source = s.replace('var laiyuan = "', "")[:-2]
        article = soup.find("div", class_="contentMainPage")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "吉林省"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "党纪政务处分"
        return info


c = JiLingChuFengCrawler()
cc = JiLingCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
cc.start(conns)
conns.close()
# print(c.get_num())
#print(c.join_url(1))
# print(c.get_urls("http://ccdijl.gov.cn/jwjct2018/scdc/scdc_85946/index_4.html"))
# c.get_info("http://ccdijl.gov.cn/jwjct2018/scdc/scdc_85946/201803/t20180319_3749032.html")
