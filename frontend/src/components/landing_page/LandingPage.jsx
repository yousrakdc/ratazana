import React from 'react';
import PromotedJerseys from './PromotedJerseys';
import NewReleases from './NewReleases';
import UpcomingJerseys from './UpcomingJerseys';
import './LandingPage.css';
import '../jerseys/JerseyCard.css';

const LandingPage = () => {
  return (
    <div className="landing-page">

      <section className="promoted-section">
        <h2> Don't miss out!</h2>
        <PromotedJerseys />
      </section>

      <section className="new-releases-section">
        <h2>New In!</h2>
        <NewReleases />
      </section>

      <section className="upcoming-section">
        <h2>Worth the wait...</h2>
        <UpcomingJerseys />
      </section>
    </div>
  );
};

export default LandingPage;
