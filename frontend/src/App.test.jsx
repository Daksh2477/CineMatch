import '@testing-library/jest-dom/vitest'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import App from './App'


describe('CineMatch App', () => {
  it('renders navigation and switches to Discover', async () => {
    vi.stubGlobal('fetch', vi.fn(async (url) => {
      if (String(url).includes('/genres/')) {
        return { ok: true, status: 200, json: async () => [] }
      }
      return {
        ok: true,
        status: 200,
        json: async () => [{
          id: 1,
          title: 'Interstellar',
          release_year: 2014,
          vote_average: 8.4,
          genres: [{ id: 1, name: 'Sci-Fi', slug: 'sci-fi' }],
        }],
      }
    }))

    render(<App />)
    expect(screen.getByText('CineMatch')).toBeInTheDocument()
    await waitFor(() => expect(screen.getByText('Interstellar')).toBeInTheDocument())
    fireEvent.click(screen.getByRole('button', { name: 'Discover' }))
    expect(screen.getByRole('heading', { name: 'Discover movies' })).toBeInTheDocument()
  })
})
