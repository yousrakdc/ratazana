import React, { useState, useEffect } from 'react';
import axios from 'axios';
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
    } catch (error) {
      if (error.response && error.response.data) {
        setErrors(error.response.data);
      } else {
        console.error('Signup error:', error);
        setErrors({ detail: 'An error occurred during signup.' });
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="signup-form">
      <div>
        <label>Username:</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        {errors.username && <p style={{ color: 'red' }}>{errors.username}</p>}
      </div>
      <div>
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {errors.email && <p style={{ color: 'red' }}>{errors.email}</p>}
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={password1}
          onChange={(e) => setPassword1(e.target.value)}
        />
        {errors.password1 && <p style={{ color: 'red' }}>{errors.password1}</p>}
      </div>
      <div>
        <label>Confirm Password:</label>
        <input
          type="password"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
        />
        {errors.password2 && <p style={{ color: 'red' }}>{errors.password2}</p>}
      </div>
      <button type="submit">
        Sign up
        <div className="arrow-wrapper">
          <div className="arrow"></div>
        </div>
      </button>
      {errors.detail && <p style={{ color: 'red' }}>{errors.detail}</p>}
    </form>
  );
}

export default SignUpForm;
