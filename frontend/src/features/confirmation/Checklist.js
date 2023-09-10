import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles/checklist.css'
import { go_back } from '../form/formSlice'
import store from '../../app/store';
import StarRating from '../rating/Rating';


const Checklist = () => {
  const [checklist, setChecklist] = useState([]);
  const [checkedItems, setCheckedItems] = useState({});
  const [confirmed, setConfirmed] = useState(false);
  const [is_enough_responses, setIs_enough_responses] = useState(true);

  const [rating, setRating] = useState(0);

  const handleRating = (newRating) => {
    // Handle the new rating here, e.g., save it to the server
    setRating(newRating);
  };

  const handleGoBack = (_) => {
    if (confirmed) {
      axios.post('/api/rating', { rating: rating })
        .then(response => {
          // handle response
        })
        .catch(error => {
          // Handle error 
        });
    }
    store.dispatch(go_back());
  }

  useEffect(() => {
    fetch('/api/checklist')
      .then(response => response.json())
      .then(data => {
        setChecklist(Object.keys(data["checklist"]));
        setCheckedItems(data["checklist"]);
        setIs_enough_responses(data["is_enough"]);
      });
  }, []);

  const handleCheckboxChange = (item) => {
    const updatedCheckedItems = { ...checkedItems };
    updatedCheckedItems[item] = !checkedItems[item];
    setCheckedItems(updatedCheckedItems);

    axios.post('/api/update-checklist', { checklist: updatedCheckedItems })
      .then(response => {
        // Handle success if necessary
      })
      .catch(error => {
        // Handle error if necessary
      });
  };

  const handleConfirm = (item) => {
    axios.post('/api/confirm-checklist')
      .then(response => {
        setConfirmed(true)
      })
      .catch(error => {
        // Handle error if necessary
      });
  };

  return (
    <div class=".checklist-container">
      {!confirmed && <div>
        <div class="header">
          Here is your AI generated playlist! Finalize it by choosing which songs to keep:
        </div>
        <form class="form-confirm">
          {checklist.map(item => (
            <div key={item} class="inputGroup">
              <input
                type="checkbox"
                checked={checkedItems[item]}
                onChange={() => handleCheckboxChange(item)}
                id={item}
              />
              <label for={item}>{item}</label>
            </div>
          ))}
        </form>
        {!is_enough_responses && 
        <div class="not-enough-songs">
          <p>Could not find enough songs that matched your description :( Please go back and try adjusting your prompt</p>
        </div>
        }
        <div class="button-container">
          <button onClick={handleGoBack} class="button-64 pair" role="button">
            Go Back
          </button>
          <button onClick={handleConfirm} class="button-63 pair" role="button">
            Confirm
          </button>
        </div>
      </div>
      }
      {confirmed && <div>
        <p class="rating-page">
          Your playlist has been created!
        </p>
        <br />
        <StarRating initialValue={rating} onRate={handleRating} />
        <div class="button-container">
          <button onClick={handleGoBack} class="button-64 pair" role="button">
            Done
          </button>
        </div>
      </div>
      }
    </div>
  );
};

export default Checklist;
