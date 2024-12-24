# Movie Review API

A Django REST API for movie reviews with TMDB integration.

## Features

- User authentication with JWT
- Movie information from TMDB API
- User reviews and ratings
- Like/unlike functionality
- User profiles with avatar support
- API documentation with Swagger


## Technologies
- Django 3.2+
- Django REST Framework
- PostgreSQL
- JWT Authentication
- TMDB API Integration
- Python-dotenv
- Django CORS Headers
- Whitenoise
- Pillow

## Prerequisites
- Python 3.8+
- PostgreSQL
- TMDB API Key

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd movie-review-api
   ```

2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create .env file with:
   ```
   TMDB_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Movies
- `GET /api/movies/` - List all movies
- `GET /api/movies/{id}/` - Get movie details
- `GET /api/movies/search/?q=query` - Search movies from TMDB
- `GET /api/movies/popular/` - Get popular movies from TMDB

### Reviews
- `GET /api/reviews/` - List all reviews
- `POST /api/reviews/` - Create movie review
- `PUT /api/reviews/{id}/` - Update review
- `DELETE /api/reviews/{id}/` - Delete review
- `POST /api/reviews/{id}/like/` - Like/unlike review

### User Profiles
- `GET /api/profiles/` - Get user profile
- `PUT /api/profiles/{id}/` - Update profile
- `PATCH /api/profiles/{id}/` - Partial update profile

## Authentication

All requests (except registration and token endpoints) require JWT token in the header:

## Example Requests

### Get JWT Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Create a Movie Review
```bash
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "movie": 1,
    "content": "Great movie!",
    "rating": 5
  }'
```

### Search Movies
```bash
curl http://localhost:8000/api/movies/search/?q=inception \
  -H "Authorization: Bearer <your_jwt_token>"
```

### Update Profile
```bash
curl -X PATCH http://localhost:8000/api/profiles/1/ \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Movie enthusiast"
  }'
```

## Error Responses

- 400: Bad Request - Invalid input
- 401: Unauthorized - Invalid/missing token
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource doesn't exist
- 500: Server Error - Something went wrong on the server

## Development

- Use `python manage.py test` to run tests
- Follow PEP 8 style guide
- Use black for code formatting
- Create feature branches for new features

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [TMDB](https://www.themoviedb.org/) for providing the movie data API
- Django REST Framework team for the amazing framework
- All contributors to this project
