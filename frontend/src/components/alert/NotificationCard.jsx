import React from 'react';
import './NotificationCard.css';

const NotificationCard = ({ message, onClose }) => {
    return (
        <div className="notification-container show">
            <span className="notification-title">Oopsie...</span>
            <div className="notification-text">{message}</div>
            <button className="close-button" onClick={onClose}>Close</button>
        </div>
    );
};

export default NotificationCard;
