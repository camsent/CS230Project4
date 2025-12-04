import React, { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import './matching.css';

const API_URL = '/api';


// Fetch cards from backend
async function getMatching(set_id) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(`${API_URL}/matching/${set_id}`, {
    method: 'GET',
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error("Error getting flashcards");
  }

  return await response.json();
}

const shuffleArray = (array) => [...array].sort(() => Math.random() - 0.5);


export default function Matching() {
  const { setId } = useParams();

  const [cards, setCards] = useState([]);
  const [FrontCard, setFrontCard] = useState([]);
  const [BackCard, setBackCard] = useState([]);
  const [pairedData, setPairedData] = useState([]);
  const [selectedMatch, setSelectedMatch] = useState(null);

  const [time, setTime] = useState(0);
  const [running, setRunning] = useState(false);
  const [win, setWin] = useState(false);

  // Fetch cards from backend
  useEffect(() => {
    async function load() {
      try {
        const flashcards = await getMatching(setId);
        setCards(flashcards);
        setFrontCard(shuffleArray(flashcards));
        setBackCard(shuffleArray(flashcards));
      } catch (err) {
        console.error(err);
      }
    }
    load();
  }, [setId]);

  // Timer
  useEffect(() => {
    let interval;
    if (running) {
      interval = setInterval(() => setTime((t) => t + 1), 1000);
    }
    return () => clearInterval(interval);
  }, [running]);

  const matchWin = pairedData.length === cards.length;

  useEffect(() => {
    if (matchWin) triggerWin();
  }, [matchWin]);

  const startGame = () => {
    setFrontCard(shuffleArray(cards));
    setBackCard(shuffleArray(cards));
    setPairedData([]);
    setSelectedMatch(null);

    setTime(0);
    setRunning(true);
    setWin(false);
  };

  const triggerWin = () => {
    setRunning(false);
    setWin(true);
  };

  const isMatched = (matchBack) =>
    pairedData.some((pairedMatch) => pairedMatch === matchBack);

  const handleClick = (match) => {
    if (!running) setRunning(true);

    if (selectedMatch && match.back === selectedMatch.back) {
      setPairedData([...pairedData, match.back]);
    }
    setSelectedMatch(null);
  };

  const confetti = Array.from({ length: 40 }).map(() => ({
    x: Math.floor(Math.random() * 100),
    d: Math.random() * 4,
  }));

  return (
    <>
      {/* TIMER DISPLAY */}
      <div className="timer-display">Time: {time}s</div>

      {/* WIN EFFECT */}
      {win && (
        <>
          <div className="win-banner">🎉 YOU WIN! 🎉</div>
          <button className="play-again-btn" onClick={startGame}>
            Play Again
          </button>

          <div className="confetti-container">
            {confetti.map((c, i) => (
              <div
                key={i}
                className="confetti-piece"
                style={{ "--x": c.x, "--d": c.d }}
              ></div>
            ))}
          </div>
        </>
      )}

      {/* GAME BOARD */}
      <div className="match-container">
        <div className="column">
          {FrontCard.map((match, index) => (
            <button
              className={`match-btn ${isMatched(match.back) ? "matched" : ""}`}
              key={index}
              onClick={() => setSelectedMatch(match)}
            >
              {match.front}
            </button>
          ))}
        </div>

        <div className="column">
          {BackCard.map((match, index) => (
            <button
              className={`match-btn ${isMatched(match.back) ? "matched" : ""}`}
              key={index}
              onClick={() => handleClick(match)}
            >
              {match.back}
            </button>
          ))}
        </div>
      </div>
    </>
  );
}

