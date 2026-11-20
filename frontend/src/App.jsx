import { useCallback, useEffect, useMemo, useState } from 'react'
import { Bookmark, Film, Heart, Search, Star, X } from 'lucide-react'
import './App.css'

const API = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

async function api(path, options = {}) {
  const token = localStorage.getItem('cinematch_token')
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) }
  if (token) headers.Authorization = `Bearer ${token}`
  const response = await fetch(`${API}${path}`, { ...options, headers })
  if (!response.ok) throw new Error(`Request failed (${response.status})`)
  return response.status === 204 ? null : response.json()
}

const fallbackPoster = '/poster-fallback.svg'

function getPoster(movie) {
  return movie?.poster_url || fallbackPoster
}

function MovieCard({ movie, onOpen, onWatchlist }) {
  return (
    <article className="movie-card">
      <button className="poster-button" onClick={() => onOpen(movie)} aria-label={`View ${movie.title}`}>
        <img src={getPoster(movie)} alt={`${movie.title} poster`} onError={(event) => { event.currentTarget.onerror = null; event.currentTarget.src = fallbackPoster }} />
        <span className="rating-chip"><Star size={14} fill="currentColor" /> {movie.vote_average?.toFixed(1) || 'N/A'}</span>
      </button>
      <div className="card-copy">
        <button className="title-button" onClick={() => onOpen(movie)}>{movie.title}</button>
        <p>{movie.release_year} · {movie.genres?.slice(0, 2).map((genre) => genre.name).join(', ')}</p>
        <button className="icon-action" onClick={() => onWatchlist(movie)} aria-label={`Add ${movie.title} to watchlist`}><Bookmark size={18} /></button>
      </div>
    </article>
  )
}

