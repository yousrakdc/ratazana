import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import JerseyList from './components/jerseys/JerseyList';
import SignInForm from './components/auth/SignInForm';
import SignUpForm from './components/auth/SignUpForm';
import Layout from './components/Layout';
import LandingPage from './components/landing_page/LandingPage';
import JerseyDetail from './components/jerseys/JerseyDetail'; // Import JerseyDetail if you need to display jersey details

const AppRoutes = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/jerseys" element={<JerseyList />} />
          <Route path="/jerseys/:id" element={<JerseyDetail />} /> {/* Ensure to include this for details */}
          <Route path="/login" element={<SignInForm />} />
          <Route path="/signup" element={<SignUpForm />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default AppRoutes;
