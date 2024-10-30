import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Layout.css';
import logo from './landing_page/images/logo.png';
import NotificationCard from './alert/NotificationCard';

const Header = ({ isLoggedIn, onLogout }) => {
    const navigate = useNavigate();
    const [notificationMessage, setNotificationMessage] = useState('');
    const [isNotificationVisible, setIsNotificationVisible] = useState(false);

    const handleMyJerseysClick = (e) => {
        if (!isLoggedIn) {
            e.preventDefault();
            setNotificationMessage("You need to log in to see your liked jerseys.");
            setIsNotificationVisible(true);
        }
    };

    const closeNotification = () => {
        setIsNotificationVisible(false);
    };

    const handleLogout = async () => {
        if (onLogout && typeof onLogout === "function") {
            await onLogout();
        } else {
            console.error("onLogout is not a function");
        }
    };

    return (
        <header>
            <div className="logo">
                <Link to="/">
                    <img src={logo} alt="Ratazana" className="logo-image" />
                </Link>
            </div>
            <div className="search">
                <input placeholder="Search" className="search__input" type="text" />
                <button className="search__button">
                    <svg viewBox="0 0 16 16" className="bi bi-search" fill="currentColor" height="16" width="16" xmlns="http://www.w3.org/2000/svg">
                        <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"></path>
                    </svg>
                </button>
            </div>
            <nav className="menu">
                <Link to="/jerseys">Shop</Link>
                <Link to="/liked-jerseys" onClick={handleMyJerseysClick}>My Jerseys</Link>
                {isLoggedIn ? (
                    <button onClick={handleLogout} className="logout-button">Logout</button>
                ) : (
                    <>
                        <Link to="/signup">Sign Up</Link>
                        <Link to="/login">Sign In</Link>
                    </>
                )}
            </nav>
            {isNotificationVisible && (
                <NotificationCard 
                    message={notificationMessage} 
                    onClose={closeNotification} 
                    isVisible={isNotificationVisible} 
                />
            )}
        </header>
    );
};

export default Header;
