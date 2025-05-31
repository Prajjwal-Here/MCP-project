export async function processQuery(query) {
  const response = await fetch('http://localhost:5000/api/nlp/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  })

  const data = await response.json()
  return data
}
