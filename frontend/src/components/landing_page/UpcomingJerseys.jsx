import React, { useEffect, useState } from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import '../jerseys/JerseyCard.css';

const UpcomingJerseys = () => {
    const [jerseys, setJerseys] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchJerseys = async () => {
            try {
                const response = await fetch('/api/jerseys/?upcoming=true');
                console.log('Response:', response); // Log the response object

                // Check if response is OK
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                setJerseys(data);
            } catch (err) {
                console.error('Fetch error:', err); // Log any fetch errors
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchJerseys();
    }, []);

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 1,
    };

    if (loading) return <div>Loading upcoming jerseys...</div>;
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

export default UpcomingJerseys;
