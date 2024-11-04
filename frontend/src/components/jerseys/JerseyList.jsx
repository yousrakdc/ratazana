import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../Layout';
import Filter from './Filter';
import Heart from './Heart';
import './JerseyList.css';


const JerseyList = () => {
    const [jerseys, setJerseys] = useState([]);
    const [filteredJerseys, setFilteredJerseys] = useState([]);
    const [filters, setFilters] = useState({ team: [], country: [], color: [], price: [] });
    const [likedJerseys, setLikedJerseys] = useState([]); 
    const [error, setError] = useState(null);

    // Fetch jerseys from the API
    useEffect(() => {
        fetch('http://localhost:8000/api/jerseys/')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                setJerseys(data);
                setFilteredJerseys(data); // Initialize filtered jerseys
            })
            .catch((error) => {
                setError(error.message); // Handle fetch errors
            });
    }, []);

    // Handle filter changes
    const handleFilterChange = (e) => {
        const { value, checked, name } = e.target;

        setFilters((prevFilters) => {
            const updatedCategory = checked
                ? [...prevFilters[name], value]
                : prevFilters[name].filter((item) => item !== value);

            return { ...prevFilters, [name]: updatedCategory };
        });
    };

    // Apply filtering logic based on selected filters
    useEffect(() => {
        let filtered = jerseys;

        // Filter by team
        if (filters.team.length > 0) {
            filtered = filtered.filter((jersey) =>
                filters.team.some((filterTeam) =>
                    jersey.team.toLowerCase().includes(filterTeam.toLowerCase())
                )
            );
        }

        // Filter by country
        if (filters.country.length > 0) {
            filtered = filtered.filter((jersey) => filters.country.includes(jersey.country));
        }

        // Filter by color
        if (filters.color.length > 0) {
            filtered = filtered.filter((jersey) =>
                filters.color.some((filterColor) =>
                    jersey.color.toLowerCase().includes(filterColor.toLowerCase())
                )
            );
        }

        // Filter by price range
        if (filters.price.length > 0) {
            filtered = filtered.filter((jersey) => {
                const price = parseFloat(jersey.price);
                return filters.price.some((range) => {
                    const [min, max] = range.split('-').map(Number);
                    return price >= min && price <= max;
                });
            });
        }

        setFilteredJerseys(filtered); // Update the state with filtered jerseys
    }, [filters, jerseys]);

    // Toggle liked state for a jersey
    const toggleLike = (id) => {
        setLikedJerseys((prev) => {
            if (prev.includes(id)) {
                return prev.filter((jerseyId) => jerseyId !== id); // Remove from liked
            }
            return [...prev, id]; // Add to liked
        });
    };

    // Display error message if fetch fails
    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="jersey-page">
            <aside className="filter-sidebar">
                <Filter onFilterChange={handleFilterChange} />
            </aside>
            <main className="jersey-list-container">
                <div className="jersey-list">
                    {filteredJerseys.length > 0 ? (
                        filteredJerseys.map((jersey) => (
                            <div key={jersey.id} className="jersey-item">
                                <Link to={`/jerseys/${jersey.id}`} className="image-container">
                                    <div className="image-wrapper">
                                        {/* Check if images exist and safely access image paths */}
                                        <img
                                            src={
                                                jersey.images && jersey.images.length > 0
                                                    ? `http://localhost:8000${jersey.images[0]?.image_path || FALLBACK_IMAGE_PATH}`
                                                    : FALLBACK_IMAGE_PATH // Use fallback if no images
                                            }
                                            alt={jersey.team}
                                            className="jersey-image"
                                        />
                                        {jersey.images && jersey.images.length > 1 && (
                                            <img
                                                src={`http://localhost:8000${jersey.images[1]?.image_path || FALLBACK_IMAGE_PATH}`}
                                                alt={jersey.team}
                                                className="jersey-image hover-image"
                                            />
                                        )}
                                    </div>
                                </Link>
                                <h3 className="jersey-team-name">{jersey.team}</h3>
                                <div className="price-container">
                                    <p className="jersey-price">£{jersey.price}</p>
                                    <Heart
                                        checked={likedJerseys.includes(jersey.id)} // Check if this jersey is liked
                                        onChange={() => toggleLike(jersey.id)} // Toggle like on checkbox change
                                    />
                                </div>
                            </div>
                        ))
                    ) : (
                        <p>No jerseys available.</p>
                    )}
                </div>
            </main>
        </div>
    );
};

export default JerseyList;
