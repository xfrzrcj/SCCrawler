from worker import Crawler
import pymysql

baseUrl = "http://www.hljjjjc.gov.cn/"
indexUrl = baseUrl + "news.php?cid=15"


class HljCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("a", attrs={"title": "最后一页"})
        num = a.get('href').split('page=')[1]
        return int(num)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = indexUrl+"&page="+str(i+1)
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", class_="main01_con font_16").find("ul")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", class_="main02_tit01")
        info_result.title = title.text
        time_source = soup.find("div", class_="main02_tit02 black font_16")
        ts = time_source.text.split("        ")
        info_result.time = ts[1]
        info_result.source = ts[0]
        article = soup.find("div", class_="main02_con font_17")
        text = article.text.replace("\n\n\n\n\n", "\n").replace("\n\n\n", "\n").replace("\r", "")
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "黑龙江"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "曝光台"
        return info

c = HljCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')

c.start(conns)
conns.close()
# c.get_num()

