import React, { useState } from 'react';
import './UploadPage.css';
import { FaPlus } from 'react-icons/fa';

const API_URL = '/api'; // instead of http://127.0.0.1:8000

const UploadPage = () => {
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem('access_token')

    if (!title || !file) {
      alert('Please enter a title and choose a file.');
      return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
        headers: {
            'Authorization': `Bearer ${token}`,
          },
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      alert('File uploaded successfully!');
      setTitle('');
      setFile(null);
      e.target.reset();
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file.');
    }
  };

  return (
    <div className="container">
      <h1>Upload a New Flashcard Set</h1>

      <form className="stuff" onSubmit={handleSubmit} id="card">
        <label>
          <strong>Title:</strong>
        </label>
        <br />
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter set title"
          style={{ width: '80%', padding: '8px', margin: '10px 0' }}
        />
        <br />

        <label>
          <strong>Choose File:</strong>
        </label>
        <br />
        <input
          type="file"
          onChange={handleFileChange}
          style={{ margin: '10px 0' }}
        />
        <br />

        <div id="buttons">
          <button type="submit">
            <FaPlus className="icon" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default UploadPage;
