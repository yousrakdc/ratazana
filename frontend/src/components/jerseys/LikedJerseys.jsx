import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import styles from "./LikedJerseys.module.css"; // Ensure your CSS file is correctly imported
import Heart from "./Heart"; // Import your Heart component for like functionality

const LikedJerseys = () => {
    const [likedJerseys, setLikedJerseys] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const authToken = localStorage.getItem("authToken");

    // Fetch liked jerseys from the API
    const fetchLikedJerseys = async () => {
        if (!authToken) {
            alert("You need to log in to see your liked jerseys.");
            return;
        }

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
            console.log('Fetched Liked Jerseys:', data); // Log the full response data for debugging
            setLikedJerseys(data); // Assuming the API returns a list of jerseys
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLikedJerseys();
    }, [authToken]);

    // Loading and error handling
    if (loading) return <p className={styles.loadingMessage}>Loading liked jerseys...</p>;
    if (error) return <p className={styles.errorMessage}>{error}</p>;

    return (
        <div className={styles.likedJerseysWrapper}>
            <h1>Keeping an eye on you...</h1>
            {likedJerseys.length > 0 ? (
                <div className={styles.likedJerseysList}>
                    {likedJerseys.map((jersey) => (
                        <div className={styles.likedJerseyItem} key={jersey.id}>
                            <Link to={`/jerseys/${jersey.id}`}>
                                <div className={styles.likedJerseyImageWrapper}>
                                    {jersey.images && jersey.images.length > 0 ? (
                                        <img
                                            src={jersey.images[0].image_path} // Directly use the full URL from the data
                                            alt={jersey.team}
                                            className={styles.likedJerseyImage}
                                            onError={(e) => {
                                                // Prevent further error handling after the first failure
                                                if (!e.target.src.includes('placeholder')) {
                                                    console.error(`Image failed to load: ${e.target.src}`);
                                                    e.target.src = 'https://via.placeholder.com/400'; // Use a valid fallback image URL
                                                }
                                            }}
                                        />
                                    ) : (
                                        <p>No images available.</p>
                                    )}
                                </div>
                                <h2>{jersey.team}</h2>
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
