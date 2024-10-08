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
            console.log(`Checking cookie: ${cookie}`);
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                console.log(`Found CSRF Token in cookie: ${cookieValue}`); // Log found CSRF token
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

    useEffect(() => {
        const fetchCsrfToken = async () => {
            try {
                const response = await axios.get('http://localhost:8000/auth/api/csrf-token/', { withCredentials: true });
                setCsrfToken(response.data.csrfToken);
                console.log('CSRF Token retrieved from server:', response.data.csrfToken); // Log retrieved CSRF token
            } catch (error) {
                console.error('Error fetching CSRF token from server:', error);
            }
        };

        const csrfFromCookie = getCookie('csrftoken');
        if (csrfFromCookie) {
            setCsrfToken(csrfFromCookie);
            console.log('CSRF Token retrieved from cookie:', csrfFromCookie); // Log retrieved CSRF token from cookie
        } else {
            fetchCsrfToken();
        }

        // Check login status on component mount
        const checkLoginStatus = async () => {
            try {
                const response = await axios.get('http://localhost:8000/auth/check-login/', { withCredentials: true });
                setIsLoggedIn(response.data.isLoggedIn);
            } catch (error) {
                console.error('Error checking login status:', error);
            }
        };

        checkLoginStatus();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log('Attempting to submit form with CSRF Token:', csrfToken);
        console.log('Payload being sent:', { email, password });

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
                        'X-CSRFToken': csrfToken,  // Correctly sending CSRF token
                    },
                    withCredentials: true,
                }
            );

            console.log('Login successful:', response.data);
            setSuccess('Login successful!');
            setError('');
            setIsLoggedIn(true); // Update the login state

            // Clear the input fields after successful login
            setEmail('');
            setPassword('');
        } catch (error) {
            console.error('Login error:', error);
            if (error.response && error.response.data) {
                setError(error.response.data.detail || 'An error occurred.');
            } else {
                setError('An error occurred during login.');
            }
            setSuccess('');
        }
    };

    // Logout function
    const handleLogout = async () => {
        console.log('Attempting to log out with CSRF Token:', csrfToken); // Log the CSRF token before logout

        try {
            const response = await axios.post(
                'http://localhost:8000/auth/logout/',
                {}, // Empty payload for logout
                {
                    headers: {
                        'X-CSRFToken': csrfToken, // Include CSRF token
                    },
                    withCredentials: true,
                }
            );

            console.log('Logout successful:', response.data);
            setSuccess('Logout successful!');
            setError('');
            setIsLoggedIn(false); // Update the login state
        } catch (error) {
            console.error('Logout error:', error);

            if (error.response) {
                // Log the full response for debugging
                console.error('Full response:', error.response);
                setError(error.response.data.detail || 'An error occurred during logout.');
            } else {
                setError('An error occurred during logout.');
            }
        }
    };

    return (
        <div className="main-container">
            <div className="form-container">
                <p className="title">Welcome back!</p>
                
                {/* Show either login form or logout button based on login state */}
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
                    <button onClick={handleLogout}>Logout</button> // Logout button after successful login
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
