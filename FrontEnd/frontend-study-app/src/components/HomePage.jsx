import React, { useEffect, useState } from 'react';
import './HomePage.css';
import { FaPen, FaTrash } from "react-icons/fa";
import { useNavigate } from 'react-router-dom';

const API_URL = '/api'; // adjust if needed

const HomePage = () => {
  const navigate = useNavigate();
  const [flashcardSets, setFlashcardSets] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFlashcardSets = async () => {
      try {
        const token = localStorage.getItem('access_token'); // get JWT token
        if (!token) throw new Error("No access token found");

        const response = await fetch(`${API_URL}/home`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`Error fetching flashcard sets: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("Flashcard sets received:", data);
        setFlashcardSets(data); // assuming backend returns {id: title} object
      } catch (err) {
        setError(err.message);
      }
    };

    fetchFlashcardSets();
  }, []);

  const handleClick = (id) => {
    navigate(`/study/${id}`);
  };

  const handleDelete = async (e, id) => {
    e.stopPropagation();
    const confirmed = window.confirm("Are you sure you want to delete this set?");
    if (!confirmed) return;

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_URL}/flashcard/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) throw new Error("Failed to delete flashcard set");
      
      setFlashcardSets(prev => prev.filter(fs => fs.id !== id));
    } catch (err) {
      console.error(err);
      alert(err.message);
    }
  };

  const handleLogout = () => {
      localStorage.removeItem("access_token");
      navigate("/"); 
  }

  return (
    <div className="container">
      <div className='banner'>
        <h1>Flash Card Sets:</h1>
        <button className="logout-button" onClick={handleLogout}>Logout</button>
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div id="card_list">
        {Array.isArray(flashcardSets) && flashcardSets.length > 0 ? (
          flashcardSets.map((fs) => (
            <div
              key={fs.id}
              className="stuff"
              onClick={() => handleClick(fs.id)}
              style={{ cursor: "pointer" }}
              id="card"
            >
              {fs.title}
              <br /><br />
              <div id="buttons">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/edit/${fs.id}`);
                  }}
                >
                  <FaPen className='icon1' />
                </button>
                <button
                  onClick={(e) => handleDelete(e, fs.id)}
                >
                  <FaTrash className='icon2' />
                </button>
              </div>
            </div>
          ))
        ) : (
          <p>{flashcardSets.message || "No flashcard sets found."}</p>
        )}
      </div>
    </div>
  );
};

export default HomePage;
