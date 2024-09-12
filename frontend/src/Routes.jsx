import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import JerseyList from './components/jerseys/JerseyList';
import Layout from './components/Layout';
import LandingPage from './components/landing_page/LandingPage';


const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route 
        path="/"
        element={
        <Layout>=
            <LandingPage />
        </Layout>
        }
        />
        <Route path="/jerseys" element={<JerseyList />} />
        {/* Define additional routes here */}
      </Routes>
    </Router>
  );
};

export default AppRoutes;