import requests, json
from bs4 import BeautifulSoup

class ipeenCrawler(object):
    def __init__(self):
        self.baseUrl = 'http://www.ipeen.com.tw'
        self.typeIndexDict = [27, 2, 4, 25, 19, 21, 17, 6, 9, 23, 126, 127, 8, 15, 7]
        self.file = open('ChineseCuisine.txt', 'a')


    def typeSoup(self):
        """
        功能: loop over 每種type
        輸出: 看typeIndexDict有幾個element就呼叫幾次soupProcess_Type，
             每次都丟「一種type網頁」給soupProcess_Type
        """
        for item in self.typeIndexDict:
            typeRes = self.typeResponse(item)
            # print(typeRes.text)
            self.soupProcess_Type(typeRes.text)
            break # 測試只丟「中式料理」


    def typeResponse(self, num):
        """
        輸入: typeIndexDict內的編號
        輸出: 對應那個編號的type的網頁內容
        """
        typeUrl = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-'
        typeUrlTail = '-0/'
        res = requests.get(typeUrl + str(num) + typeUrlTail)
        return res


    def soupProcess_Type(self, resStr):
        """
        輸入: type的一頁網頁原始碼(一頁會有15家餐廳)
        輸出: 得到一個15加餐廳的list，並根據List內容呼叫15次getSharePage
        """
        # print(resStr)
        restaurantList = list()
        soup = BeautifulSoup(resStr, 'html.parser')
        for item in soup.select('.name > a'):
            restaurantList.append(self.baseUrl + item['href'])

        # print(len(restaurantList))
        # for x in restaurantList:
        #     self.getSharePage(x)
        #     break
        self.getSharePage(restaurantList[13])


    def getSharePage(self, restaurantUrl):
        """
        輸入: 一個餐廳的網址
        輸出: 一個餐廳的所有分享文網址串成一個List
        """
        res = requests.get(restaurantUrl)
        soup = BeautifulSoup(res.text, 'html.parser')
        returnList = soup.select('#shop-header > nav > ul > li:nth-of-type(3) > a')
        # print(self.baseUrl + returnList[0]['href'])
        resShare = requests.get(self.baseUrl + returnList[0]['href']) #query該餐廳的分享文的url
        shareSoup = BeautifulSoup(resShare.text, 'html.parser')
        shareLinkList = list()
        nextPageForCheck = list()

        for tag in shareSoup.select('#comments > div.row > div > section > article > div > div.text > h2 > a'):
            shareLinkList.append(self.baseUrl + tag['href'])

        # for item in shareLinkList:
        #     print(item)
        
        # 找到第一頁的「下一頁」按鈕
        nextSharePage = shareSoup.select('#comments > div.row > div > section > div.page-block > a[data-label="下一頁"]')
        
        pageCount = 1
        while True:
            nextPageForCheck.append(self.baseUrl + nextSharePage[0]['href'])

            # query下一頁按鈕
            nextButtonRes = requests.get(self.baseUrl + nextSharePage[0]['href'])
            nextButtonSoup = BeautifulSoup(nextButtonRes.text, 'html.parser')

            # 把下一頁的分享文掛進list
            for tag in nextButtonSoup.select('#comments > div.row > div > section > article > div > div.text > h2 > a'):
                shareLinkList.append(self.baseUrl + tag['href'])

            #再找到它的下一頁按鈕
            nextSharePage = nextButtonSoup.select('#comments > div.row > div > section > div.page-block > a[data-label="下一頁"]')

            print('已經爬完第' + str(pageCount) + '頁的分享文的網址')
            pageCount += 1

            if len(nextSharePage) == 0: break

        # for item in nextPageForCheck: print(item)
        # for item in shareLinkList: print(item)
        print(shareLinkList)
        # self.soupProcess_Share(shareLinkList)



    def soupProcess_Share(self, sharePageList):
        """
        功能: 得到每篇分享文內容並寫檔
        輸入: 一個餐廳的所有分享文的網址List
        輸出: 一篇分享文為一行寫檔
        """
        count = 1
        for item in sharePageList:
            res = requests.get(item)
            soup = BeautifulSoup(res.text, 'html.parser')

            writeStr = ''
            # for p in soup.select('#comment > section > div > div.description > div > p'):
            # for p in soup.select('div.description span'):
            for tag in soup.find_all('div', class_ = 'description'):
                writeStr += tag.text

            writeStr = writeStr.replace('\n', '')
            writeStr = writeStr.replace('\t', '')
            self.file.write(writeStr + '\n')
            print('已經爬完第' + str(count) + '篇分享文')
            count += 1



    def main(self):
        self.typeSoup()
        # testList = ['http://www.ipeen.com.tw/comment/1135841', 'http://www.ipeen.com.tw/comment/1105325', 'http://www.ipeen.com.tw/comment/1094957', 'http://www.ipeen.com.tw/comment/1045226', 'http://www.ipeen.com.tw/comment/1030218', 'http://www.ipeen.com.tw/comment/910950', 'http://www.ipeen.com.tw/comment/842206', 'http://www.ipeen.com.tw/comment/831680', 'http://www.ipeen.com.tw/comment/822970', 'http://www.ipeen.com.tw/comment/779712', 'http://www.ipeen.com.tw/comment/762264', 'http://www.ipeen.com.tw/comment/752684', 'http://www.ipeen.com.tw/comment/612670', 'http://www.ipeen.com.tw/comment/576324', 'http://www.ipeen.com.tw/comment/575660', 'http://www.ipeen.com.tw/comment/552318', 'http://www.ipeen.com.tw/comment/525188', 'http://www.ipeen.com.tw/comment/522396', 'http://www.ipeen.com.tw/comment/426336', 'http://www.ipeen.com.tw/comment/406620', 'http://www.ipeen.com.tw/comment/404516', 'http://www.ipeen.com.tw/comment/403432', 'http://www.ipeen.com.tw/comment/393328', 'http://www.ipeen.com.tw/comment/387555', 'http://www.ipeen.com.tw/comment/384161', 'http://www.ipeen.com.tw/comment/362260', 'http://www.ipeen.com.tw/comment/338617', 'http://www.ipeen.com.tw/comment/260046', 'http://www.ipeen.com.tw/comment/174184', 'http://www.ipeen.com.tw/comment/169978', 'http://www.ipeen.com.tw/comment/132535', 'http://www.ipeen.com.tw/comment/123032', 'http://www.ipeen.com.tw/comment/111585', 'http://www.ipeen.com.tw/comment/84778', 'http://www.ipeen.com.tw/comment/72844', 'http://www.ipeen.com.tw/comment/71778', 'http://www.ipeen.com.tw/comment/65062', 'http://www.ipeen.com.tw/comment/61806', 'http://www.ipeen.com.tw/comment/57144', 'http://www.ipeen.com.tw/comment/56163', 'http://www.ipeen.com.tw/comment/47000', 'http://www.ipeen.com.tw/comment/40453', 'http://www.ipeen.com.tw/comment/39273', 'http://www.ipeen.com.tw/comment/37394', 'http://www.ipeen.com.tw/comment/35003', 'http://www.ipeen.com.tw/comment/30765', 'http://www.ipeen.com.tw/comment/25544', 'http://www.ipeen.com.tw/comment/24294', 'http://www.ipeen.com.tw/comment/22952', 'http://www.ipeen.com.tw/comment/18944', 'http://www.ipeen.com.tw/comment/18460', 'http://www.ipeen.com.tw/comment/14977', 'http://www.ipeen.com.tw/comment/11799', 'http://www.ipeen.com.tw/comment/4573', 'http://www.ipeen.com.tw/comment/188', 'http://www.ipeen.com.tw/comment/200', 'http://www.ipeen.com.tw/comment/1048564', 'http://www.ipeen.com.tw/comment/963440', 'http://www.ipeen.com.tw/comment/835982', 'http://www.ipeen.com.tw/comment/702000', 'http://www.ipeen.com.tw/comment/607724', 'http://www.ipeen.com.tw/comment/581856', 'http://www.ipeen.com.tw/comment/538330', 'http://www.ipeen.com.tw/comment/525112', 'http://www.ipeen.com.tw/comment/416384', 'http://www.ipeen.com.tw/comment/399242', 'http://www.ipeen.com.tw/comment/376147', 'http://www.ipeen.com.tw/comment/258133', 'http://www.ipeen.com.tw/comment/175170', 'http://www.ipeen.com.tw/comment/172044', 'http://www.ipeen.com.tw/comment/170947', 'http://www.ipeen.com.tw/comment/164919', 'http://www.ipeen.com.tw/comment/149313', 'http://www.ipeen.com.tw/comment/73820', 'http://www.ipeen.com.tw/comment/54105', 'http://www.ipeen.com.tw/comment/48077', 'http://www.ipeen.com.tw/comment/31122', 'http://www.ipeen.com.tw/comment/19769', 'http://www.ipeen.com.tw/comment/19740', 'http://www.ipeen.com.tw/comment/18971', 'http://www.ipeen.com.tw/comment/6388', 'http://www.ipeen.com.tw/comment/4895', 'http://www.ipeen.com.tw/comment/3420']
        # self.soupProcess_Share(testList)
        




if __name__ == '__main__':
    ipeenObj = ipeenCrawler()
    ipeenObj.main()
