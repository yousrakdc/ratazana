import React from 'react';
import './Layout.css';
import Header from './Header'; // Import the Header component

const Layout = ({ children }) => {
  return (
    <div className="layout">
      <Header /> {/* This will render the Header component */}
      <main>{children}</main>
      <footer>
        <p>© 2024 Ratazana. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Layout;
