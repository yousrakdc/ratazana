import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SignInForm.css';

// Function to retrieve CSRF token from cookies
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

const SignInForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [csrfToken, setCsrfToken] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    // Function to check JWT token validity
    const isTokenExpired = (token) => {
        if (!token) return true; // No token means expired
        const payload = JSON.parse(atob(token.split('.')[1]));
        return (payload.exp * 1000) < Date.now();
    };

    // Refresh the access token
    const handleTokenRefresh = async (refreshToken) => {
        try {
            const response = await axios.post(
                'http://localhost:8000/auth/token/refresh/', // Correct endpoint
                { refresh: refreshToken },
                { withCredentials: true } // Ensure cookies are sent with the request
            );

            const newAccessToken = response.data.access;
            localStorage.setItem('authToken', newAccessToken);
            setIsLoggedIn(true);
            return newAccessToken; // Return new access token
        } catch (error) {
            console.error('Token refresh error:', error);
            // Handle specific error cases
            if (error.response) {
                console.error('Refresh Token Error:', error.response.data);
                if (error.response.status === 401 || error.response.status === 403) {
                    // Token refresh failed, clear tokens
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('refreshToken');
                    setIsLoggedIn(false);
                    setError('Your session has expired. Please log in again.');
                }
            }
            return null; // Return null if refresh failed
        }
    };

    useEffect(() => {
        const authToken = localStorage.getItem('authToken');
        const refreshToken = localStorage.getItem('refreshToken');

        // If the access token is valid, set the user as logged in
        if (authToken && !isTokenExpired(authToken)) {
            setIsLoggedIn(true);
        } 
        // If the access token is expired, try refreshing it
        else if (refreshToken) {
            handleTokenRefresh(refreshToken);
        }

        // Fetch CSRF token from server
        const fetchCsrfToken = async () => {
            try {
                const response = await axios.get('http://localhost:8000/auth/api/csrf-token/', { withCredentials: true });
                setCsrfToken(response.data.csrfToken);
            } catch (error) {
                console.error('Error fetching CSRF token from server:', error);
                setError('Could not retrieve CSRF token. Please try again.');
            }
        };

        const csrfFromCookie = getCookie('csrftoken');
        if (csrfFromCookie) {
            setCsrfToken(csrfFromCookie);
        } else {
            fetchCsrfToken();
        }

        // Set up Axios interceptors to handle token refresh on 401
        const axiosInstance = axios.create();
        axiosInstance.interceptors.response.use(
            response => response,
            async error => {
                const originalRequest = error.config;
                // Check for 401 Unauthorized error and if we haven't already tried to refresh the token
                if (error.response.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true; // Mark the request as retried
                    const newAccessToken = await handleTokenRefresh(refreshToken);
                    if (newAccessToken) {
                        // Update the Authorization header and retry the original request
                        axios.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
                        return axiosInstance(originalRequest);
                    }
                }
                return Promise.reject(error);
            }
        );
    }, []);

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

            // Ensure the tokens are in the response
            if (response.data.access && response.data.refresh) {
                localStorage.setItem('authToken', response.data.access);
                localStorage.setItem('refreshToken', response.data.refresh); // Store the refresh token
                setSuccess('Login successful!');
                setError('');
                setIsLoggedIn(true);
                setEmail(''); // Clear email
                setPassword(''); // Clear password
            } else {
                throw new Error("Tokens not received from server.");
            }
        } catch (error) {
            console.error('Login error:', error);
            if (error.response) {
                console.error('Error response:', error.response);
                console.error('Error data:', error.response.data);
                setError(error.response.data.detail || 'An error occurred during login.');
            } else if (error.request) {
                console.error('Error request:', error.request);
                setError('No response received from the server. Please try again.');
            } else {
                console.error('Error message:', error.message);
                setError('An error occurred during login. Please try again.');
            }
            setSuccess('');
        }
    };

    const handleLogout = async () => {
        const csrfToken = getCookie('csrftoken');
        const authToken = localStorage.getItem('authToken');
    
        if (!csrfToken || !authToken) {
            console.error('CSRF token or Auth token not found. Cannot log out.');
            setError("Unable to log out. Please try again.");
            return;
        }
    
        try {
            const response = await axios.post(
                'http://localhost:8000/auth/logout/',
                {},
                {
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Authorization': `Bearer ${authToken}`
                    },
                    withCredentials: true,
                }
            );
    
            console.log('Logout successful:', response.data);
            setSuccess('Logout successful!');
            setError('');
            setIsLoggedIn(false);
            localStorage.removeItem('authToken');
            localStorage.removeItem('refreshToken');
        } catch (error) {
            console.error('Logout error:', error);
            setError(error.response?.data?.detail || 'An error occurred during logout.');
        }
    };
    
    

    return (
        <div className="main-container">
            <div className="form-container">
                <p className="title">Welcome back!</p>
                {!isLoggedIn ? (
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
                ) : (
                    <button onClick={handleLogout}>Logout</button>
                )}
                {error && <p style={{ color: 'red' }}>{error}</p>}
                {success && <p style={{ color: 'green' }}>{success}</p>}
                <div className="social-message">
                    <div className="line"></div>
                    <p className="message">Login with social accounts</p>
                    <div className="line"></div>
                </div>
                <div className="social-icons">
                    <button aria-label="Log in with Google" className="icon">
                        {/* Add your Google login icon SVG here */}
                    </button>
                </div>
                <p className="signup">
                    Don't have an account? <a href="#">Sign up</a>
                </p>
            </div>
        </div>
    );
};

export default SignInForm;
