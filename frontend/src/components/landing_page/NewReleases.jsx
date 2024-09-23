import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import '../jerseys/JerseyCard.css';
import new1 from './images/new1.jpg';
import new2 from './images/new2.jpeg';
import new3 from './images/new3.jpeg';
import new4 from './images/new4.jpeg';

const newReleasesData = [
  { id: 1, name: 'New Jersey 1', image: new1, price: '$70' },
  { id: 2, name: 'New Jersey 2', image: new2, price: '$75' },
  { id: 3, name: 'New Jersey 3', image: new3, price: '$75' },
  { id: 4, name: 'New Jersey 4', image: new4, price: '$75' },
];

const NewReleases = () => {
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 4,
    slidesToScroll: 4,
  };

  return (
    <Slider {...settings}>
      {newReleasesData.map(jersey => (
        <div key={jersey.id} className="jersey-card">
          <img src={jersey.image} alt={jersey.name} />
          <h3>{jersey.name}</h3>
          <p>{jersey.price}</p>
        </div>
      ))}
    </Slider>
  );
};

export default NewReleases;