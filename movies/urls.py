from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'movies', views.MovieViewSet, basename='movie')
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'profiles', views.UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
] 