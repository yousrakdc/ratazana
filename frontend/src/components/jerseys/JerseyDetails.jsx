import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Layout from '../Layout';

const JerseyDetail = () => {
    const { id } = useParams(); // Get the ID from the URL
    const [jersey, setJersey] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(`http://localhost:8000/jerseys/${id}/`) // Use the ID in the API call
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Failed to fetch jersey details');
                }
                return response.json();
            })
            .then((data) => setJersey(data))
            .catch((error) => setError(error.message));
    }, [id]);

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!jersey) {
        return <div>Loading...</div>;
    }

    return (
        <Layout>
            <div className="jersey-detail">
                <h2>{jersey.team}</h2>
                <p>Price: ${jersey.price}</p>
                <p>Description: {jersey.description}</p>
                {/* Add more details about the jersey */}
                <img src={jersey.image_path} alt={`${jersey.team} jersey`} />
            </div>
        </Layout>
    );
};

export default JerseyDetail;
