import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import HomePage from './components/homePage';
<<<<<<< HEAD
import Navbar from './components/NavBar';
=======
import StudyPage from './components/StudyPage'
>>>>>>> 4488f3eeb956ebd84aa04141e29fbfb5f6f24c1c


function App() {

  return (
    <>
    <Navbar />
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/study" element={<StudyPage />} />
      </Routes>
    </Router>
    </>
  )
}

export default App;
