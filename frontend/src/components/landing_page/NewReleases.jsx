import React, { useEffect, useState } from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import '../jerseys/JerseyCard.css';

const NewReleases = () => {
    const [jerseys, setJerseys] = useState([]);

    useEffect(() => {
        fetch('/api/jerseys/?category=new_release')
            .then(response => response.json())
            .then(data => setJerseys(data));
    }, []);

    const settings = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: 4,
        slidesToScroll: 4,
    };

    return (
        <Slider {...settings}>
            {jerseys.map(jersey => (
                <div key={jersey.id} className="jersey-card">
                    <img src={jersey.images[0]?.image_path} alt={jersey.team} />
                    <h3>{jersey.team}</h3>
                    <p>{jersey.price}</p>
                </div>
            ))}
        </Slider>
    );
};

export default NewReleases;
