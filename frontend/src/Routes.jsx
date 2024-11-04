import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import JerseyList from './components/jerseys/JerseyList';
import SignInForm from './components/auth/SignInForm';
import SignUpForm from './components/auth/SignUpForm';
import Layout from './components/Layout';
import LandingPage from './components/landing_page/LandingPage';
import JerseyDetail from './components/jerseys/JerseyDetail';
import PromotedJerseys from './components/landing_page/PromotedJerseys';
import NewReleases from './components/landing_page/NewReleases'; 
import UpcomingJerseys from './components/landing_page/UpcomingJerseys';
import LikedJerseys from './components/jerseys/LikedJerseys';

const AppRoutes = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Effect to check the login status based on local storage
  useEffect(() => {
    const loggedIn = localStorage.getItem('isLoggedIn') === 'true';
    setIsLoggedIn(loggedIn);
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
    localStorage.setItem('isLoggedIn', true);
  };

  const handleLogout = async () => {
    try {
        setIsLoggedIn(false);
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('authToken'); // Also remove the auth token if needed
    } catch (error) {
        console.error("Logout error:", error);
    }
};


  return (
    <Router>
      <Layout isLoggedIn={isLoggedIn} onLogout={handleLogout}>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/jerseys" element={<JerseyList />} />
          <Route path="/jerseys/:id" element={<JerseyDetail />} />
          <Route path="/login" element={<SignInForm onLogin={handleLogin} />} />
          <Route path="/signup" element={<SignUpForm onLogin={handleLogin} />} />
          <Route path="/promoted" element={<PromotedJerseys />} />
          <Route path="/new-releases" element={<NewReleases />} />
          <Route path="/upcoming" element={<UpcomingJerseys />} />
          <Route
            path="/liked-jerseys"
            element={isLoggedIn ? <LikedJerseys /> : <Navigate to="/login" />}
          />
        </Routes>
      </Layout>
    </Router>
  );
};

export default AppRoutes;
