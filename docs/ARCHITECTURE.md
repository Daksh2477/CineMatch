# Architecture

CineMatch uses a simple monorepo architecture:

- React and Vite provide the responsive client.
- Django REST Framework exposes JSON APIs.
- SQLite provides local persistence through the Django ORM.
- A separate recommendation engine uses scikit-learn, Pandas-ready preprocessing utilities, TF-IDF, and cosine similarity.
- JWT authentication protects watchlist, rating, and history operations.

The frontend communicates through `fetch` and the `VITE_API_BASE_URL` environment variable. Django domain apps are isolated into `movies`, `recommendations`, `users`, and `watchlist`.
