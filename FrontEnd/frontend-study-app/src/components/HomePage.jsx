import React from 'react';
import './HomePage.css'
import { FaPen, FaTrash } from "react-icons/fa"
import { useNavigate } from 'react-router-dom';


const myData = [
  { id: 1, content: "World Capitals" },
  { id: 2, content: "Landforms" },
  { id: 3, content: "Continents & Oceans" },
  { id: 4, content: "U.S. States & Abbreviations" },
  { id: 5, content: "Major Rivers of the World" },
];


const HomePage = () => {
  const navigate = useNavigate();

  const handleClick = (id) => {
    navigate(`/study/`); // navigate to another page (dynamic route)
  };

  const handleDelete = (e, item) => {
    e.stopPropagation();
    const confirmed = window.confirm(`Are you sure you want to delete "${item.content}"?`);
    if (confirmed) {
      console.log(`Deleted item with id: ${item.id}`);
      // Your delete logic here (e.g., API call or state update)
    }
  };

  return (
    <div className="container">
      <h1>Flash Card Sets:</h1>
      <div id="card_list">
        {myData.map((item) => (
          <div
            key={item.id}
            className="stuff"
            onClick={() => handleClick(item.id)}
            style={{ cursor: "pointer" }}
            id="card"
          >
            {item.content}
            <br />
            <br />
            <div id="buttons">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/edit/`);
                }}
              >
                <FaPen className='icon1' />
              </button>
              <button
                onClick={(e) => handleDelete(e, item)}
              >
                <FaTrash className='icon2' />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>

    
  );
};


export default HomePage;