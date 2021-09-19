from rest_framework import serializers
from .models import post,subscriber,customUser,comment,like
from taggit.serializers import (TagListSerializerField,TaggitSerializer)

class PostSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model=post
        fields='__all__'

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model=subscriber
        fields='__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=customUser
        fields='__all__'

class CustomUserSerializerAlt(serializers.ModelSerializer):
    class Meta:
        model=customUser
        fields=['id','name','pic']

class CommentSerializer(serializers.ModelSerializer):
    user=CustomUserSerializerAlt()
    class Meta:
        model=comment
        fields='__all__'


# will modify it
class SaveCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=comment
        fields='__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=like
        fields='__all__'