import React, { useEffect, useState } from "react";
import './styles/signin.css';
import { signin } from './signinSlice'
import { connect } from 'react-redux';
import store from '../../app/store';

const mapStateToProps = (state) => {
    return {
      signin: state.signin.signin,
    };
};

function GetSigninLink(){
    const [authUrl, setAuthUrl] = useState('');
    fetch('/signin/geturl')
        .then(response => response.json())
        .then(data => setAuthUrl(data['auth_url']));
    return(
        <div class="signin">
            <p class="landing">
                Welcome to <span className="name">MixGen</span>, an AI-powered service for creating playlists 
                quickly and easily for any occasion. <br/><br/><br/> To get started, we will 
                need to get connected to your Spotify account.
            </p>
            <div class="link_div">
                <a class = "signin-link" href={authUrl}>Let's get started</a>
            </div>
        </div>
    )
}

export function Signin() {
    const [signedIn, setSignedIn] = useState(false);
    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
    
        if (code) {
          console.log(code);
          fetch('/signin/?code='.concat(code));
          setSignedIn(true);
          store.dispatch(signin({
            signin : true})
            )
        }
    }, []);

    return(
            <GetSigninLink />
    )
}

export default connect(mapStateToProps)(Signin);