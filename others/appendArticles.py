import glob

def main():
    lineCount = 0
    totalCount = 0
    articleInfo = dict()
    fileList = glob.glob('./result/*.txt')

    with open('./AllArticles.txt', 'a') as wf:
        for item in fileList:
            lineCount = 0
            with open(item, 'r') as rf:
                for line in rf.readlines():
                    wf.write(line)
                    lineCount += 1
                    totalCount += 1
            articleInfo[item] = lineCount

    print('=== 寫檔完畢 ===')
    for key, value in articleInfo.items():
        print(key + ' 有 ' + str(value) + ' 篇文章')

    print('==> 總共有 ' + str(totalCount) + ' 篇文章 <==')



if __name__ == '__main__':
    main()

"""
./result/Breakfast.txt 有 5927 篇文章
./result/Vegetarian.txt 有 1110 篇文章
./result/ThemeRestaurant.txt 有 12642 篇文章
./result/FastFood.txt 有 4233 篇文章
./result/ChineseCuisine.txt 有 14783 篇文章
./result/Buffet.txt 有 2468 篇文章
./result/Barbecue.txt 有 10731 篇文章
./result/WesternCuisine.txt 有 11776 篇文章
./result/Snack.txt 有 15106 篇文章
./result/Bake.txt 有 15314 篇文章
./result/SweetSoup.txt 有 12408 篇文章
./result/Cafe.txt 有 14544 篇文章
./result/AsianCuisine.txt 有 5832 篇文章
./result/Hotpot.txt 有 19131 篇文章
./result/JapaneseCuisine.txt 有 10835 篇文章
==> 總共有 156840 篇文章 <==

"""