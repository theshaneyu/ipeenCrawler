import jieba.analyse
import sys, re

inputFilePath = sys.argv[1]
outputFilePath = sys.argv[2]

with open(inputFilePath, 'r') as file:
    bigAllArticlesList = list()
    for item in file.readlines():
        bigAllArticlesList.append(item)

# 結巴分析與斷詞過程已經有濾掉stopwords，只是有些還出現在文本裡
stopwords = ['我們', '他們', '這裡', '真的', '這次', '其實', '非常', '這麼', '什麼', '可以', '不過', '雖然', '還是', '還有', '沒有', '不會', '有點', '這道', '這個', '這是', '裡面', '時候', '因為', '一整', '整個', '相當', '應該', '還蠻']

everyTop5InArticles = list()
for article in bigAllArticlesList:
    articleResultList = jieba.analyse.extract_tags(article, topK=20, withWeight=True, allowPOS=())
    appendCount = 0
    for item in articleResultList:
        if item[0] in stopwords: break
        
        item = list(item)
        string = re.match(u"[\u4e00-\u9fa5]+", item[0])
        if string:
            exist = False
            if len(everyTop5InArticles) == 0:
                everyTop5InArticles.append(item)
            else:
                for result in everyTop5InArticles:
                    if result[0] == item[0]:
                        exist = True
                        result[1] += 0.5 # 如果出現重複，就把它的值提昇
                        break
                if exist == False:
                    everyTop5InArticles.append(item)
        else:
            appendCount = appendCount - 1
            continue

        appendCount += 1
        if appendCount > 10: break


print('===已開始排序everyTop5InArticles===')
everyTop5InArticles.sort(key=lambda x: x[1], reverse=True)

# for item in everyTop5InArticles:
#     print(item)

print('>>>已開始寫擋<<<')
with open(outputFilePath, 'w') as file2:
    for i in range(0, 100):
        file2.write(str(everyTop5InArticles[i]) + '\n')

