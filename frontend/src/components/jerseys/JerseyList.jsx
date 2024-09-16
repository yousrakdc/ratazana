import React from 'react';
import JerseyCard from './JerseyCard';

const JerseyList = ({ jerseys }) => {
  return (
    <div className="jersey-list">
      {jerseys.map((jersey) => (
        <JerseyCard key={jersey.id} jersey={jersey} />
      ))}
    </div>
    
  );
};

export default JerseyList;
