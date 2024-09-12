import React from "react";
import './JerseyCard.css';

const JerseyCard = ({ jersey }) => {
    return (
        <div className="jersey-card">
            <img src={jersey.image} alt={jersey.teamName} className="jersey-image"></img>
            <div className="jersey-details">
                <h3 className="team-name">${jersey.teamName}</h3>
                <p className="price">${jersey.price}</p>
            </div>
        </div>
    );
};

export default JerseyCard;