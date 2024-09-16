import React, { useState } from 'react';
import './SignInForm.css';


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
    <div className="main-container">
      <div className="form-container">
        <p className="title">Welcome back!</p>
        <form className="form" onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              name="email"
              id="email"
              placeholder=""
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              name="password"
              id="password"
              placeholder=""
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <div className="forgot">
              <a rel="noopener noreferrer" href="#">Forgot Password?</a>
            </div>
          </div>
          <button className="sign">
            Sign in
          </button>
        </form>

        {error && <p style={{ color: 'red' }}>{error}</p>}
        {success && <p style={{ color: 'green' }}>{success}</p>}

        <div className="social-message">
          <div className="line"></div>
          <p className="message">Login with social accounts</p>
          <div className="line"></div>
        </div>

        <div className="social-icons">
          <button aria-label="Log in with Google" className="icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" className="w-5 h-5 fill-current">
              <path d="M16.318 13.714v5.484h9.078c-0.37 2.354-2.745 6.901-9.078 6.901-5.458 0-9.917-4.521-9.917-10.099s4.458-10.099 9.917-10.099c3.109 0 5.193 1.318 6.38 2.464l4.339-4.182c-2.786-2.599-6.396-4.182-10.719-4.182-8.844 0-16 7.151-16 16s7.156 16 16 16c9.234 0 15.365-6.49 15.365-15.635 0-1.052-0.115-1.854-0.255-2.651z"></path>
            </svg>
          </button>
        </div>

        <p className="signup">Don't have an account?
          <a rel="noopener noreferrer" href="#" className="">Sign up</a>
        </p>
      </div>
    </div>
  );
}

export default SignInForm;
