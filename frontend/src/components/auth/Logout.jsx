import axios from 'axios';

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

const logout = async (onLogout, navigate) => {
    const csrfToken = getCookie('csrftoken');

    if (!csrfToken) {
        console.error('CSRF Token is missing. Unable to log out.');
        return;
    }

    try {
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
            onLogout(); // Trigger the logout function passed from the header
            navigate('/login'); // Navigate to login page after successful logout
        } else {
            console.error('Logout failed:', response.statusText);
        }
    } catch (error) {
        console.error('Logout error:', error);
    }
};

export default logout;
