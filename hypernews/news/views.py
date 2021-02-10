from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
import json
from django.conf import settings
from datetime import datetime
from django.shortcuts import redirect


class ComingSoon(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Coming soon")

    def redirect_view(self):
        return HttpResponseRedirect("news/")


class MainView(View):
    def get(self, request, *args, **kwargs):

        with open(settings.NEWS_JSON_PATH) as jsonFile:
            articleList = json.load(jsonFile)

        articleList.sort(key= lambda i: i["created"], reverse=True)

        for i in range(len(articleList)):
            articleList[i]["created"] = articleList[i]["created"][:10]

        q = request.GET.get('q')
        if q:
            articleList = filter(lambda x: q in x['title'], articleList)

        articleDict = {}
        for article in articleList:
            if article['created'] in articleDict:
                articleDict[article['created']].append(article)
            else:
                articleDict[article['created']] = [article]

        return render(request, "news/Main_Page.html", context={
                'articleDict': articleDict
            })


class NewsView(View):
    def get(self, request, link, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as jsonFile:
            articleList = json.load(jsonFile)

        linkedArticle = None
        for article in articleList:
            if article['link'] == int(link):
                linkedArticle = article
                break

        if linkedArticle:
            return render(request, "news/index.html", context={
                'article': linkedArticle
            })
        else:
            raise Http404


class CreateView(View):
    def post(self, request, *args, **kwargs):

        with open(settings.NEWS_JSON_PATH) as jsonFile:
            articleList = json.load(jsonFile)

        article = {
            'created': str(datetime.now().replace(microsecond=0)),
            'text': request.POST.get('text'),
            'title': request.POST.get('title'),
            'link': hash(datetime.now())
        }

        articleList.append(article)

        with open(settings.NEWS_JSON_PATH, 'w') as jsonFile:
            json.dump(articleList, jsonFile)

        return redirect('/news/')

    def get(self, request):
        return render(request, "news/create.html", context={})
