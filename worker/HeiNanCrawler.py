from worker import Crawler
import pymysql

baseUrl = "http://www.hnsjct.gov.cn/"
ZggbZjscindexUrl = baseUrl + "sitesources/hnsjct/page_pc/gzdt/jlsc/zggb/zjsc/list1.html"
ZggbDjcfIndexUrl = "http://www.hnsjct.gov.cn/sitesources/hnsjct/page_pc/gzdt/jlsc/zggb/djzwcf/list1.html"
SggbZjscIndexUrl = "http://www.hnsjct.gov.cn/sitesources/hnsjct/page_pc/gzdt/jlsc/sggb/zjsc/list1.html"
ShiggbZjscIndexUrl = "http://www.hnsjct.gov.cn/sitesources/hnsjct/page_pc/gzdt/jlsc/sggb1/zjsc/list1.html"
ShiggbDjcfIndexUrl = "http://www.hnsjct.gov.cn/sitesources/hnsjct/page_pc/gzdt/jlsc/sggb1/djzwcf/list1.html"

class HNZggbZjscCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(ZggbZjscindexUrl)
        a = soup.find("div", id="articleListTable")
        num = a.get('num')
        return int(num)

    def get_index(self):
        return None

    def join_url(self, i):
        url = baseUrl + "sitesources/hnsjct/page_pc/gzdt/jlsc/zggb/zjsc/list"+str(i+1)+".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        tags = soup.find_all("div", class_="colRtitle")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.find("a").get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", class_="cms-article-tit")
        info_result.title = title.text
        time_source = soup.find("div", class_="cms-article-attach").find_all("font")
        info_result.time = time_source[1].text
        info_result.source = time_source[0].text
        article = soup.find("div", class_="article-detail")
        text = article.text
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "河南"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "中管干部，执纪审查"
        return info


class HNZggbDjcfCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(ZggbDjcfIndexUrl)
        a = soup.find("div", id="articleListTable")
        num = a.get('num')
        return int(num)

    def get_index(self):
        return None

    def join_url(self, i):
        url = baseUrl + "sitesources/hnsjct/page_pc/gzdt/jlsc/zggb/djzwcf/list"+str(i+1)+".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        tags = soup.find_all("div", class_="colRtitle")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.find("a").get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", class_="cms-article-tit")
        info_result.title = title.text
        time_source = soup.find("div", class_="cms-article-attach").find_all("font")
        info_result.time = time_source[1].text
        info_result.source = time_source[0].text
        article = soup.find("div", class_="article-detail")
        text = article.text
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "河南"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "中管干部，党纪政务处分"
        return info


class HNSggZjscCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(SggbZjscIndexUrl)
        a = soup.find("div", id="articleListTable")
        num = a.get('num')
        return int(num)

    def get_index(self):
        return None

    def join_url(self, i):
        url = baseUrl + "sitesources/hnsjct/page_pc/gzdt/jlsc/sggb/zjsc/list"+str(i+1)+".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        tags = soup.find_all("div", class_="colRtitle")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.find("a").get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", class_="cms-article-tit")
        info_result.title = title.text
        time_source = soup.find("div", class_="cms-article-attach").find_all("font")
        info_result.time = time_source[1].text
        info_result.source = time_source[0].text
        article = soup.find("div", class_="article-detail")
        text = article.text
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "河南"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "省管干部，执纪审查"
        return info


class HNSHiggbZjscCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(ShiggbZjscIndexUrl)
        a = soup.find("div", id="articleListTable")
        num = a.get('num')
        return int(num)

    def get_index(self):
        return None

    def join_url(self, i):
        url = baseUrl + "/sitesources/hnsjct/page_pc/gzdt/jlsc/sggb1/zjsc/list"+str(i+1)+".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        tags = soup.find_all("div", class_="colRtitle")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.find("a").get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", class_="cms-article-tit")
        info_result.title = title.text
        time_source = soup.find("div", class_="cms-article-attach").find_all("font")
        info_result.time = time_source[1].text
        info_result.source = time_source[0].text
        article = soup.find("div", class_="article-detail")
        text = article.text
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "河南"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "市管干部，执纪审查"
        return info


class HNSHiggbDjcfCrawler(Crawler.CrawlerInterface):

        def get_num(self):
            soup = self.get_soup(ShiggbDjcfIndexUrl)
            a = soup.find("div", id="articleListTable")
            num = a.get('num')
            return int(num)-1

        def get_index(self):
            return None

        def join_url(self, i):
            url = baseUrl + "sitesources/hnsjct/page_pc/gzdt/jlsc/sggb1/djzwcf/list" + str(i + 1) + ".html"
            return url

        def get_urls(self, url):
            soup = self.get_soup(url)
            tags = soup.find_all("div", class_="colRtitle")
            urls = []
            for tag in tags:
                info_url = baseUrl + tag.find("a").get('href')
                urls.append(info_url)
            return urls

        def get_info(self, url):
            info_result = Crawler.Info()
            info_result.url = url
            soup = self.get_soup(url)
            title = soup.find("div", class_="cms-article-tit")
            info_result.title = title.text
            time_source = soup.find("div", class_="cms-article-attach").find_all("font")
            info_result.time = time_source[1].text
            info_result.source = time_source[0].text
            article = soup.find("div", class_="article-detail")
            text = article.text
            self.get_resum_description_from_text(text, info_result)
            return info_result

        def process_info(self, info):
            info.province = "河南"
            info.source = info.source.replace("来源：", "")
            info.time = info.time.replace("发布时间：", "")
            info.postion = "市管干部，党纪处分"
            return info


c = HNSHiggbDjcfCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.join_url(1))
# print(c.get_urls("http://www.hnsjct.gov.cn/sitesources/hnsjct/page_pc/gzdt/jlsc/zggb/zjsc/list1.html"))
# c.get_info("http://www.hnsjct.gov.cn//sitesources/hnsjct/page_pc/gzdt/jlsc/zggb/zjsc/article63005d65ce7b4aae9acafe1d7e13a48e.html")

