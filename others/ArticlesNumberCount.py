class articlesNumberCount(object):
    def __init__(self):
        import glob
        self.fileList = glob.glob('./result/*.txt')

    def articleNumbers(self):
        fileToLengthDict = dict()
        for fileName in self.fileList:
            with open(fileName, 'r') as file:
                numLines = sum(1 for line in file)
            fileToLengthDict[fileName] = numLines

        return fileToLengthDict


    def avgArticleLength(self, lenDict):
        import jieba.analyse
        avgDict = dict()
        for fileName in self.fileList: # iterate over 檔案
            with open(fileName, 'r') as file:
                wordcount = 0
                for article in file.readlines():
                    wordcount += len(article)
            avgWordCount = wordcount / float(lenDict[fileName])
            avgDict[fileName] = avgWordCount

        for key, value in avgDict.items():
            print(key + ' 的文章數目為 ' + str(lenDict[key]) + ', 每篇文章的平均字數為 ' + str(value))
        

    def main(self):
        numberDict = self.articleNumbers()
        self.avgArticleLength(numberDict)



if __name__ == '__main__':
    obj = articlesNumberCount()
    obj.main()