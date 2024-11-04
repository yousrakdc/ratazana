import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import JerseyList from './components/jerseys/JerseyList';
import SignInForm from './components/auth/SignInForm';
import SignUpForm from './components/auth/SignUpForm';
import LandingPage from './components/landing_page/LandingPage';
import LikedJerseys from './components/jerseys/LikedJerseys';

const App = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(() => {
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
        console.log('Sending check-login request...');
        try {
            const response = await fetch('http://localhost:8000/auth/check-login/', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            });

            console.log('Response status:', response.status);
            const data = await response.json();
            console.log('API Response:', data);

            if (response.ok) {
                setIsLoggedIn(data.isLoggedIn);
                localStorage.setItem('isLoggedIn', data.isLoggedIn);
                console.log('Set isLoggedIn to:', data.isLoggedIn);
            } else {
                console.error('Failed to check login status:', response.status);
            }
        } catch (error) {
            console.error('Error fetching login status:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        console.log('Calling checkLoginStatus on mount...');
        checkLoginStatus();
    }, []);

    const handleLogin = () => {
        setIsLoggedIn(true);
        localStorage.setItem('isLoggedIn', true);
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
                setIsLoggedIn(false);
                localStorage.removeItem('isLoggedIn');
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

    return (
        <Router>
            <Layout isLoggedIn={isLoggedIn} onLogout={handleLogout}>
                <Routes>
                    <Route path="/" element={<LandingPage />} />
                    <Route path="/signup" element={<SignUpForm onLogin={handleLogin} />} />
                    <Route path="/login" element={<SignInForm onLogin={handleLogin} />} />
                    <Route path="/jerseys" element={<JerseyList />} />
                    <Route
                        path="/liked-jerseys"
                        element={isLoggedIn ? <LikedJerseys /> : <Navigate to="/login" />}
                    />
                </Routes>
            </Layout>
        </Router>
    );
};

export default App;
