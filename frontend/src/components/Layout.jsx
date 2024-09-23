import React from 'react';
import { Link } from 'react-router-dom';
import './Layout.css';
import './jerseys/JerseyCard.css';
import logo from './landing_page/images/logo.png';

const Layout = ({ children }) => {
  return (
    <div className="layout">
      <header>
        <div className="logo">
          <Link to="/">
            <img src={logo} alt="Ratazana" className="logo-image" />
            </Link>
        </div>
        <div className="search">
            <input placeholder="Search" className="search__input" type="text" />
            <button className="search__button">
                <svg
                viewBox="0 0 16 16"
                className="bi bi-search"
                fill="currentColor"
                height="16"
                width="16"
                xmlns="http://www.w3.org/2000/svg"
                >
                <path
                    d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"
                ></path>
                </svg>
            </button>
            </div>

        <nav className="menu">
          <Link to="/jerseys">Shop</Link>
          <Link to="/signup">Sign Up</Link>
          <Link to="/login">Sign In</Link>
        </nav>
      </header>
      
      <main>{children}</main>

      <footer>
        <p>© 2024 Ratazana. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Layout;