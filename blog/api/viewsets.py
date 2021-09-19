from .serializers import *
from rest_framework import viewsets,response,status
from .models import post,subscriber,customUser,comment,like
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.db.models import Count



class PostViewset(viewsets.ModelViewSet):
    queryset = post.objects.all().order_by('-date_time')
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','title','tags__name','date_time']
    http_method_names = ['get','head']

class SearchPostViewset(viewsets.ModelViewSet):

    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','title','tags__name','date_time']
    http_method_names = ['get','head']

    def get_queryset(self):
        query=self.request.GET['search']
        print(query)
        results=post.objects.all()
        title_match=results.filter(title__icontains=query)
        sub_title_match=results.filter(sub_title__icontains=query)
        content_match=results.filter(content__icontains=query)
        posts=title_match.union(content_match)
        posts=posts.union(sub_title_match).order_by('-date_time')
        return posts

class PopularPostViewset(viewsets.ModelViewSet):
    #queryset = post.objects.all().order_by('like__post')
    queryset=post.objects.annotate(num_likes=Count('like')).order_by('-num_likes','-date_time')
    likeobj=like.objects.all().order_by
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','title','tags__name','date_time']
    http_method_names = ['get','head']


class SubscriberViewset(viewsets.ModelViewSet):
    queryset=subscriber.objects.all()
    serializer_class = SubscriberSerializer
    http_method_names = ['post','get','head','delete']

    def list(self, request):
        if 'email' in request.GET:
            sub=subscriber.objects.filter(email=request.GET['email'])
            if sub.count()!=0:
                is_sub=True
                return Response({'is_sub':True,'sub_id':sub[0].id})
        return Response({'is_sub':False})

class CustomUserViewset(viewsets.ModelViewSet):
    queryset=customUser.objects.all()
    serializer_class=CustomUserSerializer
    http_method_names = ['post']

class CommentViewset(viewsets.ModelViewSet):
    queryset=comment.objects.all().order_by('-date_time')
    serializer_class=CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['post']

class UserCommentViewset(viewsets.ModelViewSet):
    #queryset=comment.objects.all().order_by('-date_time')
    serializer_class=CommentSerializer
    
    def list(self, request):
        if 'email' in request.GET:
            email=request.GET['email']
            user=customUser.objects.get(email=email)
            comms=comment.objects.filter(user=user.id)
            return Response(comms.count())


class SaveCommentViewset(viewsets.ModelViewSet):
    queryset=comment.objects.all()
    serializer_class = SaveCommentSerializer

    def create(self, request):
        user=customUser.objects.get(email=request.data['user_email'])
        request.data['user']=user.id
        print(request.data)
        return super().create(request)
        

class LikeViewset(viewsets.ModelViewSet):
    queryset=like.objects.all()
    serializer_class=LikeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields ='__all__'
    http_method_names = ['post', 'head','delete','get']


    def create(self, request):
        user=customUser.objects.get(email=request.data['user_email'])
        request.data['user']=user.id
        #print(request.data)
        return super().create(request)

    def list(self, request):
        data=request.GET
        email=''
        post_id=''
        if 'user' in data:
            email=data['user']
        if 'post' in data:
            post_id=data['post']
        if email!='' and post_id!='':
            user=customUser.objects.get(email=email)
            liked=like.objects.filter(post=post_id,user=user.id)    
            if liked.count()==0:
                return Response({'val':False})
            else:
                return Response({'val':True,'id':liked[0].id})
        elif email=='' and post_id!='':
            return super().list(request)
        elif email!='' and post_id=='':
            user=customUser.objects.get(email=email)
            liked=like.objects.filter(user=user.id)
            data_list=[]
            for lik in liked:
                serializer=LikeSerializer(lik)
                data_list.append(serializer.data)
            return Response(data_list)
        else:
            return super().list(request)
        