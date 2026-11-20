# Machine Learning Recommendation System

## Dataset

CineMatch includes a small curated sample dataset for immediate local use. It is intentionally small and should not be represented as a statistical benchmark. MovieLens is the recommended source for a larger compatible dataset.

Official MovieLens source: https://grouplens.org/datasets/movielens/

The bundled loader reads `backend/datasets/sample_movies.csv`. It also demonstrates the cleaning and normalization stages used for title, year, rating, genre, director, cast, and keyword fields.

## Content-Based Filtering

Titles, descriptions, genres, directors, cast members, and keywords are normalized into text. `TfidfVectorizer` learns word and phrase weights, and `cosine_similarity` ranks catalog movies against the selected title. A result limit prevents oversized responses.

## Genre Filtering

Genre recommendations count exact genre matches and rank matching titles by match count, vote average, and popularity.

## Popularity

When vote count and rating are available, weighted rating is:

```text
(v / (v + m)) * R + (m / (v + m)) * C
```

where `R` is the movie rating, `v` is its vote count, `C` is the catalog mean rating, and `m` is the 70th percentile of vote counts. This reduces the influence of high ratings based on very few votes.

## Hybrid Ranking

The current implementation combines genre matching and weighted popularity for preference recommendations. Content similarity is used for movie-to-movie recommendations. It does not claim collaborative filtering because the application has no sufficiently established user-item interaction dataset.

## Limitations

- The demo dataset is small.
- TF-IDF has no long-term learning component.
- Recommendations do not yet incorporate all user rating history.
- Image URLs are not required for the recommendation engine.
