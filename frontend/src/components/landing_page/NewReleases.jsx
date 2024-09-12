import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './NewReleases.css'; // Ensure this file contains your CSS for styling

const newReleasesData = [
  { id: 1, name: 'New Jersey 1', image: '/images/new1.jpg', price: '$70' },
  { id: 2, name: 'New Jersey 2', image: '/images/new2.jpg', price: '$75' },
  { id: 3, name: 'New Jersey 3', image: '/images/new3.jpg', price: '$75' },
  { id: 4, name: 'New Jersey 4', image: '/images/new4.jpg', price: '$75' },
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
