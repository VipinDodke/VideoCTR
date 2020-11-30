from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests
from .models import Gift
from isodate import parse_duration
from moviepy.editor import VideoFileClip, AudioFileClip
from pytube import YouTube
# from moviepy.editor import ImageClip,CompositeVideoClip
#YouTube('https://www.youtube.com/watch?v=HO7CRp44s10').streams.first().download()

viwes=[]
def index(request):
    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part': 'snippet',
            'q': request.POST.get('search', False),
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 15,
            'type': 'video',
        }
        video_Ids = []
        r = requests.get(search_url,params=search_params)
        results = r.json()['items']
        for result in results:
            video_Ids.append(result['id']['videoId'])
        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'contentDetails,snippet',
            'id': ','.join(video_Ids),
            'maxResults': 15,
        }
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
            }
            videos.append(video_data)
            global viwes
            viwes.append(video_data)

    context = {
        'videos': videos,
    }

    return render(request, 'vict/index.html', context, )

def gift(request,mid):
    y=mid
    print(y)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        sd = request.POST.get('nam', '')
        ed = request.POST.get('dscr', '')
        gift= Gift(StartTime=sd,EndTime=ed)
        gift.save()
        k='j'
        link = f'https://www.youtube.com/watch?v={y}'
        yt = YouTube(link)
        pl = yt.streams.first()
        path=pl.download(f"E:/mm/pytube/")
        k = "downloaded"
        if k == "downloaded":
            print(path)
            file = VideoFileClip(path)
            new = file.subclip(t_start=sd, t_end=ed)
            new.write_videofile(fr"E:\mm\moviepy\converte.mp4")
    context = {'myvalue': y}

    return render(request, 'vict/gift.html',context)

def view(request,myid):
    i=myid
    s=myid
    context = {'myvalue': i}
    global dic
    for bar in viwes:
        x=bar.values()
        for o in bar.values():
          if i==o:
              dic = bar
    last=Gift.objects.last()

    # k='j'
    # link = f'https://www.youtube.com/watch?v={i}'
    # yt = YouTube(link)
    # pl = yt.streams.first()
    # path=pl.download(f"E:/mm/pytube/")
    # k = "downloaded"
    # if k == "downloaded":
    #     print(path)
    #     file = VideoFileClip(path)
    #     new = file.subclip(t_start=last.StartTime, t_end=last.EndTime)
    #     new.write_videofile(fr"E:\mm\moviepy\converte.mp4")
    # if request.method == 'POST':
    #     print(request.POST)
    #     sd = request.POST.get('stime', '')
    #     ed = request.POST.get('etime', '')
    #     back(sd,ed)
    return render(request,'vict/view.html',context)
