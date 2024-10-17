import React, { useState, useEffect } from "react";
import styled from "styled-components";
import jwtDecode from "jwt-decode"; // Ensure this package is installed with `npm install jwt-decode`

// Function to get CSRF token from cookies (if needed)
const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// Function to refresh the auth token using the refresh token
const refreshAuthToken = async () => {
    const refreshToken = localStorage.getItem("refreshToken");
    if (!refreshToken) {
        console.error("No refresh token found.");
        return null;
    }

    try {
        const response = await fetch("http://localhost:8000/api/token/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (!response.ok) {
            console.error("Failed to refresh token", response.statusText);
            return null;
        }

        const data = await response.json();
        localStorage.setItem("authToken", data.access); // Update localStorage with new token
        console.log("New token fetched:", data.access);
        return data.access; // Return the new token
    } catch (error) {
        console.error("Error refreshing token:", error);
        return null;
    }
};

const Heart = ({ jerseyId, initialLikedState, isAuthenticated }) => {
    const [liked, setLiked] = useState(initialLikedState);
    const [authToken, setAuthToken] = useState(localStorage.getItem("authToken"));
    const csrfToken = getCookie("csrftoken");

    const isTokenExpired = (token) => {
        if (!token) return true;
        const decodedToken = jwtDecode(token);
        return decodedToken.exp < Date.now() / 1000;
    };

    useEffect(() => {
        setLiked(initialLikedState);
    }, [initialLikedState]);

    const ensureValidAuthToken = async () => {
        if (isTokenExpired(authToken)) {
            console.log("Token has expired, attempting to refresh...");
            const newToken = await refreshAuthToken();
            if (newToken) {
                setAuthToken(newToken);
                return newToken;
            } else {
                alert("Session expired. Please log in again.");
                return null;
            }
        }
        return authToken;
    };

    const handleLikeToggle = async () => {
        if (!isAuthenticated) {
            alert("Please log in to like a jersey.");
            return;
        }

        const validAuthToken = await ensureValidAuthToken();
        if (!validAuthToken) return;

        const newLikedState = !liked;  // Toggle the liked state
        setLiked(newLikedState); // Update the state immediately

        try {
            const url = `http://localhost:8000/api/jerseys/${jerseyId}/likes/`;
            const method = newLikedState ? "POST" : "DELETE";

            const response = await fetch(url, {
                method: method,
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${validAuthToken}`, // Correct format for JWT
                    "X-CSRFToken": csrfToken,
                },
                body: newLikedState ? JSON.stringify({ jersey: jerseyId }) : null,
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error("Failed to update like:", errorData);
                throw new Error("Failed to update like");
            }

            console.log(`Jersey ${jerseyId} is now ${newLikedState ? "liked" : "unliked"}.`);
        } catch (error) {
            console.error("Error updating like:", error);
            alert("An error occurred while trying to like/unlike the jersey.");
            setLiked(!newLikedState); // Roll back to previous state on error
        }
    };

    return (
        <StyledWrapper>
            <div title="Like" className="heart-container" onClick={handleLikeToggle}>
                <div className="svg-container">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className={`svg-outline ${liked ? "hidden" : ""}`}
                        viewBox="0 0 24 24"
                    >
                        <path d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Zm-3.585,18.4a2.973,2.973,0,0,1-3.83,0C4.947,16.006,2,11.87,2,8.967a4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,11,8.967a1,1,0,0,0,2,0,4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,22,8.967C22,11.87,19.053,16.006,13.915,20.313Z"></path>
                    </svg>
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className={`svg-filled ${liked ? "" : "hidden"}`}
                        viewBox="0 0 24 24"
                    >
                        <path d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Z"></path>
                    </svg>
                </div>
            </div>
        </StyledWrapper>
    );
};

const StyledWrapper = styled.div`
    .heart-container {
        cursor: pointer; /* Change cursor to pointer to indicate clickability */
        display: inline-flex; /* Align heart properly */
    }

    .svg-container {
        width: 25px; /* Adjust size as needed */
        height: 25px; /* Adjust size as needed */
    }

    .svg-outline,
    .svg-filled {
        fill: rgba(150, 107, 188, 0.5);
        transition: opacity 0.3s ease;
    }

    .hidden {
        display: none; /* Hide the heart when unliked */
    }
`;

export default Heart;
