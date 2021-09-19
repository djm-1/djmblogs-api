from django.contrib import admin
from .models import post,newsletter,subscriber,customUser,comment,like
# Register your models here.
admin.site.register(post)
admin.site.register(newsletter)
admin.site.register(subscriber)
admin.site.register(customUser)
admin.site.register(comment)
admin.site.register(like)