import React, { useEffect, useState } from "react";
import logo from './logo.svg';
import './App.css';
import './form.css';
import Checklist from './Checklist';

function Playlist(props) {
  return(
  <div class="white-space-pre-line"> 
    <div class="html">Playlist for <span class="App-prompt">{props.prompt}:</span> 
    </div> <br/> {props.result}
  </div>
  )
}

function App() {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState('');
  const [numSongs, setNumSongs] = useState('');
  const [title, setTitle] = useState('');
  const [inputError, setInputError] = useState(null);

  const handleNumSongsChange = (event) => {
    setNumSongs(event.target.value);
  };
  const handlePromptChange = (event) => {
    setPrompt(event.target.value);
  };
  const handleTitleChange = (event) => {
    setTitle(event.target.value);
  };
  const handleGoBack = (_) => {
    setResult('');
    setPrompt('');
    setNumSongs('');
    setTitle('');
    setInputError(null);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (prompt.length <= 0){
      setInputError('Please provide a playlist description!');
      return
    }
    else if (numSongs <= 0){
      setInputError('Please request a number of songs greater than 0!');
      return
    }
    else{
      setInputError(null);
    }
    try {
      const app_response = await fetch('/api/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({ "prompt": prompt, "num_songs": numSongs, "title": title}),
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
    <div class="html">
       {/* Form */}
      {!result && 
      <div class="container">
        <div class="cta-form">
          <h2>Create a new playlist!</h2> 
          <p>Submit the form to create an AI generated playlist from your liked songs.</p>
        </div>
        <form class="form"  onSubmit={handleSubmit}>
      
          <input class="form__input" type="text" value={title} onChange={handleTitleChange} placeholder="Title" />
          <label class="form__label" htmlFor="title">Title</label>
          
          <input class="form__input" type="text" value={prompt} onChange={handlePromptChange} placeholder="Prompt"/>
          <label for="prompt" class="form__label" htmlFor="description">Description</label>
          
          <input class="form__input" type="number" step="1" value = {numSongs} onChange={handleNumSongsChange} placeholder="Length" /> 
          <label for="songs" class="form__label" htmlFor="num_songs">Length</label>

          {inputError && <div style={{ color: 'red' }}>{inputError}</div>}
          <button type="submit">Submit</button>
        </form>
      </div> }

      {/* Result */}
      <div class="playlist">
      {/* {result && <Playlist prompt={prompt} result = {result}/>} */}
      {result && <Checklist/>}
      <br/>
      { result && <button onClick={handleGoBack}>
        Go Back
      </button>
      }
      </div>
    </div>
  );
}

export default App;