import React, { useEffect, useState } from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import '../jerseys/JerseyCard.css';

const PromotedJerseys = () => {
    const [jerseys, setJerseys] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/api/jerseys/?category=promoted')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log("Fetched Jerseys:", data); // Log the fetched data
                setJerseys(data);
            })
            .catch(error => console.error('Error fetching promoted jerseys:', error));
    }, []);

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
    };

    return (
        <Slider {...settings}>
            {jerseys.length > 0 ? (
                jerseys.map(jersey => (
                    <div key={jersey.id} className="jersey-card">
                        {jersey.images.length > 0 && (
                            <img className="jersey-image" src={jersey.images[0].image_path} alt={jersey.team} />
                        )}
                        <div className="jersey-details">
                            <h3 className="team-name">{jersey.team}</h3>
                            <p className="price">${parseFloat(jersey.price).toFixed(2)}</p>
                        </div>
                    </div>
                ))
            ) : (
                <p>No promoted jerseys available</p>
            )}
        </Slider>
    );
};

export default PromotedJerseys;
