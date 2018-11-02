from .models import User, Blog_Articles, FriendShip
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'adder', 'phone', 'birthday')


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blog_Articles
        fields = ('title', 'body', 'create_time', 'author')


class FriendSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FriendShip
        fields =('followed', 'follower', 'create_time')