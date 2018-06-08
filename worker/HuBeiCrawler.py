from worker import Crawler
import pymysql

baseUrl = "http://www.hbjwjc.gov.cn/"
indexUrl = baseUrl + "info/iList.jsp?cat_id=10007"


class HBCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("a", class_="all")
        href = a.get('href').split("cur_page=")[1]
        return int(href)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl + "info/iList.jsp?site_id=CMShbjct&cat_id=10007&cur_page=" + str(i+1)
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("ul", class_="list-b-t")
        tags = lists.find_all("h4")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.find("a").get("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("h2", id="tts-title")
        info_result.title = title.text
        time_source = soup.find("p", class_="info")
        ts = time_source.find_all("span")
        info_result.time = ts[0].text
        info_result.source = ts[1].text
        article = soup.find("div", id="tts-text")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text.replace("\t", "") + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "湖北"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "审查调查"
        return info

c = HBCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.join_url(1))
# print(c.get_urls("http://www.hbjwjc.gov.cn/info/iList.jsp?site_id=CMShbjct&cat_id=10007&cur_page=3"))
# c.get_info("http://www.hbjwjc.gov.cn/ajcc/101809.htm")
