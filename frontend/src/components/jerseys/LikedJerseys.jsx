import React, { useState, useEffect } from "react";
import { Link, Navigate } from "react-router-dom"; 
import styles from "./LikedJerseys.module.css"; 
import Heart from "./Heart"; 

const LikedJerseys = () => {
    const [likedJerseys, setLikedJerseys] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const authToken = localStorage.getItem("authToken");

    // Redirect if not logged in
    if (!authToken) {
        return <Navigate to="/login" />;
    }

    // Fetch liked jerseys and their price history
    const fetchLikedJerseys = async () => {
        try {
            const response = await fetch("http://localhost:8000/api/jerseys/likes/", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${authToken}`,
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error("Failed to fetch liked jerseys");
            }

            const data = await response.json();
            
            const jerseyPromises = data.map(async (jersey) => {
                const priceResponse = await fetch(`http://localhost:8000/api/jerseys/${jersey.id}/price-history/`, {
                    headers: {
                        "Authorization": `Bearer ${authToken}`,
                        "Content-Type": "application/json",
                    },
                });

                if (priceResponse.ok) {
                    const priceHistory = await priceResponse.json();
                    const priceChange = checkRecentPriceDrop(priceHistory, parseFloat(jersey.price));
                    return { ...jersey, ...priceChange };
                }
                return jersey;
            });

            const updatedJerseys = await Promise.all(jerseyPromises);
            setLikedJerseys(updatedJerseys);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    // Check if there was a price drop in the last 24 hours
    const checkRecentPriceDrop = (priceHistory, currentPrice) => {
        if (priceHistory.length === 0) {
            return { priceChangeStatus: 'no_change', priceChangePercentage: 0 };
        }

        const now = new Date();
        const twentyFourHoursAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000); // 24 hours ago

        const recentPricePoints = priceHistory.filter(pricePoint => new Date(pricePoint.date) >= twentyFourHoursAgo);
        const mostRecentPrice = recentPricePoints.length > 0 ? parseFloat(recentPricePoints[0].price) : parseFloat(priceHistory[0].price);
        currentPrice = parseFloat(currentPrice);
        const priceChangePercentage = ((mostRecentPrice - currentPrice) / mostRecentPrice * 100).toFixed(2);

        if (currentPrice < mostRecentPrice) {
            return { priceChangeStatus: 'decreased', priceChangePercentage: Math.abs(priceChangePercentage) };
        } else {
            return { priceChangeStatus: 'no_highlight', priceChangePercentage: 0 };
        }
    };

    useEffect(() => {
        fetchLikedJerseys();
    }, [authToken]);

    if (loading) return <p className={styles.loadingMessage}>Loading liked jerseys...</p>;
    if (error) return <p className={styles.errorMessage}>{error}</p>;

    return (
        <div className={styles.likedJerseysWrapper}>
            <h1>Keeping an eye on you...</h1>
            {likedJerseys.length > 0 ? (
                <div className={styles.likedJerseysList}>
                    {likedJerseys.map((jersey) => (
                        <div className={`${styles.likedJerseyItem} ${jersey.priceChangeStatus === 'decreased' ? styles.decreased : ''}`} key={jersey.id}>
                            <Link to={`/jerseys/${jersey.id}`}>
                                <div className={styles.likedJerseyImageWrapper}>
                                    {jersey.images && jersey.images.length > 0 ? (
                                        <img
                                            src={jersey.images[0].image_path}
                                            alt={jersey.team}
                                            className={styles.likedJerseyImage}
                                            onError={(e) => {
                                                if (!e.target.src.includes('placeholder')) {
                                                    e.target.src = 'https://via.placeholder.com/400';
                                                }
                                            }}
                                        />
                                    ) : (
                                        <p>No images available.</p>
                                    )}
                                </div>
                                <h2>{jersey.team}</h2>
                                {jersey.priceChangeStatus === 'decreased' && (
                                    <p className={`${styles.priceChangeMessage} ${styles.decreased}`}>
                                        Good news! Price dropped by {jersey.priceChangePercentage}%!
                                    </p>
                                )}
                            </Link>
                            <div className={styles.likedJerseyPriceContainer}>
                                <p className={styles.likedJerseyPrice}>£{jersey.price}</p>
                                <Heart jerseyId={jersey.id} initialLikedState={true} isAuthenticated={true} />
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <p>No liked jerseys found.</p>
            )}
        </div>
    );
};

export default LikedJerseys;
