import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import JerseyList from './components/jerseys/JerseyList';
import SignInForm from './components/auth/SignInForm';
import SignUpForm from './components/auth/SignUpForm';
import LandingPage from './components/landing_page/LandingPage';

const App = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(() => {
        // Load the initial state from local storage
        const storedLoginState = localStorage.getItem('isLoggedIn');
        return storedLoginState ? JSON.parse(storedLoginState) : false;
    });
    const [loading, setLoading] = useState(true);

    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    const checkLoginStatus = async () => {
        console.log('Sending check-login request...'); // Debugging line
        try {
            const response = await fetch('http://localhost:8000/auth/check-login/', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            });

            console.log('Response status:', response.status); // Log response status
            const data = await response.json(); // Parse response here
            console.log('API Response:', data); // Log the entire response

            if (response.ok) {
                setIsLoggedIn(data.isLoggedIn); // Update login state
                localStorage.setItem('isLoggedIn', data.isLoggedIn); // Persist login state
                console.log('Set isLoggedIn to:', data.isLoggedIn); // Confirm what state is set
            } else {
                console.error('Failed to check login status:', response.status);
            }
        } catch (error) {
            console.error('Error fetching login status:', error);
        } finally {
            setLoading(false); // Set loading to false after check
        }
    };

    // Effect to check login status on mount
    useEffect(() => {
        console.log('Calling checkLoginStatus on mount...'); // Debugging line
        checkLoginStatus(); // Call checkLoginStatus on mount
    }, []);

    const handleLogin = () => {
        setIsLoggedIn(true); // Set login state to true
        localStorage.setItem('isLoggedIn', true); // Persist login state
        console.log('User logged in:', true);
    };

    const handleLogout = async () => {
        const csrfToken = getCookie('csrftoken');
        try {
            const response = await fetch('http://localhost:8000/auth/logout/', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            });

            if (response.ok) {
                setIsLoggedIn(false); // Update state to reflect logout
                localStorage.removeItem('isLoggedIn'); // Remove login state from local storage
                console.log('User logged out successfully');
            } else {
                console.error('Failed to log out:', response.status);
            }
        } catch (error) {
            console.error('Error logging out:', error);
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    // Log the value of isLoggedIn before rendering
    console.log('App isLoggedIn before rendering:', isLoggedIn);

    return (
        <Router>
            <Layout isLoggedIn={isLoggedIn} onLogout={handleLogout}>
                <Routes>
                    <Route path="/" element={<LandingPage />} />
                    <Route path="/signup" element={<SignUpForm onLogin={handleLogin} />} />
                    <Route path="/login" element={<SignInForm onLogin={handleLogin} />} />
                    <Route path="/jerseys" element={<JerseyList />} />
                </Routes>
            </Layout>
        </Router>
    );
};

export default App;
