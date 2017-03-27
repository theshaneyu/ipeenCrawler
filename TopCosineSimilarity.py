import numpy as np
from gensim import models


class GetTopResult(object):
    def __init__(self, modelPath, uri):
        from pymongo import MongoClient
        self.client = MongoClient(uri)
        self.db = self.client['iPeen']
        self.coll = self.db['ipeenArticleInfo']
        self.modelPath = modelPath


    def getArticle(self, inputTermList):
        model = models.KeyedVectors.load_word2vec_format(self.modelPath, binary=True)
        uninitialized = True
        for item in inputTermList:
            try:
                if uninitialized:
                    sumVec = model[item]
                    uninitialized = False
                else:
                    sumVec += model[item]
            except:
                continue
        # 至此已經得到使用者Query的所有Term的加總向量，為sumVec
        # self.getMostSimilar(sumVec)
        ID = self.getMostSimilar(sumVec)
        resultArticle = self.coll.find({'ID':ID})
        # print(type(resultArticle[0])) # <class 'dict'>
        return resultArticle[0]




    def getMostSimilar(self, queryVec):
        allVectors = self.coll.find({}, {'Vector':True, 'ID':True, '_id':False})
        topCosineSimilarity = 0.0
        for vector in allVectors:
            array = np.array(vector['Vector']) # 資料庫裡的Vector欄位，當初是以.tolist()存進json，則拿出來要這樣復原
            cosineSimilarity = np.dot(queryVec, array)/(np.linalg.norm(queryVec) * np.linalg.norm(array))
        # print(topCosineSimilarity)
            if cosineSimilarity > topCosineSimilarity:
                topCosineSimilarity = cosineSimilarity
                topResultID = vector['ID']
        # print(type(topResultID))
        return topResultID


    def testMongo(self):
        result = self.coll.find({}, {'Vector':1, 'ID':True, '_id':False})
        for item in result:
            array = np.array(item['Vector'])
            print(item)


    def main(self):
        self.testMongo()



if __name__ == '__main__':
    import sys
    queryList = list()
    for item in sys.argv:
        if item == sys.argv[0]: continue
        queryList.append(item)

    obj = GetTopResult('./med250.model.bin', 'mongodb://140.120.13.244:7777/')
    print(obj.getArticle(queryList)['Content'])
    # obj.main()


