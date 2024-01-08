import React from 'react';
import RingLoader from "react-spinners/RingLoader";
import './styles/loadingSpinner.css';

const LoadingSpinner = () => {
  return (
    <div className="loader">
        <div className="innerLoader">
            <RingLoader color="#54E0C7" size={300}/>
            <span className="loaderText">Generating your playlist, honestly this could take a while.</span>
        </div>
    </div>
  );
};

export default LoadingSpinner;