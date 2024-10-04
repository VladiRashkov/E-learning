import React, { useState, useEffect } from 'react';
import api from './api';

const App = () => {
  const [courses, setCourses] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    home_page_picture: '',
    is_premium: false,
    rating: '',
    objectives: '',
  });
//admin token
  localStorage.setItem('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNCwiZXhwIjoxNzI4MDM4ODI5fQ.rJ78QVU5KxAA48tp6g3dCZsv_Tmtf98RhUi0S4I6S4s');

  const fetchCourses = async () => {
    try {
      const token = localStorage.getItem('token'); // Get token from localStorage
      const response = await api.get('/courses', {
        headers: {
          Authorization: `Bearer ${token}`, // Include token in the request header
        },
      });
      setCourses(response.data);
    } catch (error) {
      if (error.response && error.response.status === 403) {
        console.error('Unauthorized: ', error.response.data.detail);
      } else {
        console.error('An error occurred:', error);
      }
    }
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  const handleInputChange = (event) => {
    const value =
      event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    const token = localStorage.getItem('token'); // Get token for POST request
    await api.post('/courses', formData, {
      headers: {
        Authorization: `Bearer ${token}`, // Include token in the request header
      },
    });
    fetchCourses();
    setFormData({
      title: '',
      description: '',
      home_page_picture: '',
      is_premium: false,
      rating: '',
      objectives: '',
    });
  };

  return (
    <div>
      <nav className="navbar navbar bg-primary">
        <div className="container-fluid">
          <a className="navbar-brand" href="/">
            E-Learning App
          </a>
        </div>
      </nav>
      <div className="container">
        <form onSubmit={handleFormSubmit}>
          <div className="mb-3 mt-3">
            <label htmlFor="title" className="form-label">
              Title
            </label>
            <input
              type="text"
              className="form-control"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </form>
        {courses.length > 0 ? (
          <ul>
            {courses.map((course) => (
              <li key={course.id}>{course.title}</li>
            ))}
          </ul>
        ) : (
          <p>No courses available.</p>
        )}
      </div>
    </div>
  );
};

export default App;
