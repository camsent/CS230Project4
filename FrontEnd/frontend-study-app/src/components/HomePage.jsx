import React from 'react';
import './HomePage.css'
import { FaUser, FaLock } from "react-icons/fa"

const myData = [
  { id: 1, content: "Item 1" },
  { id: 2, content: "Item 2" },
  { id: 2, content: "Item 2" },
  { id: 2, content: "Item 2" },
  { id: 2, content: "Item 2" },
  { id: 2, content: "Item 2" },
  { id: 2, content: "Item 2" },
  { id: 2, content: "Item 2" },
  { id: 2, content: "Item 2" },
  { id: 2, content: "Item 2" },

];

const HomePage = () => {
  return (
    <div className="container">
      {myData.map((item) => (
        <div key={item.id} className="stuff">
          {item.content}
          <br></br>
          <button>Delete</button>
          <button>Edit</button>
        </div>
      ))}
    </div>
  );
};


export default HomePage;