import React, { useState } from "react";

function App() {
  // State for adding personal text
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  // State for querying AI
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");

  // 1) Add new personal text
  const handleAddText = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/add_text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content }),
        mode: "cors",
      });

      if (!response.ok) throw new Error(`Error: ${response.status}`);

      alert("Text added successfully!");
      setTitle("");
      setContent("");
    } catch (error) {
      console.error("Fetch error:", error);
      alert("Failed to add text.");
    }
  };

  // 2) Query the AI
  const handleQueryAI = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/query_ai", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (!data.answer || data.answer.trim() === "") {
            setAnswer("I don't have data for that.");  // ✅ Prevents frontend crashes
        } else {
            setAnswer(data.answer);
        }
    } catch (error) {
        console.error("Error fetching AI response:", error);
        setAnswer("An error occurred. Please try again.");  // ✅ Ensures UI never breaks
    }
};

  

  return (
    <div style={{ margin: "20px" }}>
      <h1>Personal AI - Phase 1 (Text Only)</h1>

      {/* Section to add new personal text */}
      <div style={{ marginBottom: "30px" }}>
        <h2>Add Personal Data</h2>
        <input
          type="text"
          placeholder="Title..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{ width: "300px", display: "block", marginBottom: "10px" }}
        />
        <textarea
          rows={4}
          placeholder="Content..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          style={{ width: "300px", marginBottom: "10px" }}
        />
        <button onClick={handleAddText}>Add Text</button>
      </div>

      {/* Section to query AI */}
      <div>
        <h2>Ask AI</h2>
        <input
          type="text"
          placeholder="Ask a question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ width: "300px", display: "block", marginBottom: "10px" }}
        />
        <button onClick={handleQueryAI}>Get Answer</button>
      </div>

      {/* Display AI response */}
      {answer && (
        <div style={{ marginTop: "20px" }}>
          <h3>AI's Response:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;
