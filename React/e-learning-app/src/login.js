import React, { useState } from 'react';
import api from './api';
import './Login.css';
import Register from './register';  // Import Register component

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [showRegister, setShowRegister] = useState(false);  // State to toggle between login and register

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/users/login', { email, password });
      const token = response.data.access_token;
      localStorage.setItem('token', token);
      onLogin(token);
    } catch (error) {
      setErrorMessage('Invalid credentials, please try again.');
    }
  };

  const handleRegister = () => {
    setShowRegister(true);  // Show the register form when the button is clicked
  };

  const handleRegisterSuccess = () => {
    setShowRegister(false);  // After successful registration, return to login form
  };

  if (showRegister) {
    return <Register onRegisterSuccess={handleRegisterSuccess} />;
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h1><strong><u>E-learning LTD.</u></strong></h1>
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
          <button type="submit">Login</button>
        </form>
        <button onClick={handleRegister}>Register</button>
      </div>
    </div>
  );
};

export default Login;
