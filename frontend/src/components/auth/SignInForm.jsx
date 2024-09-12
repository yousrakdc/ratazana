import React, { useState } from 'react';

function SignInForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent the default form submission
    console.log("Form submitted");

    fetch('http://localhost:8000/auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include'  // Include credentials (cookies) in the request
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (data.access) {
        // Successful login
        console.log("Login successful");
        setSuccess('Login successful!');
        setError(''); // Clear any previous errors
      } else {
        // Handle errors returned from the backend
        console.error("Login error:", data.detail || "Unknown error");
        setError(data.detail || "An error occurred");
        setSuccess(''); // Clear any previous success messages
      }
    })
    .catch(error => {
      console.error("Network or server error:", error);
      setError("Network error or server issue.");
      setSuccess(''); // Clear any previous success messages
    });
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button>
            Sign in
            <div class="arrow-wrapper">
                <div class="arrow"></div>

            </div>
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
    </div>
  );
};

export default SignInForm;
