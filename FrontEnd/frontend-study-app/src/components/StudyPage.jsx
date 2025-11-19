import React, { useState } from 'react';
import './StudyPage.css';
import { FaArrowLeft, FaArrowRight } from "react-icons/fa"
import { useNavigate } from 'react-router-dom';


const myData = [
  { card_num: 1, front: "France", back: "Paris" },
  { card_num: 2, front: "Japan", back: "Tokyo" },
  { card_num: 3, front: "Canada", back: "Ottawa" },
  { card_num: 4, front: "Brazil", back: "Brasília" },
  { card_num: 5, front: "Australia", back: "Canberra" },
  { card_num: 6, front: "Egypt", back: "Cairo" },
  { card_num: 7, front: "India", back: "New Delhi" },
  { card_num: 8, front: "Kenya", back: "Nairobi" },
];

const StudyPage = () => {
  const [index, setIndex] = useState(0);
  const [showFront, setShowFront] = useState(true);
  const navigate = useNavigate();

  const handlePrev = () => {
    setShowFront(true);
    setIndex((prev) => (prev === 0 ? myData.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setShowFront(true);
    setIndex((prev) => (prev === myData.length - 1 ? 0 : prev + 1));
  };

  const handleFlip = () => setShowFront((prev) => !prev);

  const handleClick = (id) => {
    navigate(`/study/${id}`); // example dynamic navigation
  };

  const currentCard = myData[index];

  return (
    <div className="container">
      <div id="studying">
        <div id="flashcard" onClick={handleFlip}>
          <div>{showFront ? currentCard.front : currentCard.back}</div>
        </div>
        <div id="buttons">
        <button onClick={handlePrev}><FaArrowLeft className='icon' /></button>
        <button onClick={handleNext}><FaArrowRight className='icon' /></button>
        </div>
      </div>

      <div style={{ marginTop: '1rem' }}>
        <p style={{ color: "ghostwhite" }}>Card {currentCard.card_num} of {myData.length}</p>
      </div>
    </div>
  );
};

export default StudyPage;