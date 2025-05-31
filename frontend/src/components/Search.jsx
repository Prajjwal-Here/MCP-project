import React, { useState } from 'react'
import { processQuery } from '../api/nlp'

function Search() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    const res = await processQuery(query)
    setResult(res)
  }

  return (
    <div>
      <h2>Search Pokémon Info</h2>
      <form onSubmit={handleSubmit}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Enter query"
        />
        <button type="submit">Submit</button>
      </form>

      {result && result.response && (
        <div
          style={{
            whiteSpace: 'pre-line',
            background: 'white',
            padding: '1rem',
            marginTop: '1rem',
            borderRadius: '0.5rem',
            boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
            textAlign: 'left'
          }}
        >
          {result.response}
        </div>
      )}
    </div>
  )
}

export default Search
