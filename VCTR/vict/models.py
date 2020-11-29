from django.db import models

# Create your models here.
class Gift(models.Model):
    Time_id= models.AutoField
    Name = models.CharField(max_length=50,default='')
    StartTime = models.IntegerField(default=0)
    EndTime = models.IntegerField(default=0)
    def __str__(self) :
        return self.Name