from django.shortcuts import render,HttpResponse
from django.views.generic import View
import time
import json
import requests

class IndexView(View):
    def get(self,request):
        return render(request, 'index.html')
    def post(self,request):
        b = request.POST.get('k','')
        k = json.loads(b)
        for i in k:
            print(i)

        return HttpResponse('{"status":"1","msg":"添加成功"}', content_type='application/json')



def music_get_link(request):
    if request.method == "GET":
        song_id = int(request.GET.get("id"))
        filehash = request.GET.get("filehash")
        temp_url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=%s&album_id=%s" % (filehash, song_id)
        print(temp_url)
        try:
            song_item = requests.get(temp_url).json().get("data")
            data = {"album_id": song_item["album_id"], "timelength": song_item["timelength"], "lyrics": song_item["lyrics"],
                    "audio_name": song_item["audio_name"], "play_url": song_item["play_url"], "img": song_item["img"]}
            return HttpResponse(json.dumps({"err": 0, "music_objs": data}), content_type='application/json')
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({"err": -1, "msg": "error:%e" % e}), content_type='application/json')



def music_search_view(request):
    song_name = request.GET.get("song_name")
    page_no = request.GET.get("page_no", 1)
    page_size = request.GET.get("page_size", 10)
    results = []
    count = 0
    url1 = "http://songsearch.kugou.com/song_search_v2"
    param = {"keyword": song_name, "page": page_no, "pagesize": page_size,'clientver':'','platform':'WebFilter'}
    ret = requests.get(url1, params = param)
    try:
        count = ret.json()["data"]["total"]
        ret = ret.json()["data"]["lists"]
    except Exception as e:
        return HttpResponse(json.dumps({"err": -1, "msg": "没有找到相关歌曲信息"}), content_type='application/json')
    for item in ret:
        duration = "%02d'%02ds" % (item["Duration"]/60,item["Duration"]%60)
        results.append({"SongName": item["SongName"], "SingerName": item["SingerName"], "Duration": duration,
                        "FileSize": "%.2fM" % (item["FileSize"]/(1024*1024)), "ID": item["ID"], "FileHash": item["FileHash"]})
    return HttpResponse(json.dumps({"err": 0, "music_objs": results, "count": count}), content_type='application/json')
