import jieba.analyse
import sys

inputFilePath = sys.argv[1]
outputFilePath = sys.argv[2]

with open(inputFilePath, 'r') as file:
    bigAllArticlesList = list()
    for item in file.readlines():
        bigAllArticlesList.append(item)


everyTop5InArticles = list()
for article in bigAllArticlesList:
    articleResultList = jieba.analyse.extract_tags(article, topK=20, withWeight=True, allowPOS=())
    if len(articleResultList) < 5:
        for item in articleResultList:
            if '.' or r'^[0-9]+$' or r'^[a-zA-Z]+$' in item[0]:
                continue
            everyTop5InArticles.append(item)
    else:
        for num in range(0, 5):
            if '.' or r'^[0-9]+$' or r'^[a-zA-Z]+$' in articleResultList[num][0]:
                continue
            everyTop5InArticles.append(articleResultList[num])

print('===已開始排序===')
everyTop5InArticles.sort(key=lambda x: x[1], reverse=True)

# for item in everyTop5InArticles:
#     print(item)

print('>>>已開始寫擋<<<')
with open(outputFilePath, 'w') as file2:
    for i in range(0, 100):
        file2.write(str(everyTop5InArticles[i]) + '\n')

