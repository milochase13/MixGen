import React, { useState } from "react";
import { submit } from './formSlice'
import './styles/form.css';
import { connect } from 'react-redux';
import store from '../../app/store';

const mapStateToProps = (state) => {
    return {
      result: state.form.mode, 
      user_prompt: state.form.user_prompt, 
      num_songs: state.form.num_songs, 
      title: state.form.title, 
      input_error: state.form.input_error, 
    };
};

export function Form() {
  const [prompt, setPrompt] = useState('');
  const [mode, setMode] = useState(0);
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (prompt.length <= 0){
    console.log(prompt.length);
      setInputError('Please provide a playlist description!');
      store.dispatch(submit({
        user_prompt: "",
        mode: 0,
        num_songs: "",
        title: "",
        input_error: inputError
      }))
      return
    }
    else if (numSongs <= 0){
      setInputError('Please request a number of songs greater than 0!');
      store.dispatch(submit({
        user_prompt: "",
        mode: 0,
        num_songs: "",
        title: "",
        input_error: inputError
      }))
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
        setMode(1);
        store.dispatch(submit({
            user_prompt: prompt,
            mode: 1,
            num_songs: numSongs,
            title: title,
            input_error: inputError
        }));
        
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
      </div> 
      
    </div>
  );
}

export default connect(mapStateToProps)(Form);