function App() {
  const [section, setSection] = useState('home')
  const [movies, setMovies] = useState([])
  const [genres, setGenres] = useState([])
  const [similar, setSimilar] = useState([])
  const [watchlist, setWatchlist] = useState([])
  const [selected, setSelected] = useState(null)
  const [recommendationSource, setRecommendationSource] = useState(null)
  const [query, setQuery] = useState('')
  const [genreFilter, setGenreFilter] = useState('')
  const [yearFilter, setYearFilter] = useState('')
  const [ratingFilter, setRatingFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadMovies = useCallback(async (filters = {}) => {
    setLoading(true)
    setError('')
    try {
      const params = new URLSearchParams()
      const nextGenre = filters.genre ?? genreFilter
      const nextYear = filters.year ?? yearFilter
      const nextRating = filters.rating ?? ratingFilter
      if (nextGenre) params.set('genre', nextGenre)
      if (nextYear) params.set('year', nextYear)
      if (nextRating) params.set('rating', nextRating)
      const data = await api(`/movies/?${params}`)
      setMovies(Array.isArray(data) ? data : data.results || [])
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }, [genreFilter, yearFilter, ratingFilter])

  useEffect(() => {
    Promise.all([api('/genres/'), api('/movies/popular/')])
      .then(([genreData, movieData]) => {
        setGenres(Array.isArray(genreData) ? genreData : genreData.results || [])
        setMovies(movieData)
      })
      .catch((requestError) => setError(requestError.message))
      .finally(() => setLoading(false))
  }, [])

  const filteredMovies = useMemo(() => {
    if (!query.trim()) return movies
    const normalized = query.trim().toLowerCase()
    return movies.filter((movie) =>
      movie.title.toLowerCase().includes(normalized)
      || movie.description?.toLowerCase().includes(normalized)
    )
  }, [movies, query])

  const openMovie = async (movie) => {
    setSelected(movie)
    setSimilar([])
    try {
      const recommendations = await api(`/recommendations/movie/${movie.id}/`)
      setSimilar(recommendations)
    } catch {
      setSimilar([])
    }
  }

  const selectRecommendationMovie = async (movie) => {
    setSelected(null)
    setRecommendationSource(movie)
    setSimilar([])
    try {
      const recommendations = await api(`/recommendations/movie/${movie.id}/`)
      setSimilar(recommendations)
    } catch {
      setSimilar([])
    }
  }

  const addToWatchlist = async (movie) => {
    if (!localStorage.getItem('cinematch_token')) {
      setError('Sign in to save movies to your watchlist.')
      setSection('watchlist')
      return
    }
    try {
      await api('/watchlist/', { method: 'POST', body: JSON.stringify({ movie_id: movie.id }) })
      setWatchlist((current) => current.some((item) => item.movie.id === movie.id)
        ? current
        : [...current, { id: Date.now(), movie }])
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  const loadWatchlist = async () => {
    setSection('watchlist')
    if (!localStorage.getItem('cinematch_token')) return
    try {
      const data = await api('/watchlist/')
      setWatchlist(Array.isArray(data) ? data : data.results || [])
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  const signIn = async () => {
    const username = window.prompt('Username')
    if (!username) return
    const password = window.prompt('Password')
    if (!password) return
    try {
      const data = await api('/auth/token/', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      })
      localStorage.setItem('cinematch_token', data.access)
      localStorage.setItem('cinematch_username', username)
      setError('')
      loadWatchlist()
    } catch {
      setError('Sign-in failed. Check your username and password.')
    }
  }

  const removeWatchlist = async (item) => {
    try {
      await api(`/watchlist/${item.id}/`, { method: 'DELETE' })
      setWatchlist((current) => current.filter((entry) => entry.id !== item.id))
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <button className="brand" onClick={() => setSection('home')}><Film size={24} /> CineMatch</button>
        <nav aria-label="Primary navigation">
          <button className={section === 'home' ? 'active' : ''} onClick={() => setSection('home')}>Home</button>
          <button className={section === 'discover' ? 'active' : ''} onClick={() => { setSection('discover'); loadMovies() }}>Discover</button>
          <button className={section === 'recommendations' ? 'active' : ''} onClick={() => setSection('recommendations')}>Recommendations</button>
          <button className={section === 'watchlist' ? 'active' : ''} onClick={loadWatchlist}>Watchlist</button>
        </nav>
        <button className="sign-in" onClick={signIn}>{localStorage.getItem('cinematch_username') || 'Sign in'}</button>
      </header>

      {error && <div className="notice" role="alert">{error}<button onClick={() => setError('')}><X size={16} /></button></div>}

      <main>
        {section === 'home' && (
          <>
            <section className="hero">
              <div>
                <span className="eyebrow">Your next favorite story</span>
                <h1>Discover films that match your taste.</h1>
                <p>Search the catalog, explore genres, and find thoughtful recommendations powered by movie metadata.</p>
                <button className="primary" onClick={() => { setSection('discover'); loadMovies() }}>Explore movies</button>
              </div>
              <div className="hero-feature">
                {movies[0] && <img src={getPoster(movies[0])} alt={`${movies[0].title} featured artwork`} onError={(event) => { event.currentTarget.onerror = null; event.currentTarget.src = fallbackPoster }} />}
              </div>
            </section>
            <section className="content-section">
              <div className="section-heading"><div><span>Now popular</span><h2>Popular movies</h2></div></div>
              {loading ? <div className="grid skeleton-grid">{[1,2,3,4].map((n) => <div className="skeleton" key={n} />)}</div> : (
                <div className="movie-grid">{movies.slice(0, 8).map((movie) => <MovieCard key={movie.id} movie={movie} onOpen={openMovie} onWatchlist={addToWatchlist} />)}</div>
              )}
            </section>
            <section className="genre-strip">
              {genres.map((genre) => <button key={genre.id} onClick={() => { setGenreFilter(genre.slug); setSection('discover'); loadMovies({ genre: genre.slug }) }}>{genre.name}</button>)}
            </section>
          </>
        )}

        {section === 'discover' && (
          <section className="content-section">
            <div className="discover-header">
              <div><span>Explore</span><h1>Discover movies</h1></div>
              <label className="search-box"><Search size={18} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search title or description" /></label>
            </div>
            <div className="filters">
              <select value={genreFilter} onChange={(event) => { setGenreFilter(event.target.value); loadMovies({ genre: event.target.value }) }}><option value="">All genres</option>{genres.map((genre) => <option value={genre.slug} key={genre.id}>{genre.name}</option>)}</select>
              <select value={yearFilter} onChange={(event) => { setYearFilter(event.target.value); loadMovies({ year: event.target.value }) }}><option value="">All years</option>{[2022,2021,2018,2017,2016,2015,2014,2010,2008,2004,1995].map((year) => <option value={year} key={year}>{year}</option>)}</select>
              <select value={ratingFilter} onChange={(event) => { setRatingFilter(event.target.value); loadMovies({ rating: event.target.value }) }}><option value="">Any rating</option>{[9,8,7].map((rating) => <option value={rating} key={rating}>{rating}+ rating</option>)}</select>
            </div>
            {loading ? <div className="movie-grid">{[1,2,3,4,5,6].map((n) => <div className="skeleton" key={n} />)}</div> : filteredMovies.length ? (
              <div className="movie-grid">{filteredMovies.map((movie) => <MovieCard key={movie.id} movie={movie} onOpen={openMovie} onWatchlist={addToWatchlist} />)}</div>
            ) : <div className="empty-state"><Film size={36} /><h2>No movies found</h2><p>Try changing a filter or search term.</p></div>}
          </section>
        )}

        {section === 'recommendations' && (
          <section className="content-section">
            <div className="section-heading"><div><span>For you</span><h1>Recommendation finder</h1></div></div>
            <div className="recommendation-panel">
              <label><span>Choose a movie</span><select onChange={(event) => { const movie = movies.find((item) => item.id === Number(event.target.value)); if (movie) selectRecommendationMovie(movie) }}><option value="">Select a movie</option>{movies.map((movie) => <option value={movie.id} key={movie.id}>{movie.title}</option>)}</select></label>
              {recommendationSource && <p>Because you selected <strong>{recommendationSource.title}</strong>, CineMatch compares genres, descriptions, directors, cast, and keywords using TF-IDF and cosine similarity.</p>}
            </div>
            {similar.length ? <div className="movie-grid">{similar.map((movie) => <MovieCard key={movie.id} movie={movie} onOpen={openMovie} onWatchlist={addToWatchlist} />)}</div> : <div className="empty-state"><Heart size={36} /><h2>Select a movie</h2><p>Similar titles will appear here.</p></div>}
          </section>
        )}

        {section === 'watchlist' && (
          <section className="content-section">
            <div className="section-heading"><div><span>Saved</span><h1>My watchlist</h1></div></div>
            {!localStorage.getItem('cinematch_token') ? <div className="empty-state"><Bookmark size={36} /><h2>Sign in to save movies</h2><p>Your watchlist is stored with your account.</p><button className="primary" onClick={signIn}>Sign in</button></div> : watchlist.length ? (
              <div className="movie-grid">{watchlist.map((item) => <div className="watchlist-card" key={item.id}><MovieCard movie={item.movie} onOpen={openMovie} onWatchlist={addToWatchlist} /><button className="remove-button" onClick={() => removeWatchlist(item)}>Remove</button></div>)}</div>
            ) : <div className="empty-state"><Bookmark size={36} /><h2>Your watchlist is empty</h2><p>Save a movie to see it here.</p></div>}
          </section>
        )}
      </main>

      {selected && (
        <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) setSelected(null) }}>
          <article className="detail-modal" role="dialog" aria-modal="true" aria-label={selected.title}>
            <button className="modal-close" onClick={() => setSelected(null)} aria-label="Close"><X /></button>
            <img src={getPoster(selected)} alt={`${selected.title} poster`} onError={(event) => { event.currentTarget.onerror = null; event.currentTarget.src = fallbackPoster }} />
            <div>
              <span className="eyebrow">{selected.release_year} · {selected.runtime ? `${selected.runtime} min` : 'Runtime unavailable'}</span>
              <h2>{selected.title}</h2>
              <p>{selected.description}</p>
              <div className="modal-meta"><span><Star size={16} fill="currentColor" /> {selected.vote_average}</span><span>{selected.genres?.map((genre) => genre.name).join(' · ')}</span></div>
              <button className="primary" onClick={() => addToWatchlist(selected)}><Bookmark size={18} /> Add to watchlist</button>
            </div>
          </article>
        </div>
      )}
    </div>
  )
}

export default App
