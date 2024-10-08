import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Slider from 'react-slick'; // Import Slick
import './JerseyDetail.css';

function JerseyDetail() {
    const { id } = useParams();
    const [jersey, setJersey] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null); 

    useEffect(() => {
        const fetchJersey = async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/jerseys/${id}/`);
                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('Error response from server:', errorText);
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log('Fetched jersey data:', data); // Debugging line
                setJersey(data);
            } catch (error) {
                console.error('Error fetching jersey:', error);
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchJersey();
    }, [id]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!jersey) return <div>Jersey not found</div>;

    // Slick settings for the image carousel
    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
    };

    return (
        <div className="jersey-details-container">
            {/* Slick Carousel for images */}
            <div className="image-carousel">
                {jersey.images && jersey.images.length > 0 ? (
                    <Slider {...settings}>
                        {jersey.images.map((image, index) => (
                            <div key={index}>
                                <img
                                    src={`http://localhost:8000${image.image_path}`}
                                    alt={jersey.team}
                                    className="jersey-image"
                                />
                            </div>
                        ))}
                    </Slider>
                ) : (
                    <p>No images available.</p>
                )}
            </div>

            {/* Jersey name underneath the images */}
            <h1 className="jersey-name">{jersey.team} - {jersey.brand} ({jersey.season})</h1>

            {/* Jersey description directly underneath images */}
            <div className="jersey-description">
                <p>{jersey.description || "Description not available."}</p>
                <p className="jersey-price">Price: £{jersey.price || "Price not available."}</p>

                {/* Button to redirect to Nike page */}
                {jersey.original_url && (
                    <a
                        href={jersey.original_url}
                        className="nike-button"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        View on Nike
                    </a>
                )}
            </div>
        </div>
    );
}

export default JerseyDetail;
