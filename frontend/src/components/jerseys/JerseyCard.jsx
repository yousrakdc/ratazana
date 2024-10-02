import React from "react";
import './JerseyCard.css';

const JerseyCard = ({ jersey }) => {
    return (
        <div className="jersey-card">
            <img src={jersey.image_path.split(',')[0]} alt={jersey.team} className="jersey-image" />
            <div className="jersey-details">
                <h3 className="team-name">{jersey.team}</h3>
                <p className="brand">{jersey.brand}</p>
                <p className="price">£{jersey.price}</p>
                <p className="season">{jersey.season}</p>
            </div>
        </div>
    );
};

export default JerseyCard;
