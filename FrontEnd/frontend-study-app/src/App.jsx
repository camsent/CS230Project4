import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import HomePage from './components/homePage';
import Navbar from './components/NavBar';
import StudyPage from './components/StudyPage'
import EditPage from './components/EditPage';

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
        <Route path="/edit" element={<EditPage />} />
      </Routes>
    </Router>
    </>
  )
}

export default App;
