import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './PromotedJerseys.css';

const jerseys = [
  { id: 1, name: 'Promoted Jersey 1', image: '/images/jersey1.jpg', price: '$50' },
  { id: 2, name: 'Promoted Jersey 2', image: '/images/jersey2.jpg', price: '$60' },
  { id: 2, name: 'Promoted Jersey 3', image: '/images/jersey3.jpg', price: '$100' },
  { id: 2, name: 'Promoted Jersey 4', image: '/images/jersey3-4.jpg', price: '$160' },
];

const PromotedJerseys = () => {
  // Slider settings
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
        },
      },
    ],
  };


  return (
    <div className="promoted-jerseys">
      <Slider {...settings}>
        {jerseys.map(jersey => (
          <div className="jersey-card" key={jersey.id}>
            <img src={jersey.image} alt={jersey.name} />
            <h3>{jersey.name}</h3>
            <p>{jersey.price}</p>
          </div>
        ))}
      </Slider>
    </div>
  );
};

export default PromotedJerseys;