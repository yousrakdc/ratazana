import React, { useState, useEffect } from "react";
import Heart from "./Heart"; // Ensure this path is correct
import './JerseyCard.css';

const JerseyCard = ({ jersey }) => {
    const [liked, setLiked] = useState(false);

    // Check local storage to see if this jersey is liked
    useEffect(() => {
        const likedJerseys = JSON.parse(localStorage.getItem("likedJerseys")) || [];
        setLiked(likedJerseys.includes(jersey.id)); // Assuming jersey has an 'id' property
    }, [jersey.id]);

    // Handle toggling the like status
    const handleToggleLike = (jerseyId, isLiked) => {
        if (isLiked) {
            // If liked, remove it from local storage
            const likedJerseys = JSON.parse(localStorage.getItem("likedJerseys")) || [];
            const updatedJerseys = likedJerseys.filter(id => id !== jerseyId);
            localStorage.setItem("likedJerseys", JSON.stringify(updatedJerseys));
        } else {
            // If unliked, add it to local storage
            const likedJerseys = JSON.parse(localStorage.getItem("likedJerseys")) || [];
            likedJerseys.push(jerseyId);
            localStorage.setItem("likedJerseys", JSON.stringify(likedJerseys));
        }
        setLiked(!isLiked);
    };

    return (
        <div className="jersey-card">
            <img src={jersey.image_path.split(',')[0]} alt={jersey.team} className="jersey-image" />
            <div className="jersey-details">
                <h3 className="team-name">{jersey.team}</h3>
                <p className="brand">{jersey.brand}</p>
                <p className="price">£{jersey.price}</p>
                <p className="season">{jersey.season}</p>
                <Heart jerseyId={jersey.id} isLiked={liked} onToggleLike={handleToggleLike} />
            </div>
        </div>
    );
};

export default JerseyCard;
