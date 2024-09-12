import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './NewReleases.css';

const UpcomingJerseysData = [
  { id: 1, name: 'Upcoming Jersey 1', image: '/images/upcoming1.jpg', price: '$80' },
  { id: 2, name: 'Upcoming Jersey 2', image: '/images/upcoming2.jpg', price: '$85' },
  { id: 3, name: 'Upcoming Jersey 3', image: '/images/upcoming3.jpg', price: '$90' },
];

const UpcomingJerseys = () => {
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1,
  };

  return (
    <Slider {...settings}>
      {UpcomingJerseysData.map(jersey => (
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
