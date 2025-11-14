import React, { useState } from 'react';
import './EditPage.css';
import { FaTrash, FaSave } from "react-icons/fa";

const initialData = [
  { card_num: 1, front: "Mountain", back: "Large natural elevation of Earth’s surface" },
  { card_num: 2, front: "Plateau", back: "High, flat landform" },
  { card_num: 3, front: "Delta", back: "Sediment deposition at a river mouth" },
  { card_num: 4, front: "Valley", back: "Low area between hills/mountains" },
  { card_num: 5, front: "Archipelago", back: "Chain or group of islands" },
  { card_num: 6, front: "Desert", back: "Dry region with little rainfall" },
  { card_num: 7, front: "Glacier", back: "Slow-moving mass of ice" },
  { card_num: 8, front: "Canyon", back: "Deep gorge with steep sides" },
];


const EditPage = () => {
  const [cards, setCards] = useState(initialData);

  const handleChange = (index, side, value) => {
    const updated = [...cards];
    updated[index][side] = value;
    setCards(updated);
  };

  const handleDelete = (card_num) => {
    const confirmed = window.confirm(`Are you sure you want to delete card #${card_num}?`);
    if (confirmed) {
      setCards(cards.filter((card) => card.card_num !== card_num));
    }
  };

  const handleSave = () => {
    console.log("Saved cards:", cards);
    alert("Cards saved successfully!");
    // Here you can add API call to persist changes
  };

  return (
    <div className="container">
      <h1>Edit Flashcards</h1>

      <div className="card-list">
        {cards.map((item, index) => (
          <React.Fragment key={item.card_num}>
            {/* Front Card */}
            <div className="card">
              <div className="card-content">
                <h3>Front</h3>
                <textarea
                  value={item.front}
                  onChange={(e) => handleChange(index, "front", e.target.value)}
                />
              </div>
            </div>

            {/* Back Card */}
            <div className="card">
              <div className="card-content">
                <h3>Back</h3>
                <textarea
                  value={item.back}
                  onChange={(e) => handleChange(index, "back", e.target.value)}
                />
              </div>
            </div>

            {/* Delete Button (one per row) */}
            <div className="row-delete">
              <button className="delete-btn" onClick={() => handleDelete(item.card_num)}>
                <FaTrash className="icon" /> Delete Card
              </button>
            </div>
          </React.Fragment>
        ))}
      </div>
      <button>+</button>
      {/* Floating Save Button */}
      <button className="save-btn" onClick={handleSave}><FaSave className="icon" /></button>
    </div>
  );
};

export default EditPage;
