import React from 'react';
import './HomePage.css'
import { FaUser, FaLock } from "react-icons/fa"

const myData = [
  { id: 1, content: "Item 1" },
  { id: 2, content: "Item 2" },
  { id: 3, content: "Item 3" },
  { id: 4, content: "Item 4" },
];

const HomePage = () => {
  return (
    <div className="container">
      {myData.map((item) => (
        <div key={item.id} className="stuff">
          {item.content}
          Stuff
        </div>
      ))}
    </div>
  );
};


export default HomePage;