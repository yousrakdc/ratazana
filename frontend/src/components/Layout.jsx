import React from 'react';
import Header from './Header';
import './Layout.css';

const Layout = ({ children, isLoggedIn, onLogout }) => {
    console.log('Layout isLoggedIn before rendering:', isLoggedIn); // Debugging line
    return (
        <div className="layout">
            <Header isLoggedIn={isLoggedIn} onLogout={onLogout} />
            <main>{children}</main>
            <footer>
                <p>© 2024 Ratazana. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default Layout;
