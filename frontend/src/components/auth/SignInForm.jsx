import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SignInForm.css';

// Function to get a cookie value by name
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

const SignInForm = ({ onLogin }) => {
    console.log('onLogin prop:', onLogin); // Log the onLogin prop
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [csrfToken, setCsrfToken] = useState('');
    const navigate = useNavigate();

    // Function to check if the access token is expired
    const isTokenExpired = (token) => {
        if (!token) return true;
        const payload = JSON.parse(atob(token.split('.')[1]));
        return (payload.exp * 1000) < Date.now();
    };

    // Function to handle token refresh using refresh token
    const handleTokenRefresh = async (refreshToken) => {
        try {
            const response = await axios.post(
                'http://localhost:8000/auth/token/refresh/',
                { refresh: refreshToken },
                { withCredentials: true }
            );

            const newAccessToken = response.data.access;
            localStorage.setItem('authToken', newAccessToken);
            return newAccessToken;
        } catch (error) {
            console.error('Token refresh error:', error);
            if (error.response && (error.response.status === 401 || error.response.status === 403)) {
                localStorage.removeItem('authToken');
                localStorage.removeItem('refreshToken');
                setError('Your session has expired. Please log in again.');
            }
            return null;
        }
    };

    useEffect(() => {
        const authToken = localStorage.getItem('authToken');
        const refreshToken = localStorage.getItem('refreshToken');

        // Check if the auth token is valid or if a refresh token needs to be used
        if (authToken && !isTokenExpired(authToken)) {
            if (typeof onLogin === 'function') {
                onLogin();
            } else {
                console.error('onLogin is not a function');
            }
        } else if (refreshToken) {
            handleTokenRefresh(refreshToken);
        }

        // Fetch the CSRF token
        const fetchCsrfToken = async () => {
            try {
                const response = await axios.get('http://localhost:8000/auth/api/csrf-token/', { withCredentials: true });
                setCsrfToken(response.data.csrfToken);
            } catch (error) {
                console.error('Error fetching CSRF token from server:', error);
                setError('Could not retrieve CSRF token. Please try again.');
            }
        };

        // Check if CSRF token is available in cookies
        const csrfFromCookie = getCookie('csrftoken');
        if (csrfFromCookie) {
            setCsrfToken(csrfFromCookie);
        } else {
            fetchCsrfToken();
        }

        // Set up an axios instance with interceptors for token refresh
        const axiosInstance = axios.create();
        axiosInstance.interceptors.response.use(
            response => response,
            async error => {
                const originalRequest = error.config;
                if (error.response.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true;
                    const newAccessToken = await handleTokenRefresh(refreshToken);
                    if (newAccessToken) {
                        axios.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
                        return axiosInstance(originalRequest);
                    }
                }
                return Promise.reject(error);
            }
        );
    }, [onLogin]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!csrfToken) {
            setError("CSRF token not found. Unable to submit form.");
            return;
        }

        try {
            const response = await axios.post(
                'http://localhost:8000/auth/login/',
                { email, password },
                {
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
                    withCredentials: true,
                }
            );

            if (response.data.access && response.data.refresh) {
                localStorage.setItem('authToken', response.data.access);
                localStorage.setItem('refreshToken', response.data.refresh);
                setSuccess('Login successful!');
                setError('');
                setEmail(''); 
                setPassword('');
                if (typeof onLogin === 'function') {
                    onLogin(); // Call onLogin after successful login
                } else {
                    console.error('onLogin is not a function');
                }
                navigate('/');
            } else {
                throw new Error("Tokens not received from server.");
            }
        } catch (error) {
            console.error('Login error:', error);
            if (error.response) {
                setError(error.response.data.detail || 'An error occurred during login.');
            } else if (error.request) {
                setError('No response received from the server. Please try again.');
            } else {
                setError('An error occurred during login. Please try again.');
            }
            setSuccess('');
        }
    };

    return (
        <div className="main-container">
            <div className="form-container">
                <p className="title">Welcome back!</p>
                
                <form className="form" onSubmit={handleSubmit}>
                    <div className="input-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                        <div className="forgot">
                            <a href="#">Forgot Password?</a>
                        </div>
                    </div>
                    <button type="submit">Sign in</button>
                </form>

                {error && <p style={{ color: 'red' }}>{error}</p>}
                {success && <p style={{ color: 'green' }}>{success}</p>}
            

                <p className="signup">
                    Don't have an account? <a href="#">Sign up</a>
                </p>
            </div>
        </div>
    );
};

export default SignInForm;
