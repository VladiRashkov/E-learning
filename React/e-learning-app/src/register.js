import React, { useState } from 'react';
import api from './api';  
import './Register.css';  

const Register = ({ onRegisterSuccess }) => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        linkedin_account: '',
        photo: '',
        role: '',
    });
    const [errorMessage, setErrorMessage] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/users/new_account', formData);
            console.log('Registration successful:', response.data);

           
            onRegisterSuccess();
        } catch (error) {
            setErrorMessage('Registration failed, please try again.');
        }
    };

    return (
        <div className="register-container">
            <div className="register-box">
                <h2>Register</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <div className="input-container">
                            <label htmlFor="first_name">First Name</label>
                            <input type="text" name="first_name" placeholder="First Name" onChange={handleInputChange} required />
                        </div>
                        <div className="input-container">
                            <label htmlFor="last_name">Last Name</label>
                            <input type="text" name="last_name" placeholder="Last Name" onChange={handleInputChange} required />
                        </div>
                    </div>

                    <div className="form-group">
                        <div className="input-container">
                            <label htmlFor="email">Email</label>
                            <input type="email" name="email" placeholder="Email" onChange={handleInputChange} required />
                        </div>
                        <div className="input-container">
                            <label htmlFor="password">Password</label>
                            <input type="password" name="password" placeholder="Password" onChange={handleInputChange} required />
                        </div>
                    </div>

                    <div className="form-group">
                        <div className="input-container">
                            <label htmlFor="phone_number">Phone Number</label>
                            <input type="text" name="phone_number" placeholder="Phone Number" onChange={handleInputChange} required />
                        </div>
                        <div className="input-container">
                            <label htmlFor="linkedin_account">LinkedIn Profile</label>
                            <input type="text" name="linkedin_account" placeholder="LinkedIn Profile" onChange={handleInputChange} />
                        </div>
                    </div>

                    <div className="form-group">
                        <div className="input-container">
                            <label htmlFor="photo">Photo URL</label>
                            <input type="text" name="photo" placeholder="Photo URL" onChange={handleInputChange} />
                        </div>
                        <div className="input-container">
                            <label htmlFor="role">Role</label>
                            <select name="role" onChange={handleInputChange} required>
                                <option value="">Select Role</option>
                                <option value="student">Student</option>
                                <option value="teacher">Teacher</option>
                            </select>
                        </div>
                    </div>

                    {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                    <button type="submit">Register</button>
                </form>

                <div className="back-to-login">
                    <p>Already have an account? <a href="/login">Login here</a></p>
                </div>
            </div>
        </div>
    );
};

export default Register;
