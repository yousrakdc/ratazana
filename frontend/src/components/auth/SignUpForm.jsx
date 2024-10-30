import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SignUpForm.css';

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

function SignUpForm() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password1, setPassword1] = useState('');
    const [password2, setPassword2] = useState('');
    const [errors, setErrors] = useState({});
    const [csrfToken, setCsrfToken] = useState('');
    const navigate = useNavigate();

    // Get CSRF token from the server when the component mounts
    useEffect(() => {
        const fetchCsrfToken = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/csrf-token/');
                setCsrfToken(response.data.csrfToken);
                console.log("Retrieved CSRF Token:", response.data.csrfToken);
            } catch (error) {
                console.error('Error fetching CSRF token:', error);
            }
        };

        fetchCsrfToken();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!csrfToken) {
            console.error('CSRF Token is missing');
            setErrors({ detail: 'CSRF token is missing.' });
            return;
        }

        try {
            const response = await axios.post(
                'http://127.0.0.1:8000/auth/signup/',
                {
                    username,
                    email,
                    password1,
                    password2
                },
                {
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    withCredentials: true
                }
            );

            console.log('Signup successful:', response.data);
            // check for the access token and refresh token
            if (response.data && response.data.access) {
                localStorage.setItem('authToken', response.data.access);  
                localStorage.setItem('refreshToken', response.data.refresh);
                navigate('/');
            }
        } catch (error) {
            console.error('Signup error:', error);
            if (error.response && error.response.data) {
                setErrors(error.response.data);
            } else {
                setErrors({ detail: 'An error occurred during sign-up.' });
            }
        }
    };

    return (
        <div className="main-container">
            <div className="form-container">
                <p className="title">Welcome</p>
                <form className="form" onSubmit={handleSubmit}>
                    <div className="input-group">
                        <label htmlFor="username">Username</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                        {errors.username && <p style={{ color: 'red' }}>{errors.username[0]}</p>}
                    </div>
                    <div className="input-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                        {errors.email && <p style={{ color: 'red' }}>{errors.email[0]}</p>}
                    </div>
                    <div className="input-group">
                        <label htmlFor="password1">Password</label>
                        <input
                            type="password"
                            id="password1"
                            value={password1}
                            onChange={(e) => setPassword1(e.target.value)}
                            required
                        />
                        {errors.password1 && <p style={{ color: 'red' }}>{errors.password1[0]}</p>}
                    </div>
                    <div className="input-group">
                        <label htmlFor="password2">Confirm Password</label>
                        <input
                            type="password"
                            id="password2"
                            value={password2}
                            onChange={(e) => setPassword2(e.target.value)}
                            required
                        />
                        {errors.password2 && <p style={{ color: 'red' }}>{errors.password2[0]}</p>}
                    </div>
                    <button type="submit">Sign Up</button>
                </form>
                {errors.detail && <p style={{ color: 'red' }}>{errors.detail}</p>}

                <p className="signup">
                    Already have an account? <a href="#">Sign in</a>
                </p>
            </div>
        </div>
    );
}

export default SignUpForm;
