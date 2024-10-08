import React, { useState } from 'react';
import api from './api';  
import './Login.css';  // Import external CSS

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post('/users/login', {
        email,
        password,
      });
      console.log('Response:', response); 
      const token = response.data.access_token;  
      console.log('Token:', token);
      
      localStorage.setItem('token', token);
      onLogin(token);  
    } catch (error) {
      setErrorMessage('Invalid credentials, please try again.');
    }
  };

  const handleRegister = () => {
    // Handle registration logic or navigate to registration page
    console.log('Register button clicked');
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1><strong><u>E-learning LTD.</u></strong></h1> {/* Bold and Underline */}
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Username</label>
            <input
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
          <button type="submit">Login</button>
        </form>
        <div className="register-container">
          <button onClick={handleRegister}>Register</button>
        </div>
      </div>
    </div>
  );
};

export default Login;
