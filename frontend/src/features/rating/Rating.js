import React, { useState } from 'react';
import './styles/rating.css'

const StarRating = ({ initialValue, onRate }) => {
  const [rating, setRating] = useState(initialValue);

  const handleStarClick = (newRating) => {
    setRating(newRating);
    if (onRate) {
      onRate(newRating);
    }
  };

  const renderStars = () => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span
          key={i}
          className={`star ${i <= rating ? 'filled' : ''}`}
          onClick={() => handleStarClick(i)}
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