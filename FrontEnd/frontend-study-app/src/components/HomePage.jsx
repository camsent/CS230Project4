import React from 'react';
import './HomePage.css'
import { FaUser, FaLock } from "react-icons/fa"
import { useNavigate } from 'react-router-dom';


const myData = [
  { id: 1, content: "Item 1" },
  { id: 2, content: "Item 2" },
  { id: 3, content: "Item 3" },
  { id: 4, content: "Item 4" },
  { id: 5, content: "Item 5" },

];


const HomePage = () => {
  const navigate = useNavigate();

  const handleClick = (id) => {
    navigate(`/study/${id}`); // navigate to another page (dynamic route)
  };

  return (
    <div className="container">
      {myData.map((item) => (
        <div
          key={item.id}
          className="stuff"
          onClick={() => handleClick(item.id)}
          style={{ cursor: "pointer" }}
        >
          {item.content}
          <br />
          <br />
          <button>Study</button>
          <button>Edit</button>
          <button>Delete</button>
        </div>
      ))}
    </div>
  );
};


export default HomePage;