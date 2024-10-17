import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Slider from 'react-slick';
import Heart from './Heart';
import './JerseyDetail.css';
import jwt_decode from 'jwt-decode'; 
import PriceTracker from '../data/PriceTracker'; 

function JerseyDetail() {
    const { id } = useParams();
    const [jersey, setJersey] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isLiked, setIsLiked] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [priceData, setPriceData] = useState([]); // State for price data
    const [isAlertSet, setIsAlertSet] = useState(false); // State to track if alert is set
    const [lastPrice, setLastPrice] = useState(null); // Track last price for comparison

    // Function to get CSRF token from cookies
    const getCsrfToken = () => {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='));
        return cookieValue ? cookieValue.split('=')[1] : null;
    };

    // Function to refresh access token if expired
    const refreshAccessToken = async (refreshToken) => {
        const csrfToken = getCsrfToken();
        const response = await fetch('http://localhost:8000/auth/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('authToken', data.access);
            return data.access;
        } else {
            throw new Error('Unable to refresh token');
        }
    };

    // Fetch jersey details and price history
    useEffect(() => {
        const fetchJersey = async () => {
            try {
                let token = localStorage.getItem('authToken');
                const refreshToken = localStorage.getItem('refreshToken');

                if (token) {
                    const decoded = jwt_decode(token);
                    const currentTime = Math.floor(Date.now() / 1000);
                    // Refresh token if expired
                    if (decoded.exp < currentTime && refreshToken) {
                        token = await refreshAccessToken(refreshToken);
                    }
                }

                const csrfToken = getCsrfToken();
                const headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token ? `Bearer ${token}` : '',
                    'X-CSRFToken': csrfToken,
                };

                // Fetch jersey data
                const jerseyResponse = await fetch(`http://localhost:8000/api/jerseys/${id}/`, {
                    headers: headers,
                });

                if (!jerseyResponse.ok) {
                    throw new Error(`Error fetching jersey data: ${jerseyResponse.statusText}`);
                }

                const jerseyData = await jerseyResponse.json();
                console.log('Fetched Jersey Data:', jerseyData); // Log the entire jersey object
                setJersey(jerseyData);
                setLastPrice(jerseyData.price); // Set the initial price for comparison

                // Log the original URL for debugging
                console.log('Original URL:', jerseyData.original_url || 'No URL available');

                // Fetch price history data
                const priceResponse = await fetch(`http://localhost:8000/api/jerseys/${id}/price-history/`, {
                    headers: headers,
                });
                if (!priceResponse.ok) {
                    throw new Error(`Error fetching price history: ${priceResponse.statusText}`);
                }

                const priceHistory = await priceResponse.json();
                console.log('Fetched price history:', priceHistory);
                setPriceData(priceHistory);

                // Fetch likes data only if authenticated
                if (token) {
                    const likesResponse = await fetch(`http://localhost:8000/api/jerseys/${id}/likes/`, {
                        headers: headers,
                    });
                    if (likesResponse.ok) {
                        const likesData = await likesResponse.json();
                        setIsLiked(likesData.is_liked);
                    }
                }
            } catch (error) {
                console.error('Error fetching jersey:', error);
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchJersey();
    }, [id]);

    useEffect(() => {
        const token = localStorage.getItem('authToken');
        setIsAuthenticated(!!token);
    }, []);

    // New function to handle setting the alert for price decrease
    const handleSetAlert = () => {
        if (isAlertSet) {
            alert("Price alert is already set!");
            return;
        }

        // Set an alert for price decrease
        setIsAlertSet(true);
        alert("Price alert is set! You will be notified if the price decreases.");
    };

    // Function to check price decrease
    const checkPriceDecrease = () => {
        if (jersey && lastPrice !== null && jersey.price < lastPrice) {
            alert(`Price decreased! New price: £${jersey.price}`);
            setLastPrice(jersey.price); // Update the last price
        }
    };

    // Set an interval to check for price decrease every minute (or set as needed)
    useEffect(() => {
        const intervalId = setInterval(() => {
            checkPriceDecrease();
        }, 60000); // Check every 60 seconds

        return () => clearInterval(intervalId); // Clear the interval on unmount
    }, [jersey]);

    const handleToggleLike = (liked) => {
        setIsLiked(liked);
    };

    // Loading and error handling
    if (loading) {
        return <div>Loading...</div>;
    }
    if (error) {
        return <div>Error: {error}</div>;
    }
    if (!jersey) {
        return <div>Jersey not found</div>;
    }

    // Process sizes from jersey data
    let processedSizes = [];
    if (jersey.sizes) {
        if (typeof jersey.sizes === 'string') {
            processedSizes = jersey.sizes.split('/').map(size => size.trim()).filter(size => size);
        } else if (Array.isArray(jersey.sizes)) {
            processedSizes = jersey.sizes.map(size => size.toString().trim()).filter(size => size);
        }
    }

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
    };

    return (
        <div className="jersey-details-container">
            <div className="image-carousel">
                {jersey.images && jersey.images.length > 0 ? (
                    <Slider {...settings}>
                        {jersey.images.map((image, index) => (
                            <div key={index}>
                                <img
                                    src={`http://localhost:8000${image.image_path}`}
                                    alt={jersey.team}
                                    className="jersey-image"
                                />
                            </div>
                        ))}
                    </Slider>
                ) : (
                    <p>No images available.</p>
                )}
            </div>
            <h1 className="jersey-name">{jersey.team} - {jersey.brand} ({jersey.season})</h1>

            {/* Jersey description */}
            <p className="jersey-description">{jersey.description || "Description not available."}</p>

            {/* New container for sizes, price, and heart */}
            <div className="size-price-heart-container">
                {/* Available sizes */}
                {processedSizes.length > 0 ? (
                    <div className="jersey-sizes">
                        <strong>Available Sizes: </strong>
                        {processedSizes.join(', ')}
                    </div>
                ) : (
                    <p>Sizes not available.</p>
                )}

                {/* Price and Heart */}
                <div className="price-heart-container">
                    <p className="jersey-price">Price: £{jersey.price || "Price not available."}</p>
                    <Heart
                        jerseyId={jersey.id}
                        isLiked={isLiked}
                        onToggleLike={handleToggleLike}
                        isAuthenticated={isAuthenticated}
                    />
                </div>
            </div>

            {/* Set Price Alert Button */}
            {isAuthenticated && (
                <button onClick={handleSetAlert}>Set Price Alert</button>
            )}

            {/* View on Nike button with validation */}
            {jersey.original_url && jersey.original_url.startsWith('http') ? (
                <a
                    href={jersey.original_url}
                    className="nike-button"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    View on Nike
                </a>
            ) : (
                <a
                    href="https://www.nike.com"
                    className="nike-button"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    View on Nike (Default)
                </a>
            )}

            {priceData.length > 0 ? (
                <PriceTracker priceData={priceData} />
            ) : (
                <div>No price data available.</div>
            )}
        </div>
    );
}

export default JerseyDetail;
