import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles/checklist.css'
import { go_back } from '../form/formSlice'
import store from '../../app/store';


const Checklist = () => {
  const [checklist, setChecklist] = useState([]);
  const [checkedItems, setCheckedItems] = useState({});
  const [confirmed, setConfirmed] = useState(false);

  const handleGoBack = (_) => {
    store.dispatch(go_back());
}

  useEffect(() => {
    fetch('/api/checklist')
      .then(response => response.json())
      .then(data => {
        setChecklist(Object.keys(data));
        setCheckedItems(data);
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
    <div>
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
            <div>
                <button onClick={handleConfirm} class="button-63" role="button">
                    Confirm
                </button>
            </div>
        </div>
        }
        {confirmed && <div>
            <p>
            Your playlist has been created!
            </p>
        </div>}
        <br/>
        <button onClick={handleGoBack} class="button-64" role="button">
            Go Back
        </button>
    </div>
  );
};

export default Checklist;
