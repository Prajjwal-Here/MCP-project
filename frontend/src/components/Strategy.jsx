import React, { useState } from 'react'
import { processQuery } from '../api/nlp'

function Strategy() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    const res = await processQuery(query)
    setResult(res.response || 'No response received.')
  }

  return (
    <div>
      <h2 className="text-xl font-bold mb-2">Strategy Guide</h2>
      <form onSubmit={handleSubmit} className="mb-4">
        <input
          className="border px-2 py-1 mr-2 w-80"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="What's the best strategy for Gengar?"
        />
        <button
          type="submit"
          className="bg-purple-600 text-white px-4 py-1 rounded"
        >
          Get Strategy
        </button>
      </form>
      {result && (
        <div className="whitespace-pre-line bg-gray-100 p-4 rounded border">
          {result}
        </div>
      )}
    </div>
  )
}

export default Strategy
