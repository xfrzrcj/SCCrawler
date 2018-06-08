from worker import Crawler
import pymysql

baseUrl = "http://www.sdjj.gov.cn/"
indexUrl = baseUrl + "tbbg/index.htm"


class SDCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        return 5

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"tbbg/index_"+str(i)+".htm"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("ul", id="mycarousel")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + "tbbg/" + tag.get('href')[2:]
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("h2")
        info_result.title = title.text
        time_source = soup.find("div", class_="head").find("p").find_all("span")
        info_result.time = time_source[1].text
        info_result.source = time_source[0].text
        article = soup.find("div", id="show3")
        ats = article.find_all("p")
        text = ""
        for at in ats:
            text = text + at.text
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "山东"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "通报曝光"
        return info

c = SDCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# c.get_num()
# print(c.join_url())
# print(c.get_urls("http://www.sdjj.gov.cn/tbbg/index_1.htm"))
# c.get_info("http://www.sdjj.gov.cn/tbbg/201803/t20180306_11255884.htm")
