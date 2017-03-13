import requests, json
from bs4 import BeautifulSoup

class ipeenCrawler(object):
    def __init__(self):
        self.baseUrl = 'http://www.ipeen.com.tw'
        self.typeIndexDict = [27, 2, 4, 25, 19, 21, 17, 6, 9, 23, 126, 127, 8, 15, 7]

    def typeSoup(self):
        for item in self.typeIndexDict: # loop over 每種type
            typeRes = self.typeResponse(item)
            # print(typeRes.text)
            self.soupProcess_Type(typeRes.text)
            break


    def typeResponse(self, num):
        """
        輸入：編號
        輸出：那個編號的type的網頁內容
        """
        typeUrl = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-'
        typeUrlTail = '-0/'
        res = requests.get(typeUrl + str(num) + typeUrlTail)
        return res


    def soupProcess_Type(self, resStr):
        """
        輸入：type的一頁網頁原始碼
        輸出：該type一頁中各家餐廳的網址（一頁15個）成一個list
        """
        # print(resStr)
        restaurantList = list()
        soup = BeautifulSoup(resStr, 'html.parser')
        for item in soup.select('.name > a'):
            restaurantList.append(self.baseUrl + item['href'])

        for x in restaurantList:
            print(x)




        


    def main(self):
        self.typeSoup()



if __name__ == '__main__':
    ipeenObj = ipeenCrawler()
    ipeenObj.main()