import React from 'react';
import SignUpForm from './components/auth/SignUpForm';
import SignInForm from './components/auth/SignInForm';
import 'swiper/swiper.min.css';


function App() {
  return (
    <div className="App">
      <SignUpForm />
      <SignInForm />
    </div>
  );
}

export default App;
