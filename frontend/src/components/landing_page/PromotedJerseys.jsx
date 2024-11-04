import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import styles from './PromotedJerseys.module.css';

const PromotedJerseys = () => {
    const [jerseys, setJerseys] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Fetch promoted jerseys from the API
        fetch('http://localhost:8000/api/jerseys/?category=promoted')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then((data) => {
                setJerseys(data);
                setLoading(false);
            })
            .catch((error) => {
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
        autoplay: true,
        autoplaySpeed: 5000,
    };

    if (loading) return <p>Loading promoted jerseys...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <Slider {...settings}>
            {jerseys.length > 0 ? (
                jerseys.map((jersey) => (
                    <div key={jersey.id} className={styles.jerseyCard}>
                        <div className={styles.jerseyContent}>
                            <div className={styles.imageWrapper}>
                                {jersey.images.length > 0 ? (
                                    <img
                                        src={`http://localhost:8000${jersey.images[0].image_path}`}
                                        alt={jersey.team}
                                        className={styles.jerseyImage}
                                    />
                                ) : (
                                    <img
                                        src="/path/to/fallback-image.jpg" 
                                        alt="No image available"
                                        className={styles.jerseyImage}
                                    />
                                )}
                                {jersey.images.length > 1 && (
                                    <img
                                        src={`http://localhost:8000${jersey.images[1].image_path}`}
                                        alt={jersey.team}
                                        className={styles.hoverImage}
                                    />
                                )}
                            </div>
                            
                            <div className={styles.jerseyDetails}>
                                <h3 className={styles.jerseyTeamName}>{jersey.team}</h3>
                                <p className={styles.price}>£{parseFloat(jersey.price).toFixed(2)}</p>
                                <Link to={`/jerseys/${jersey.id}`} className={styles.buttonLink}>
                                    <button className={styles.viewButton}>Shop Now</button>
                                </Link>
                            </div>
                        </div>
                    </div>
                ))
            ) : (
                <p>No promoted jerseys available.</p>
            )}
        </Slider>
    );    
};

export default PromotedJerseys;
