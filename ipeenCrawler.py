import requests, json, sys, time
from bs4 import BeautifulSoup


class ipeenCrawler(object):
    def __init__(self, typeNumber):
        self.baseUrl = 'http://www.ipeen.com.tw'
        # typeIndexDict有15種
        self.typeIndexDict = {27:[1500, 'ChineseCuisine.txt'], 2:[500, 'JapaneseCuisine.txt'], 4:[150, 'AsianCuisine.txt'], 25:[500, 'WesternCuisine.txt'], 19:[200, 'Barbecue.txt'], 21:[400, 'Hotpot.txt'], 17:[1000, 'Cafe.txt'], 6:[50, 'Vegetarian.txt'], 9:[70, 'FastFood.txt'], 23:[150, 'ThemeRestaurant.txt'], 126:[150, 'Breakfast.txt'], 127:[15, 'Buffet.txt'], 8:[1000, 'Snack.txt'], 15:[300, 'SweetSoup.txt'], 7:[300, 'Bake.txt']}
        self.typeNumber = typeNumber


    def getTypeUrl(self):
        """
        功能: loop over 每種type
        輸出: 看typeIndexDict有幾個element就呼叫幾次soupProcess_Type，
             每次都丟一個「type網頁」給soupProcess_Type
        """
        typeUrlHead = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-'
        typeUrlTail = '-0/?p='

        print('<===開始處理' + self.typeIndexDict[self.typeNumber][1] + '===>')

        for p in range(1, self.typeIndexDict[self.typeNumber][0]):
            # print(typeUrlHead + str(self.typeNumber) + typeUrlTail + str(p))
            print('==========正在處理第' + str(p) + '頁的所有餐廳==========')
            res = requests.get(typeUrlHead + str(self.typeNumber) + typeUrlTail + str(p))
            self.soupProcess_Type(res.text)
            # break # 測試只丟「該料理的第一頁」
            # if p == 1: break


    def soupProcess_Type(self, resStr):
        """
        輸入: type的一頁網頁原始碼(一頁會有15家餐廳)
        輸出: 得到一個15加餐廳的list，並根據List內容呼叫15次getSharePage
        """
        restaurantList = list()
        soup = BeautifulSoup(resStr, 'html.parser')
        tagList = soup.select('.name > a')
        del tagList[0] # 刪除第一個隨機顯示的餐廳
        for item in tagList:
            restaurantList.append(self.baseUrl + item['href'])

        # for item in restaurantList: print(item)
        count = 0
        for restaurant in restaurantList: # restaurant是餐廳的網址
            count += 1
            print('===已送出該頁第' + str(count) + '家餐廳的連結給getSharePage函式===')
            self.getSharePage(restaurant)
            # break


    def getSharePage(self, restaurantUrl):
        """
        輸入: 一家餐廳的網址
        輸出: 一個餐廳的所有分享文網址串成一個List
        """
        # 找到該餐廳的「分享文」按鈕的url
        res = requests.get(restaurantUrl)
        soup = BeautifulSoup(res.text, 'html.parser')
        returnList = soup.select('#shop-header > nav > ul > li:nth-of-type(3) > a')
        # for item in returnList: print(self.baseUrl + item['href'])
        # print('====' + str(len(returnList)) + '===')

        # print(self.baseUrl + returnList[0]['href'])
        resShare = requests.get(self.baseUrl + returnList[0]['href']) #query該餐廳的分享文按鈕的url
        shareSoup = BeautifulSoup(resShare.text, 'html.parser')

        shareLinkList = list()
        nextPageForCheck = list()

        # 如果有分享文，把它們的連結串進shareLinkList
        articleList = shareSoup.select('#comments > div.row > div > section > article > div > div.text > h2 > a')
        if len(articleList) != 0:
            for tag in articleList: # 如果沒有分享文，會沒有article標籤，shareLinkList會是空串列
                shareLinkList.append(self.baseUrl + tag['href'])

        # for item in shareLinkList: print(item)
        
        # 找到「第一頁」的「下一頁」按鈕
        nextPageButtonList = shareSoup.select('#comments > div.row > div > section > div.page-block > a[data-label="下一頁"]')
        # print(self.baseUrl + nextPageButtonList[0]['href'])

        # 如果有「下一頁」按鈕
        if len(nextPageButtonList) != 0:
            pageCount = 1
            while True:
                # 檢查用，存「下一頁」按鈕的連結
                nextPageForCheck.append(self.baseUrl + nextPageButtonList[0]['href'])
                # query下一頁按鈕
                nextPageResponse = requests.get(self.baseUrl + nextPageButtonList[0]['href'])
                nextPageSoup = BeautifulSoup(nextPageResponse.text, 'html.parser')
                # 把下一頁的分享文的url掛進list
                for url in nextPageSoup.select('#comments > div.row > div > section > article > div > div.text > h2 > a'):
                    shareLinkList.append(self.baseUrl + url['href'])
                #再找到它的下一頁按鈕
                nextPageButtonList = nextPageSoup.select('#comments > div.row > div > section > div.page-block > a[data-label="下一頁"]')

                print('已經爬完第' + str(pageCount) + '頁的分享文的網址')
                pageCount += 1

                if len(nextPageButtonList) == 0: break
        
        print('v v v v v 這家餐廳的所有分享文的連結如下 v v v v v')
        for item in shareLinkList: print(item)
        self.soupProcess_Share(shareLinkList) # 有可能傳空list出去


    def soupProcess_Share(self, sharePageList):
        """
        功能: 得到每篇分享文內容並寫檔
        輸入: 一家餐廳的所有分享文的網址List
        輸出: 一篇分享文為一行寫檔
        """
        if len(sharePageList) == 0:
            pass

        with open('./result/' + self.typeIndexDict[self.typeNumber][1], 'a') as file:
            count = 1
            for item in sharePageList:
                res = requests.get(item)
                soup = BeautifulSoup(res.text, 'html.parser')

                writeStr = ''
                
                for tag in soup.find_all('div', class_ = 'description'):
                    writeStr += tag.text

                writeStr = writeStr.replace('\n', '')
                writeStr = writeStr.replace('\t', '')
                writeStr = writeStr.replace(' ', '')
                file.write(writeStr + '\n')
                print('該餐廳第' + str(count) + '篇分享文已寫檔完畢')
                count += 1
                time.sleep(5)



    def main(self):

        self.getTypeUrl()
        # testList = ['http://www.ipeen.com.tw/comment/1135841', 'http://www.ipeen.com.tw/comment/1105325', 'http://www.ipeen.com.tw/comment/1094957', 'http://www.ipeen.com.tw/comment/1045226', 'http://www.ipeen.com.tw/comment/1030218', 'http://www.ipeen.com.tw/comment/910950', 'http://www.ipeen.com.tw/comment/842206', 'http://www.ipeen.com.tw/comment/831680', 'http://www.ipeen.com.tw/comment/822970', 'http://www.ipeen.com.tw/comment/779712', 'http://www.ipeen.com.tw/comment/762264', 'http://www.ipeen.com.tw/comment/752684', 'http://www.ipeen.com.tw/comment/612670', 'http://www.ipeen.com.tw/comment/576324', 'http://www.ipeen.com.tw/comment/575660', 'http://www.ipeen.com.tw/comment/552318', 'http://www.ipeen.com.tw/comment/525188', 'http://www.ipeen.com.tw/comment/522396', 'http://www.ipeen.com.tw/comment/426336', 'http://www.ipeen.com.tw/comment/406620', 'http://www.ipeen.com.tw/comment/404516', 'http://www.ipeen.com.tw/comment/403432', 'http://www.ipeen.com.tw/comment/393328', 'http://www.ipeen.com.tw/comment/387555', 'http://www.ipeen.com.tw/comment/384161', 'http://www.ipeen.com.tw/comment/362260', 'http://www.ipeen.com.tw/comment/338617', 'http://www.ipeen.com.tw/comment/260046', 'http://www.ipeen.com.tw/comment/174184', 'http://www.ipeen.com.tw/comment/169978', 'http://www.ipeen.com.tw/comment/132535', 'http://www.ipeen.com.tw/comment/123032', 'http://www.ipeen.com.tw/comment/111585', 'http://www.ipeen.com.tw/comment/84778', 'http://www.ipeen.com.tw/comment/72844', 'http://www.ipeen.com.tw/comment/71778', 'http://www.ipeen.com.tw/comment/65062', 'http://www.ipeen.com.tw/comment/61806', 'http://www.ipeen.com.tw/comment/57144', 'http://www.ipeen.com.tw/comment/56163', 'http://www.ipeen.com.tw/comment/47000', 'http://www.ipeen.com.tw/comment/40453', 'http://www.ipeen.com.tw/comment/39273', 'http://www.ipeen.com.tw/comment/37394', 'http://www.ipeen.com.tw/comment/35003', 'http://www.ipeen.com.tw/comment/30765', 'http://www.ipeen.com.tw/comment/25544', 'http://www.ipeen.com.tw/comment/24294', 'http://www.ipeen.com.tw/comment/22952', 'http://www.ipeen.com.tw/comment/18944', 'http://www.ipeen.com.tw/comment/18460', 'http://www.ipeen.com.tw/comment/14977', 'http://www.ipeen.com.tw/comment/11799', 'http://www.ipeen.com.tw/comment/4573', 'http://www.ipeen.com.tw/comment/188', 'http://www.ipeen.com.tw/comment/200', 'http://www.ipeen.com.tw/comment/1048564', 'http://www.ipeen.com.tw/comment/963440', 'http://www.ipeen.com.tw/comment/835982', 'http://www.ipeen.com.tw/comment/702000', 'http://www.ipeen.com.tw/comment/607724', 'http://www.ipeen.com.tw/comment/581856', 'http://www.ipeen.com.tw/comment/538330', 'http://www.ipeen.com.tw/comment/525112', 'http://www.ipeen.com.tw/comment/416384', 'http://www.ipeen.com.tw/comment/399242', 'http://www.ipeen.com.tw/comment/376147', 'http://www.ipeen.com.tw/comment/258133', 'http://www.ipeen.com.tw/comment/175170', 'http://www.ipeen.com.tw/comment/172044', 'http://www.ipeen.com.tw/comment/170947', 'http://www.ipeen.com.tw/comment/164919', 'http://www.ipeen.com.tw/comment/149313', 'http://www.ipeen.com.tw/comment/73820', 'http://www.ipeen.com.tw/comment/54105', 'http://www.ipeen.com.tw/comment/48077', 'http://www.ipeen.com.tw/comment/31122', 'http://www.ipeen.com.tw/comment/19769', 'http://www.ipeen.com.tw/comment/19740', 'http://www.ipeen.com.tw/comment/18971', 'http://www.ipeen.com.tw/comment/6388', 'http://www.ipeen.com.tw/comment/4895', 'http://www.ipeen.com.tw/comment/3420']
        # self.soupProcess_Share(testList)
        




if __name__ == '__main__':
    ipeenObj = ipeenCrawler(int(sys.argv[1]))
    ipeenObj.main()
