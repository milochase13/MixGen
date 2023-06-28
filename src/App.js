import React, { useEffect, useState } from "react";
import logo from './logo.svg';
import './App.css';

function App() {
  const [response, setResponse] = useState('');
  const [result, setResult] = useState('');
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/api/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
      const app_response = await fetch('/api/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({ response }),
      });
  
      if (app_response.ok) {
        const app_response_json = app_response.json();
        app_response_json.then(data => setResult(data["playlist"]));
      } else {
        throw new Error('Request failed with status ' + app_response.status);
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div class="App">
      {/* <p>The current time is {currentTime}.</p> */}
      <form class="App-header"  onSubmit={handleSubmit}>
        Describe your playlist:   
        <input type="text" value={response} onChange={(e) => setResponse(e.target.value)} />
        <button type="submit">Submit</button>
      </form>
      <div class="App-playlist">
      {result && <div class="white-space-pre-line"> <div class="App-playlist-header">Playlist for <span class="App-prompt">{response}:</span> </div> <br/> {result} </div>}
      </div>
    </div>
  );
}

export default App;