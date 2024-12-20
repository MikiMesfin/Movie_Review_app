from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Review, UserProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class MovieSerializer(serializers.ModelSerializer):
    poster_url = serializers.CharField(read_only=True)
    
    class Meta:
        model = Movie
        fields = ('id', 'title', 'tmdb_id', 'overview', 'poster_url', 
                 'release_date', 'created_at', 'updated_at')

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'movie', 'user', 'content', 'rating', 'created_at', 'likes_count')

    def get_likes_count(self, obj):
        return obj.likes.count()

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'reviews_count')

    def get_reviews_count(self, obj):
        return obj.user.reviews.count() 