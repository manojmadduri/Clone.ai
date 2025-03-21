import React, { useState } from "react";
import { Card, Button, Alert, Form, Container } from "react-bootstrap";
import { FaPlus, FaPaperPlane } from "react-icons/fa";
import "bootstrap/dist/css/bootstrap.min.css";
import "./styles.css";

function App() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [status, setStatus] = useState("");

  // Add personal text
  const handleAddText = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/add_text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content }),
      });

      if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

      const data = await response.json();
      setStatus(data.status === "duplicate" ? "Title already exists!" : "Text added successfully!");
      setTitle("");
      setContent("");
    } catch (error) {
      console.error("Error adding text:", error);
      setStatus("Failed to add text.");
    }
  };

  // Query AI
  const handleQueryAI = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/query_ai", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

      const data = await response.json();
      setAnswer(data.answer || "No response.");
    } catch (error) {
      console.error("Error querying AI:", error);
      setAnswer("Failed to get AI response.");
    }
  };

  return (
    <Container className="container">
      <h1>Clone.AI - Personal AI</h1>

      {/* Status Message */}
      {status && <Alert variant="info">{status}</Alert>}

      {/* Add Personal Data */}
      <Card className="p-3">
        <h2 className="mb-3">Add Personal Data</h2>
        <Form.Control
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="mb-2"
        />
        <Form.Control
          as="textarea"
          rows={3}
          placeholder="Content..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="mb-2"
        />
        <Button variant="success" className="w-100" onClick={handleAddText}>
          <FaPlus className="me-2" /> Add Text
        </Button>
      </Card>

      {/* Query AI */}
      <Card className="p-3">
        <h2 className="mb-3">Ask Your AI</h2>
        <Form.Control
          type="text"
          placeholder="Ask something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="mb-2"
        />
        <Button variant="primary" className="w-100" onClick={handleQueryAI}>
          <FaPaperPlane className="me-2" /> Get Answer
        </Button>
      </Card>

      {/* AI Response */}
      {answer && (
        <Card className="p-3">
          <h3>AI's Response:</h3>
          <Alert variant="secondary">{answer}</Alert>
        </Card>
      )}
    </Container>
  );
}

export default App;
