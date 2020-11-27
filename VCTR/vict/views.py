from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests
from isodate import parse_duration
from moviepy.editor import VideoFileClip, AudioFileClip
from pytube import YouTube

#YouTube('https://www.youtube.com/watch?v=HO7CRp44s10').streams.first().download()
b=0;
viwes=[]
def index(request):
    videos = []
    #



    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part':'snippet',
            'q': request.POST.get('search', False),
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 15,
            'type': 'video',
        }
        video_Ids= []
        r = requests.get(search_url,params=search_params)
        results= r.json()['items']
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
            video_data ={
                'title': result['snippet']['title'],
                'id': result['id'],
                'url' : f'https://www.youtube.com/watch?v={result["id"]}',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
            }
            videos.append(video_data)
            global viwes
            viwes.append(video_data)

    context={
        'videos': videos,
    }

    return render(request,'vict/index.html',context,)

def view(request,myid):
    i=myid
    print(i)
    context = {
        'myvalue': i
    }
    return render(request,'vict/view.html',context)
    #'''link = f'https://www.youtube.com/embed/{i}'
    #yt = YouTube(link)
    #vid = yt.streams.all()
    #st_num= int(input("Enter the size"))
    #pl = vid[st_num-1]
    #pl.download(f'C:/Users/NITESH/PycharmProjects/vv/VideoCTR/VCTR/vict/static/vict/{i}.mp4')
    #k="downloaded"
    #print(k)
    #l=1
    #if k=="downloaded":
     #   path = fr'C:/Users/NITESH/PycharmProjects/vv/VideoCTR/VCTR/vict/static/vict/{i}.mp4'
      #  file = VideoFileClip(path)
       # new = file.subclip(t_start=6, t_end=16)
        #new.write_videofile(fr'E:\working drc\New folder\Play__{i}.mp4')

    #'''