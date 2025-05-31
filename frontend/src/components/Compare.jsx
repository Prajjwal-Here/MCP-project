import React, { useState } from 'react'
import { processQuery } from '../api/nlp'

function Compare() {
  const [query, setQuery] = useState('')
  const [sentence, setSentence] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    const res = await processQuery(query)
    if (res && res.sentence) {
      setSentence(res.sentence)
    } else {
      setSentence('Sorry, could not generate a comparison.')
    }
  }

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Compare Pokémon</h2>
      <form onSubmit={handleSubmit} className="mb-4 flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Compare Pikachu and Alakazam"
          className="border rounded p-2 flex-1"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Compare
        </button>
      </form>
      {sentence && (
        <div className="bg-white shadow rounded p-4 border border-gray-200">
          {sentence}
        </div>
      )}
    </div>
  )
}

export default Compare
