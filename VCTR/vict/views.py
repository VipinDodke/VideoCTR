from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests
from .models import Gift ,Clip,Contect
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
        sd =int( request.POST.get('nam', ''))
        ed = int(request.POST.get('dscr', ''))
        k='j'
        link = f'https://www.youtube.com/watch?v={y}'
        yt = YouTube(link)
        title = yt.title
        print(title)
        pl = yt.streams.first()
        path=pl.download("media/vict/PY_video")
        k = "downloaded"
        if k == "downloaded":
            print(path)
            file = VideoFileClip(path)
            new = file.subclip(t_start=sd, t_end=ed)
            gift = Gift(Name=name, Pytube_Video=path)
            gift.save()
            gift = Clip(Name=name,Moviepy_Video=new.write_videofile(f"media/vict/PY_video/Mov_video/YOUTUBE_CUTTER_{title}.mp4"))
            gift.save()
    context = {'myvalue': y}
    return render(request, 'vict/gift.html',context)

def view(request,myid):
    p=myid
    print(p)
    context = {'myvalue':p}
    k='j'
    link = f'https://www.youtube.com/watch?v={p}'
    yt = YouTube(link)
    name=yt.title
    poster= yt.thumbnail_url
    #pl = yt.streams.first()
    context = {'name':name,'link':link,'poster':poster}
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


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        call = request.POST.get('call', '')
        desc = request.POST.get('desc','')
        contect = Contect(Name=name, Email=email, Call=call, desc=desc)
        contect.save()
    return render(request, 'vict/contact.html')