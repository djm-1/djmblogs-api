from django.urls import path, include
from rest_framework import routers
from .viewsets import *
from . import views
router = routers.DefaultRouter()


router.register('post',PostViewset,'post')
router.register('subscriber',SubscriberViewset)
router.register('customuser',CustomUserViewset)
router.register('comment',CommentViewset,'comment')
router.register('savecomment',SaveCommentViewset,'savecomment')
router.register('usercomment',UserCommentViewset,'usercomment')
router.register('like',LikeViewset)
router.register('popularpost',PopularPostViewset,'popularpost')
router.register('searchpost',SearchPostViewset,'searchpost')


urlpatterns = [
    path('', include(router.urls)),
    path('chart/',views.index,name='admindata'),
    path('send_newsletter/<int:id>/',views.send_newsletter,name='send_newsletter'),
]
