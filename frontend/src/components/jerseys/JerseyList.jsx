import React, { useState, useEffect } from 'react';
import Layout from '../Layout';
import Filter from './Filter';
import './JerseyList.css';

const JerseyList = () => {
    const [jerseys, setJerseys] = useState([]);
    const [filteredJerseys, setFilteredJerseys] = useState([]);
    const [filters, setFilters] = useState({ team: [], country: [], color: [], price: [] });
    const [error, setError] = useState(null);

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
                setFilteredJerseys(data);
            })
            .catch((error) => {
                setError(error.message);
            });
    }, []);

    const handleFilterChange = (e) => {
        const { value, checked, name } = e.target;

        setFilters((prevFilters) => {
            const updatedCategory = checked
                ? [...prevFilters[name], value]
                : prevFilters[name].filter((item) => item !== value);

            return { ...prevFilters, [name]: updatedCategory };
        });
    };

    useEffect(() => {
        let filtered = jerseys;

        // Debugging logs
        console.log("Initial Jerseys:", jerseys);
        console.log("Current Filters:", filters);

        // Filter by team
        if (filters.team.length > 0) {
            filtered = filtered.filter(jersey => filters.team.includes(jersey.team));
            console.log("Filtered by Team:", filtered);
        }

        // Filter by country
        if (filters.country.length > 0) {
            filtered = filtered.filter(jersey => filters.country.includes(jersey.country));
            console.log("Filtered by Country:", filtered);
        }

        // Filter by color
        if (filters.color.length > 0) {
            filtered = filtered.filter(jersey => filters.color.includes(jersey.color));
            console.log("Filtered by Color:", filtered);
        }

        // Filter by price range
        if (filters.price.length > 0) {
            filtered = filtered.filter(jersey => {
                const price = parseInt(jersey.price, 10);
                return filters.price.some(priceRange => {
                    const [min, max] = priceRange.split('-').map(Number);
                    return price >= min && price <= max;
                });
            });
            console.log("Filtered by Price:", filtered);
        }

        // Final filtered jerseys
        setFilteredJerseys(filtered);
        console.log("Final Filtered Jerseys:", filtered);
    }, [filters, jerseys]);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <Layout>
            <div className="jersey-page">
                <aside className="filter-sidebar">
                    <Filter onFilterChange={handleFilterChange} />
                </aside>
                <main className="jersey-list-container">
                    <div className="jersey-list">
                        {filteredJerseys.length > 0 ? (
                            filteredJerseys.map((jersey) => (
                                <div key={jersey.id} className="jersey-item">
                                    <div className="image-container">
                                        <img 
                                            src={`http://localhost:8000${jersey.images[0].image_path}`} 
                                            alt={jersey.team} 
                                            className="jersey-image" 
                                        />
                                    </div>
                                    <h3 className="jersey-team-name">{jersey.team}</h3>
                                    <p>£{jersey.price}</p>
                                </div>
                            ))
                        ) : (
                            <p>No jerseys available.</p>
                        )}
                    </div>
                </main>
            </div>
        </Layout>
    );
};

export default JerseyList;
