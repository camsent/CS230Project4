import React, { useState } from "react";
import "./TestPage.css";
import { FaArrowRight } from "react-icons/fa";

// Hardcoded quiz data 
const quizData = [
  {
    question: "What is the capital of France?",
    choices: ["Paris", "Madrid", "Berlin", "Lisbon"],
    answer: "Paris"
  },
  {
    question: "What is the capital of Japan?",
    choices: ["Kyoto", "Tokyo", "Osaka", "Nagoya"],
    answer: "Tokyo"
  },
  {
    question: "What is the capital of Australia?",
    choices: ["Melbourne", "Sydney", "Canberra", "Perth"],
    answer: "Canberra"
  },
  {
    question: "What is the capital of Brazil?",
    choices: ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"],
    answer: "Brasília"
  }
];

// TestPage component
const TestPage = () => {
    // State to track current question index, selected choice, and correctness
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState(null);
  const [isCorrect, setIsCorrect] = useState(null);

  const current = quizData[index];

  // Handle choice selection and provide feedback
  const handleSelect = (choice) => {
    if (selected) return; // prevent double clicking
    setSelected(choice);
    setIsCorrect(choice === current.answer);
  };

  // Move to the next question
  const handleNext = () => {
    setSelected(null);
    setIsCorrect(null);
    setIndex((prev) => (prev === quizData.length - 1 ? 0 : prev + 1));
  };

  // Render the test page UI with question, choices, feedback, and navigation 
  return (
    <div id="test-container">
      <h1 id="question">{current.question}</h1>

      <div id="choices">
        {current.choices.map((choice, i) => (
          <button
            key={i}
            className={`choice-btn ${
              selected
                ? choice === current.answer
                  ? "correct"
                  : choice === selected
                  ? "incorrect"
                  : ""
                : ""
            }`}
            onClick={() => handleSelect(choice)}
          >
            {choice}
          </button>
        ))}
      </div>

      {selected && (
        <div id="feedback">
          {isCorrect ? (
            <p className="correct-text">Correct!</p>
          ) : (
            <p className="incorrect-text">
              Incorrect — Correct answer: {current.answer}
            </p>
          )}

          <button id="next-btn" onClick={handleNext}>
            Next <FaArrowRight className="icon" />
          </button>
        </div>
      )}

      <p id="counter">
        Question {index + 1} of {quizData.length}
      </p>
    </div>
  );
};

// Export the TestPage component to be used in other parts of the application
export default TestPage;
