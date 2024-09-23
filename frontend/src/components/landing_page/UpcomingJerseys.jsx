import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import '../jerseys/JerseyCard.css';
import upcoming1 from './images/upcoming1.jpeg';
import upcoming2 from './images/upcoming2.jpg';
import upcoming3 from './images/upcoming3.jpg';

const UpcomingJerseysData = [
  { id: 1, name: 'Upcoming Jersey 1', image: upcoming1, price: '$80' },
  { id: 2, name: 'Upcoming Jersey 2', image: upcoming2, price: '$85' },
  { id: 3, name: 'Upcoming Jersey 3', image: upcoming3, price: '$90' },
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