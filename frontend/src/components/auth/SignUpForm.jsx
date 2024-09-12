import React, { useState } from 'react';
import axios from 'axios';
import './SignUpForm.css';

function SignupForm() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [errors, setErrors] = useState({});

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/signup/', {
        username,
        email,
        password1,
        password2
      });
      // Handle successful signup (e.g., redirect, show a message)
      console.log('Signup successful:', response.data);
    } catch (error) {
      setErrors(error.response.data);
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
        {errors.username && <p>{errors.username}</p>}
      </div>
      <div>
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {errors.email && <p>{errors.email}</p>}
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={password1}
          onChange={(e) => setPassword1(e.target.value)}
        />
        {errors.password1 && <p>{errors.password1}</p>}
      </div>
      <div>
        <label>Confirm Password:</label>
        <input
          type="password"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
        />
        {errors.password2 && <p>{errors.password2}</p>}
      </div>
      <button>
          Sign up
          <div class="arrow-wrapper">
              <div class="arrow"></div>

          </div>
      </button>
    </form>
  );
}

export default SignupForm;
