import React, { useState, useEffect } from 'react';
import './StudyPage.css';
import { FaArrowLeft, FaArrowRight } from "react-icons/fa";
import { useNavigate, useParams } from 'react-router-dom';

const API_URL = '/api'; // Vite proxy will handle this

const StudyPage = () => {
  const { setId } = useParams(); // dynamic route /study/:setId
  const [cards, setCards] = useState([]);
  const [index, setIndex] = useState(0);
  const [showFront, setShowFront] = useState(true);
  const navigate = useNavigate();

  // Fetch flashcards on component mount
  useEffect(() => {
  const fetchFlashcards = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_URL}/get/flashcard/set/${setId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) {
        if (response.status === 401) {
          alert('Unauthorized. Please log in again.');
          navigate('/login');
          return;
        }
        throw new Error('Failed to fetch flashcards');
      }

      const data = await response.json();
      setCards(data.flashcards || []);
      setIndex(0);
      setShowFront(true);
    } catch (err) {
      console.error(err);
      alert('Error loading flashcards');
    }
  };

  fetchFlashcards();
}, [setId, navigate]);


  const handlePrev = () => {
    setShowFront(true);
    setIndex(prev => (prev === 0 ? cards.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setShowFront(true);
    setIndex(prev => (prev === cards.length - 1 ? 0 : prev + 1));
  };

  const handleFlip = () => setShowFront(prev => !prev);

  if (!cards.length) return <p>Loading flashcards...</p>;

  const currentCard = cards[index];

  return (
    <div className="container">
      <div id="studying">
        <div id="flashcard" onClick={handleFlip}>
          {showFront ? currentCard.front : currentCard.back}
        </div>
        <div id="buttons">
          <button onClick={handlePrev}><FaArrowLeft className='icon' /></button>
          <button onClick={handleNext}><FaArrowRight className='icon' /></button>
        </div>
      </div>

      <div style={{ marginTop: '1rem' }}>
        <p style={{ color: "ghostwhite" }}>Card {index + 1} of {cards.length}</p>
      </div>
    </div>
  );
};

export default StudyPage;
