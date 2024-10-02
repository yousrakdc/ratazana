import React, { useEffect, useState } from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './PromotedJerseys.css';
import '../jerseys/JerseyCard.css';

const PromotedJerseys = () => {
    const [jerseys, setJerseys] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('/api/jerseys/?promoted=true')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch promoted jerseys');
                }
                return response.json();
            })
            .then(data => {
                setJerseys(data);
                setLoading(false);
            })
            .catch(error => {
                setError(error.message);
                setLoading(false);
            });
    }, []);

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
    };

    if (loading) return <div>Loading promoted jerseys...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <Slider {...settings}>
            {jerseys.map(jersey => (
                <div key={jersey.id} className="jersey-card">
                    <img src={jersey.image} alt={jersey.name} />
                    <h3>{jersey.name}</h3>
                    <p>{jersey.price}</p>
                </div>
            ))}
        </Slider>
    );
};

export default PromotedJerseys;
