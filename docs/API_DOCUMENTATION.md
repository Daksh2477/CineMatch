# API Documentation

Interactive documentation is available at `/api/docs/` when the Django server is running.

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/movies/` | GET | Paginated search and filtering |
| `/api/movies/{id}/` | GET | Movie detail |
| `/api/movies/search/?q=text` | GET | Search movies |
| `/api/movies/popular/` | GET | Popular movies |
| `/api/genres/` | GET | Genre list |
| `/api/recommendations/movie/{id}/` | GET | Content-based recommendations |
| `/api/recommendations/preferences/` | POST | Genre preference recommendations |
| `/api/watchlist/` | GET, POST | Read or add authenticated watchlist items |
| `/api/watchlist/{id}/` | DELETE | Remove a watchlist item |
| `/api/ratings/` | GET, POST | Read or add an authenticated 1–10 rating |
| `/api/history/` | GET | Authenticated recommendation history |
| `/api/auth/register/` | POST | Register a username, email, and password |
| `/api/auth/token/` | POST | Obtain JWT access and refresh tokens |
| `/api/auth/token/refresh/` | POST | Refresh an access token |

Movie list filtering supports `q`, `genre`, `year`, `rating`, and `ordering`.
