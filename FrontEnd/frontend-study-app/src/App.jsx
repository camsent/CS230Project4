import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import HomePage from './components/homePage';
import Navbar from './components/NavBar';
import StudyPage from './components/StudyPage'
import UploadPage from './components/UploadPage';
import EditPage from './components/EditPage';
import Matching from './components/Matching';

function App() {

  return (
    <>
    <Navbar />
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/home" element={<HomePage />} />
        {
        //<Route path="/study/:setId" element={<StudyPage />} />
        }
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/study" element={<StudyPage />} />
        <Route path="/edit" element={<EditPage />} />
        <Route path="/matching" element={<Matching />} />
      </Routes>
    </Router>
    </>
  )
}

export default App;
