from django.db import models
from django.contrib.auth.models import models
# Create your models here.
class Gift(models.Model):
    Time_id= models.AutoField
    Name = models.CharField(max_length=50,default='')
    Pytube_Video = models.FileField(upload_to="media/vict/PY_video/",default='')
    def __str__(self) :
        return (self.Name)

class Clip(models.Model):
    Time_id= models.AutoField
    Name = models.CharField(max_length=10, default='Converted')
    Moviepy_Video = models.FileField(upload_to="media/vict/PY_video/Mov_video/", default='')
    def __str__(self) :
        return (self.Name)