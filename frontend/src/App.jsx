import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import JerseyList from './components/jerseys/JerseyList';
import Layout from './components/Layout';
import SignUpForm from './components/auth/SignUpForm';
import SignInForm from './components/auth/SignInForm';
import LandingPage from './components/landing_page/LandingPage';
import JerseyDetails from './components/JerseyDetails'; 

const App = () => {
    return (
        <Router>
            <Layout>
                <Routes>
                    <Route path="/" element={<LandingPage />} />
                    <Route path="/jerseys" element={<JerseyList />} />
                    <Route path="/signup" element={<SignUpForm />} />
                    <Route path="/login" element={<SignInForm />} />
                    <Route path="/jerseys/:id" element={<JerseyDetails />} />
                </Routes>
            </Layout>
        </Router>
    );
};

export default App;
