import React, { useState } from 'react';
import './Summarize.css';
import { FaPlus } from 'react-icons/fa';
import { redirect } from 'react-router-dom';

const API_URL = '/api'; // your backend endpoint

const SummarizePage = () => {
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);
  const [numCards, setNumCards] = useState(10); // Default to 10 cards
  const [summaryText, setSummaryText] = useState("");


  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('access_token');

    if (!file) {
      alert('Please choose a file.');
      return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('file', file);
    formData.append('num_cards', numCards);

    try {
      const response = await fetch(`${API_URL}/summarize`, {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

       const data = await response.json();
       setSummaryText(data.text);

      setTitle('');
      setFile(null);
      setNumCards(10);
      e.target.reset();
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file.');
    }
  };

  return (
  <div className="container"  style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
    <h1>Summarize Text</h1>
    <form className="stuff" onSubmit={handleSubmit} id="card">
      <label>
        <strong>Choose File:</strong>
      </label>
      <br />
      <input
        type="file"
        onChange={handleFileChange}
        style={{ margin: '10px 0' }}
      />
      <div id="buttons">
        <button type="submit">
          <FaPlus className="icon" />
        </button>
      </div>
    </form>

    <div
      id="summary-box"
      style={{
        marginTop: "100px",
        padding: "15px",
        border: "1px solid #ccc",
        borderRadius: "8px",
        minHeight: "120px",
        background: "#f8f8f8",
      }}
    >
      <p>{summaryText}</p>
    </div>
  </div>
 );
}

export default SummarizePage;
