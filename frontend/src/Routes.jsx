import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
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
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/jerseys" element={<JerseyList />} />
          <Route path="/jerseys/:id" element={<JerseyDetail />} />
          <Route path="/login" element={<SignInForm />} />
          <Route path="/signup" element={<SignUpForm />} />
          <Route path="/promoted" element={<PromotedJerseys />} />
          <Route path="/new-releases" element={<NewReleases />} />
          <Route path="/upcoming" element={<UpcomingJerseys />} />
          <Route path="/liked-jerseys" element={ <LikedJerseys />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default AppRoutes;
