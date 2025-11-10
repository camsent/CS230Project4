import React, { useState } from 'react';
import './StudyPage.css';
import { useNavigate } from 'react-router-dom';

const myData = [
  { card_num: 1, front: "Item 1", back: "1 Item" },
  { card_num: 2, front: "Item 2", back: "2 Item" },
  { card_num: 3, front: "Item 3", back: "3 Item" },
  { card_num: 4, front: "Item 4", back: "4 Item" },
  { card_num: 5, front: "Item 5", back: "5 Item" },
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
        <button onClick={handlePrev}>PREV</button>

        <div id="flashcard" onClick={handleFlip}>
          <div>{showFront ? currentCard.front : currentCard.back}</div>
        </div>

        <button onClick={handleNext}>NEXT</button>
      </div>

      <div style={{ marginTop: '1rem' }}>
        <p style={{ color: "ghostwhite" }}>Card {currentCard.card_num} of {myData.length}</p>
      </div>
    </div>
  );
};

export default StudyPage;