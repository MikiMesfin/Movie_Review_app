from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Review, UserProfile
from .serializers import MovieSerializer, ReviewSerializer, UserSerializer, UserProfileSerializer
from .permissions import IsOwnerOrReadOnly
from .services import TMDBService

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'created_at']

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter is required'}, status=400)
        
        tmdb_service = TMDBService()
        movies = tmdb_service.search_movies(query)
        
        # Import first 5 movies to our database
        imported_movies = []
        for movie in movies[:5]:
            imported_movie = tmdb_service.import_movie_to_db(movie)
            imported_movies.append(imported_movie)
        
        serializer = self.get_serializer(imported_movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        tmdb_service = TMDBService()
        movies = tmdb_service.get_popular_movies()
        
        imported_movies = []
        for movie in movies[:10]:  # Import top 10 popular movies
            imported_movie = tmdb_service.import_movie_to_db(movie)
            imported_movies.append(imported_movie)
        
        serializer = self.get_serializer(imported_movies, many=True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['movie', 'rating']
    ordering_fields = ['created_at', 'rating']

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        review = self.get_object()
        if request.user in review.likes.all():
            review.likes.remove(request.user)
            return Response({'status': 'unliked'})
        else:
            review.likes.add(request.user)
            return Response({'status': 'liked'}) 

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 