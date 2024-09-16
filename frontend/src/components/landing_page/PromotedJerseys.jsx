import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './PromotedJerseys.css';
import '../jerseys/JerseyCard.css';
import jersey1 from './images/jersey1.png';
import jersey2 from './images/jersey2.png';
import jersey3 from './images/jersey3.png';


const jerseys = [
  { id: 1, name: 'Promoted Jersey 1', image: jersey1, price: '$50' },
  { id: 2, name: 'Promoted Jersey 2', image: jersey2, price: '$60' },
  { id: 2, name: 'Promoted Jersey 3', image: jersey3, price: '$100' },
];

const PromotedJerseys = () => {
  // Slider settings
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  };


  return (
      <Slider {...settings}>
        {jerseys.map(jersey => (
            <img src={jersey.image} alt={jersey.name} />
        ))}
      </Slider>
  );
};

export default PromotedJerseys;