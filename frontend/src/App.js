import React from "react";
import './styles/App.css';
import Checklist from './features/confirmation/Checklist';
import Form from './features/form/Form';
import Signin from './features/signin/Signin';
import { connect } from 'react-redux';

const mapStateToProps = (state) => {
  return {
    result: state.form.mode, 
    user_prompt: state.form.user_prompt, 
    num_songs: state.form.num_songs, 
    title: state.form.title, 
    input_error: state.form.input_error, 
    signin: state.signin.signin,
  };
};

function App(props) {
  
  if (props.result) {
    return (
      <div class="html">
        <div class="playlist">
          <Checklist/> 
        </div>
      </div>
    )
  }
  else{
    if(!props.signin){
      return(
        <Signin/>
      )
    }
    else{
      return(
        <div class="html">
        <Form/>
        </div>
      )
    }
  }
}

export default connect(mapStateToProps)(App);