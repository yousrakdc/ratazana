import React from 'react';
import PromotedJerseys from './PromotedJerseys';
import NewReleases from './NewReleases';
import UpcomingJerseys from './UpcomingJerseys';
import './LandingPage.css';
import '../jerseys/JerseyCard.css';

const LandingPage = () => {
  return (
    <div className="landing-page">

      {/* Promoted Jerseys Section */}
      <section className="promoted-section">
        <PromotedJerseys />
      </section>

      {/* New Releases Section (Carousel) */}
      <section className="new-releases-section">
        <h2>New Releases</h2>
        <NewReleases />
      </section>

      {/* Upcoming Jerseys Section (Carousel) */}
      <section className="upcoming-section">
        <h2>Worth the wait...</h2>
        <UpcomingJerseys />
      </section>
    </div>
  );
};

export default LandingPage;