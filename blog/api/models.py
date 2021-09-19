# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
#from django.core.files.storage import FileSystemStorage
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.



class post(models.Model):
    post_id=models.AutoField
    title=models.CharField(max_length=200,blank=False)
    sub_title=models.CharField(max_length=200,blank=True)
    featured_image=models.ImageField(upload_to='images/',blank=True)
    content=RichTextUploadingField()
    tags = TaggableManager()
    date_time=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class newsletter(models.Model):
    title=models.CharField(max_length=200,blank=False)
    content=RichTextUploadingField()
    date_time=models.DateTimeField(auto_now=True)
    published=models.BooleanField(default=False)
    def __str__(self):
        return self.title

class subscriber(models.Model):
    email=models.EmailField(unique=True)
    def __str__(self):
        return self.email

class customUser(models.Model):
    user_id=models.AutoField
    name=models.CharField(max_length=200,blank=False)
    email=models.EmailField(max_length=254,blank=False,unique=True)
    pic=models.URLField(blank=True)
    def __str__(self):
        return self.name

class comment(models.Model):
    sno=models.AutoField
    content=models.TextField(blank=False)
    user=models.ForeignKey(customUser,on_delete=models.CASCADE)
    post=models.ForeignKey(post,on_delete=models.CASCADE)
    parent_comment=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    date_time=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content[0:15]+"... by "+ self.user.name

class like(models.Model):
    like_id=models.AutoField
    user=models.ForeignKey(customUser,on_delete=models.CASCADE)
    post=models.ForeignKey(post,on_delete=models.CASCADE)
    