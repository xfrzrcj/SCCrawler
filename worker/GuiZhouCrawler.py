from worker import Crawler
import pymysql
import urllib.request
import re

baseUrl = "http://www.gzdis.gov.cn"
indexUrl = "http://www.gzdis.gov.cn/gzdt/jlsc/"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/66.0.3359.117 Safari/537.36')]


class GZCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl, opener)
        a = soup.find("div", class_="page").text
        nums = re.findall("[0-9]+", a)
        return int(nums[0])

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/gzdt/jlsc/index_"+str(i)+".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url, opener)
        lists = soup.find("ul", class_="list01")
        tags = lists.find_all("dd")
        urls = []
        for tag in tags:
            href = re.findall('var str_1 = ".*?.html";', tag.text)[0]
            info_url = baseUrl + "/gzdt/jlsc" + href[14:-2]
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url, opener)
        title = soup.find("div", class_="btnr").find("span")
        info_result.title = title.text
        time_source = soup.find("div", class_="btnr").find_all("p")
        info_result.time = time_source[1].text
        info_result.source = time_source[0].text
        article = soup.find("div", id="textBox")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "贵州"
        info.source = info.source.replace(" 信息来源：", "")
        info.time = info.time.replace("发布时间:", "")
        info.postion = "审查调查"
        return info

c = GZCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.gzdis.gov.cn/gzdt/jlsc/index_1.html"))
# c.get_info("http://www.gzdis.gov.cn/gzdt/jlsc/201802/t20180228_2291412.html")
