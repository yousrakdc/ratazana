import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Slider from 'react-slick';
import Heart from './Heart';
import './JerseyDetail.css';
import jwt_decode from 'jwt-decode'; 
import PriceTracker from '../data/PriceTracker'; 
import NotificationCard from '../alert/NotificationCard'; 

function JerseyDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [jersey, setJersey] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isLiked, setIsLiked] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [priceData, setPriceData] = useState([]);
    const [lastPrice, setLastPrice] = useState(null);
    const [alertMessage, setAlertMessage] = useState(null);
    const [priceDropMessage, setPriceDropMessage] = useState(null);
    const [temporaryButtonText, setTemporaryButtonText] = useState('Price Drop Alert');

    const getCsrfToken = () => {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='));
        return cookieValue ? cookieValue.split('=')[1] : null;
    };

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

    useEffect(() => {
        const fetchJersey = async () => {
            try {
                let token = localStorage.getItem('authToken');
                const refreshToken = localStorage.getItem('refreshToken');

                if (token) {
                    const decoded = jwt_decode(token);
                    const currentTime = Math.floor(Date.now() / 1000);
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

                const jerseyResponse = await fetch(`http://localhost:8000/api/jerseys/${id}/`, {
                    headers: headers,
                });

                if (!jerseyResponse.ok) {
                    throw new Error(`Error fetching jersey data: ${jerseyResponse.statusText}`);
                }

                const jerseyData = await jerseyResponse.json();
                setJersey(jerseyData);
                setLastPrice(jerseyData.price);

                const priceResponse = await fetch(`http://localhost:8000/api/jerseys/${id}/price-history/`, {
                    headers: headers,
                });
                if (!priceResponse.ok) {
                    throw new Error(`Error fetching price history: ${priceResponse.statusText}`);
                }

                const priceHistory = await priceResponse.json();
                setPriceData(priceHistory);
                checkPriceDecrease(priceHistory, parseFloat(jerseyData.price));

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

    const checkPriceDecrease = (priceHistory, currentPrice) => {
        currentPrice = parseFloat(currentPrice);
    
        if (priceHistory.length === 0) {
            setPriceDropMessage(null);
            return;
        }
    
        const oldestPrice = parseFloat(priceHistory[0].price);
        const highestPrice = Math.max(...priceHistory.map(record => parseFloat(record.price)));
    
        if (currentPrice < oldestPrice) {
            const decreasePercentage = ((oldestPrice - currentPrice) / oldestPrice * 100).toFixed(2);
            const message = `Price dropped by ${decreasePercentage}% since ${new Date(priceHistory[0].date).toLocaleDateString()}! New price: £${currentPrice}`;
            setPriceDropMessage(message);
        } else if (currentPrice < highestPrice) {
            const decreasePercentage = ((highestPrice - currentPrice) / highestPrice * 100).toFixed(2);
            const message = `Price is down ${decreasePercentage}% from its peak of £${highestPrice}!`;
            setPriceDropMessage(message);
        } else {
            setPriceDropMessage(null);
        }
    };

    const handleToggleLike = async (liked) => {
        setIsLiked(liked);
        const message = liked ? "You liked this jersey! Price alert is set." : "You unliked this jersey.";
        console.log("Setting alert message:", message);
        setAlertMessage(message);
        
        clearTimeout(window.notificationTimeout);
        
        window.notificationTimeout = setTimeout(() => {
            setAlertMessage(null);
        }, 3000);
        
        console.log("Alert message state updated:", alertMessage);
    };

    const handleCloseNotification = () => {
        setAlertMessage(null);
        setPriceDropMessage(null);
    };

    const handleTemporaryButtonClick = async () => {
        const token = localStorage.getItem('authToken');
    
        try {
            const response = await fetch(`http://localhost:8000/api/jerseys/${id}/temporary-price-drop/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                    'X-CSRFToken': getCsrfToken(),
                },
            });
    
            if (response.ok) {
                console.log("Price dropped successfully!");
            } else {
                console.error("Error triggering price drop:", response.statusText);
            }
        } catch (error) {
            console.error("Error triggering price drop", error);
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }
    if (error) {
        return <div>Error: {error}</div>;
    }
    if (!jersey) {
        return <div>Jersey not found</div>;
    }

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
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
    };

    return (
        <div className="jersey-details-page">
            <div className="jersey-details-container">
                {priceDropMessage && (
                    <div className="price-drop-alert">
                        <strong>{priceDropMessage}</strong>
                    </div>
                )}
                {alertMessage && (
                    <NotificationCard 
                        message={alertMessage} 
                        onClose={handleCloseNotification} 
                    />
                )}

                <div className="details-layout">
                    {/* Return Button on the left side */}
                    <button className="return-button" onClick={() => navigate('/jerseys')}>
                        <div className="button-box">
                            <span className="button-elem">
                                <svg viewBox="0 0 46 40" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3 .8 4.4-.3l16-17c .5-.5 .8-1 .8-1 .9z"></path>
                                </svg>
                            </span>
                            <span className="button-elem">
                                <svg viewBox="0 0 46 40">
                                    <path d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3 .8 4.4-.3l16-17c .5-.5 .8-1 .8-1 .9z"></path>
                                </svg>
                            </span>
                        </div>
                    </button>

                    {/* Image Carousel */}
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

                    {/* Jersey Info */}
                    <div className="jersey-info">
                        <h1 className="jersey-name">{jersey.team} - {jersey.brand} ({jersey.season})</h1>
                        <p className="jersey-description">{jersey.description || "Description not available."}</p>

                        <div className="size-price-heart-container">
                            {processedSizes.length > 0 ? (
                                <div className="jersey-sizes">
                                    <strong>Available Sizes: </strong>
                                    {processedSizes.join(', ')}
                                </div>
                            ) : (
                                <p>Sizes not available.</p>
                            )}
                            <div className="price-heart-container">
                                <p className="jersey-price">Price: £{jersey.price || "Price not available."}</p>
                                <Heart
                                    jerseyId={jersey.id}
                                    initialLikedState={isLiked}
                                    onToggleLike={handleToggleLike}
                                    isAuthenticated={isAuthenticated}
                                />
                            </div>
                        </div>

                        {jersey.original_url && jersey.original_url.startsWith('http') ? (
                            <button 
                                className="nike-button" 
                                style={{ "--clr": "#7808d0" }} 
                                onClick={() => window.open(jersey.original_url, '_blank')}
                            >
                                <span className="nike-button__icon-wrapper">
                                    <svg
                                        viewBox="0 0 14 15"
                                        fill="none"
                                        xmlns="http://www.w3.org/2000/svg"
                                        className="button__icon-svg"
                                        width="10"
                                    >
                                        <path
                                            d="M13.376 11.552l-.264-10.44-10.44-.24.024 2.28 6.96-.048L.2 12.56l1.488 1.488 9.432-9.432-.048 6.912 2.304.024z"
                                            fill="currentColor"
                                        ></path>
                                    </svg>
                                </span>
                                View on Nike.com
                            </button>
                        ) : (
                            <p>No purchase link available.</p>
                        )}
                    </div>
                </div>

                {lastPrice && (
                    <PriceTracker 
                        priceData={priceData} 
                        lastPrice={lastPrice} 
                    />
                )}

                {/* Temporary Button */}
                <button onClick={handleTemporaryButtonClick} className="temp-button">
                    {temporaryButtonText}
                </button>
                
            </div>
        </div>
    );      
}

export default JerseyDetail;
