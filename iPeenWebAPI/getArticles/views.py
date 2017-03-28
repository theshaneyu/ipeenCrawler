from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from TopCosineSimilarity.TopCosineSimilarity import GetTopResult
# Create your views here.

def get(request):
    obj = GetTopResult('./TopCosineSimilarity/med250.model.bin', 'mongodb://140.120.13.244:7777/')
    termStr = request.GET['term']
    termList = termStr.split()
    print(termList)
    returnDict = obj.getArticle(termList)
    Top20Str = ''
    for item in returnDict['Top20']:
        Top20Str += (item + ' / ')

    # returnStr = returnDict['Content'] + '{Top20 keywords : [' + Top20Str + ']}'
    # print(type(termStr)) # <class 'str'>
    # return JsonResponse(returnDict, safe = False)
    # return HttpResponse('%s' % returnStr)
    # return HttpResponse('%s' % returnDict['Content'])
    return HttpResponse('<p><strong> 文章內容 </strong></p>'
                        '<p>' + returnDict['Content'] + '</p>'
                        '<p><strong> 前20關鍵字 </strong></p>'
                        '<p>' + Top20Str + '</p>')