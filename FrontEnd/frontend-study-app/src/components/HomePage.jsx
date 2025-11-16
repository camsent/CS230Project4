import React, { useState, useEffect } from 'react';
import './HomePage.css'
import { FaPen, FaTrash } from "react-icons/fa";
import { useNavigate } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:8000';

export async function getSets() {
  const response = await fetch(`${API_URL}/home`, {        
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
  });
 
  if (!response.ok) {
    throw new Error('Failed to fetch sets');
  }

  const data = await response.json();

  // Transform backend data into the same shape as `myData`
  const formattedData = data.map(item => ({
    id: item.id,
    title: item.title,
  }));

  return formattedData;
}

const HomePage = () => {
  const [myData, setMyData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchData() {
      try {
        const sets = await getSets();
        setMyData(sets);
      } catch (error) {
        console.error('Error fetching sets:', error);
      }
    }
    fetchData();
  }, []);

  const handleClick = (id) => {
    navigate(`/study/${id}`);
  };

  const handleDelete = (e, item) => {
    e.stopPropagation();
    const confirmed = window.confirm(`Are you sure you want to delete "${item.title}"?`);
    if (confirmed) {
      console.log(`Deleted item with id: ${item.id}`);
      // TODO: Add API delete or state update
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
            {item.title}
            <br />
            <br />
            <div id="buttons">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/edit/${item.id}`);
                }}
              >
                <FaPen className='icon' />
              </button>
              <button onClick={(e) => handleDelete(e, item)}>
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