import math, operator, jieba, sys

class Tfidf(object):
    """
    使用main函式時需傳入兩個參數: 1) 輸入檔案 2) 輸出檔案
    """
    def __init__(self, fileStr, writeFile):
        self.file = open(fileStr, 'r')
        self.writeFile = writeFile


    def tf(self, smallList): #回傳一個文章中各個斷詞的tf值的list
        """
        輸入: 一篇文章所有斷詞的list
        輸出: 該篇文章每個斷詞的tf值串成List
        """
        TfValueList = list() #用於保存本篇文章的各字詞tf值
        for x in smallList:
            TfValueList.append((float(smallList.count(x)))/(float(len(smallList))))

        return TfValueList


    def containing(self, word, bigList): #回傳一個詞在全部文章中出現的篇數
        """
        輸入: 一個斷詞 & 整個文本的雙層List
        輸出: 該個斷詞「在全部文章中出現的次數」
        """
        sum = 0
        for List in bigList: #一個List是一個文章的所有斷詞組成的list
            if word in List:
                sum = sum + 1

        return sum


    def idf(self, smallList, bigList): #回傳一個文章中各個斷詞的idf值的list
        IdfValueList = []
        for x in smallList:
            IdfValueList.append(math.log(len(bigList)/self.containing(x, bigList)))

        return IdfValueList


    def tfidf(self, smallList, bigList): #回傳一個斷詞與其tfidf值對應的字典
        """
        輸入: 一個文章的List & 整個文本的雙層List
        輸出: 
        """
        ResultList = []
        ResultTfList = self.tf(smallList)
        ResultIdfList = self.idf(smallList, bigList)
        
        for n in range(len(smallList)):
            ResultList.append(ResultTfList[n] * ResultIdfList[n])

        ComparisonDict = dict(zip(smallList, ResultList))
        return ComparisonDict


    def readFileAsList(self):
        bigDoubleLayerList = list()
        for item in self.file.readlines():
            bigDoubleLayerList.append(item.split(' '))

        return bigDoubleLayerList


    def printingAndWriteFile(self, bigDoubleLayerList):
        print('=====共有' + str(len(bigDoubleLayerList)) + '篇文章=====')
        tempDict = dict()
        count = 0
        for item in bigDoubleLayerList:
            tempDict.update(self.tfidf(item, bigDoubleLayerList))
            count += 1
            if count % 10 == 0: print('已經計算完前' + str(count) +'篇文章的tfidf值')
            # dictionary的update會把新的加入，如果有重複的key，新的value會覆蓋舊的value

        print('=====開始進行排序=====')
        sorted_tempDict = sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True)

        top = 0
        with open(self.writeFile, 'w') as file:
            for item in sorted_tempDict:
                file.write(str(item) + '\n')
                top += 1
                if top == 100: break



    def main(self):
        bigDoubleLayerList = self.readFileAsList()
        self.printingAndWriteFile(bigDoubleLayerList)



if __name__ == '__main__':
    TfidfObj = Tfidf(sys.argv[1], sys.argv[2])
    TfidfObj.main()
