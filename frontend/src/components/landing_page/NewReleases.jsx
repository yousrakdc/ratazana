import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import styles from './NewReleases.module.css';

const NewReleases = () => {
    const [jerseys, setJerseys] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch new release jerseys on component mount
    useEffect(() => {
        fetch('http://localhost:8000/api/jerseys/?category=new_release')
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

    // Slider settings for responsive behavior
    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 5000,
        centerMode: true,
        centerPadding: '30px',
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                },
            },
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                },
            },
        ],
    };

    // Loading and error handling
    if (loading) return <p>Loading new releases...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <Slider {...settings} className={styles.newReleasesSlide}>
            {jerseys.length > 0 ? (
                jerseys.map((jersey) => (
                    <div key={jersey.id} className={styles.jerseyCard}>
                        <Link to={`/jerseys/${jersey.id}`} className={styles.imageContainer}>
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
                                    <p className={styles.jerseyBrand}>{jersey.brand}</p> {/* New brand element */}
                                    <p className={styles.price}>£{parseFloat(jersey.price).toFixed(2)}</p>
                                </div>
                            </div>
                        </Link>
                    </div>
                ))
            ) : (
                <p>No new releases available.</p>
            )}
        </Slider>
    );
};

export default NewReleases;
