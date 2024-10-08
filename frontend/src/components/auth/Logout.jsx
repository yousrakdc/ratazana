import React from 'react';

const Logout = ({ onLogout }) => {
    const handleLogoutClick = () => {
        console.log('Logout button clicked'); // Log when logout is clicked
        onLogout();
    };

    return (
        <button onClick={handleLogoutClick}>Logout</button>
    );
};

export default Logout;
