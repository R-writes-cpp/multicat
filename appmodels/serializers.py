from rest_framework import serializers
from appmodels.models import User, Creator, Release, Rating, Connection, DescriptorVote

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'

class ReleaseSerializer(serializers.ModelSerializer):
    creator_primary = CreatorSerializer()
    creator_secondary = CreatorSerializer()

    class Meta:
        model = Release
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    release = ReleaseSerializer()
    user = UserSerializer()

    class Meta:
        model = Rating
        fields = '__all__'

class DescriptorVoteSerializer(serializers.ModelSerializer):
    release = ReleaseSerializer()
    user = UserSerializer()

    class Meta:
        model = DescriptorVote
        fields = '__all__'

class ConnectionSerializer(serializers.Serializer):
    follower = UserSerializer()
    followee = UserSerializer()

    class Meta:
        model = Connection
        fields = '__all__'
