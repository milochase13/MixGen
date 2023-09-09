import React, { useState } from 'react';
import './styles/rating.css'

const StarRating = ({ initialValue, onRate }) => {
  const [rating, setRating] = useState(initialValue);
  const [hoveredRating, setHoveredRating] = useState(0);

  const handleStarClick = (newRating) => {
    setRating(newRating);
    if (onRate) {
      onRate(newRating);
    }
  };

  const handleStarHover = (i) => {
    setHoveredRating(i);
  };

  const renderStars = () => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span
          key={i}
          className={`star ${i <= rating || i <= hoveredRating ? 'filled' : ''}`}
          onClick={() => handleStarClick(i)}
          onMouseEnter={() => handleStarHover(i)}
          onMouseLeave={() => setHoveredRating(0)}
        >
          &#9733;
        </span>
      );
    }
    return stars;
  };

  return (
    <div class="feedback">
      <p class="message">
        We value your feedback. Please rate how accurately you felt the generated playlist matched your prompt.
      </p>
      <div className="star-rating">
        {renderStars()}
      </div>
    </div>
  );
};

export default StarRating;