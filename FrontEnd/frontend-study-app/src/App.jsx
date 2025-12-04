import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import HomePage from './components/HomePage';
import StudyPage from './components/StudyPage';
import UploadPage from './components/UploadPage';
import Matching from './components/Matching';
import Navbar from './components/NavBar';

function AppContent() {
  const location = useLocation();

  // Hide Navbar on login, register, and upload pages
  const hideNavbar = ["/", "/register", "/upload"].includes(location.pathname);

  return (
    <>
      {!hideNavbar && <Navbar />}
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/home" element={<HomePage />} />
       <Route path="/study/:setId" element={<StudyPage />} />
        <Route path="/matching/:setId" element={<Matching />} />
        <Route path="/upload" element={<UploadPage />} />
      </Routes>
    </>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
