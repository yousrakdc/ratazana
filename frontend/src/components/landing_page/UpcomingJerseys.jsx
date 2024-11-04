import React, { useEffect, useState } from 'react';
import Slider from 'react-slick';
import styles from './UpcomingJerseys.module.css';

const UpcomingJerseys = () => {
    const [jerseys, setJerseys] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Fetch upcoming jerseys from the API
        fetch('http://localhost:8000/api/jerseys/?category=upcoming')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
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
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 5000,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                }
            }
        ]
    };

    if (loading) return <p>Loading upcoming jerseys...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <Slider {...settings}>
            {jerseys.length > 0 ? (
                jerseys.map(jersey => (
                    <div key={jersey.id} className={styles.jerseyCard}>
                        <div className={styles.imageWrapper}>
                            <img 
                                src={`http://localhost:8000${jersey.images[0]?.image_path}`} 
                                alt={jersey.team} 
                                className={styles.jerseyImage} 
                            />
                            <img 
                                src={`http://localhost:8000${jersey.images[1]?.image_path}`} 
                                alt={jersey.team} 
                                className={styles.hoverImage} 
                            />
                        </div>
                        <div className={styles.jerseyDetails}>
                            <h3 className={styles.jerseyTeamName}>{jersey.team}</h3>
                            <p className={styles.jerseyBrand}>{jersey.brand}</p>
                            <p className={styles.price}>£{parseFloat(jersey.price).toFixed(2)}</p>
                        </div>
                    </div>
                ))
            ) : (
                <p>No upcoming jerseys available.</p>
            )}
        </Slider>
    );
};

export default UpcomingJerseys;
