import React, { useState } from 'react'
import { processQuery } from '../api/nlp'

function TeamBuilder() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    const res = await processQuery(query)
    setResult(res)
  }

  return (
    <div>
      <h2>Team Builder</h2>
      <form onSubmit={handleSubmit}>
        <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Build a balanced team with a fire attacker" />
        <button type="submit">Generate Team</button>
      </form>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  )
}

export default TeamBuilder
