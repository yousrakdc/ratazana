import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Logout.css';

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

const Logout = ({ onLogout }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleLogout = async () => {
      try {
        const csrfToken = getCookie('csrftoken');
        console.log('Retrieved CSRF Token:', csrfToken);

        if (!csrfToken) {
          console.error('CSRF Token is missing. Unable to log out.');
          return;
        }

        console.log('Sending logout request...');
        const response = await axios.post(
          'http://localhost:8000/auth/logout/',
          {},
          {
            withCredentials: true,
            headers: {
              'X-CSRFToken': csrfToken,
            },
          }
        );

        if (response.status === 200) {
          console.log('Logout successful');

          if (onLogout) {
            onLogout(); // Call the onLogout function passed down from App
          }

          navigate('/login'); // Redirect to login after logout
        } else {
          console.error('Logout failed:', response.statusText);
        }
      } catch (error) {
        console.error('Logout error:', error);
      }
    };

    handleLogout();
  }, [onLogout, navigate]);

  return null; // No UI to render for this component
};

export default Logout; // Ensure this line exists
