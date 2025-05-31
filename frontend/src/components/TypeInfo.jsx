import { useState } from "react";
import axios from "axios";

const TypeInfo = () => {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setResult("");

    try {
      const res = await axios.post("http://localhost:5000/api/type", {
        query: query
      });

      if (res.data.response) {
        setResult(res.data.response);
      } else {
        setResult("Unexpected response from server.");
      }
    } catch (err) {
      setResult("Error fetching type info.");
    }

    setLoading(false);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Type Info</h2>
      <textarea
        className="w-full p-2 border rounded"
        rows="3"
        placeholder="Ask about a type, e.g., 'What is fire weak against?'"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        className="mt-2 px-4 py-2 bg-indigo-600 text-white rounded"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Loading..." : "Get Type Info"}
      </button>

      {result && (
        <div className="mt-4 whitespace-pre-wrap bg-gray-100 p-3 rounded">
          {result}
        </div>
      )}
    </div>
  );
};

export default TypeInfo;
