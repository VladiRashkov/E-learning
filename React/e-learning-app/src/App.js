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
          <a className="navbar-brand" href="/" style={{ fontSize: '24px', fontWeight: 'Medium', color: '#fff' }}>
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
            ></input>
          </div>

          <div>
            <label htmlFor='description' className='form-label'>
              Description
            </label>
          </div>
      
        </form>

        <table className='table table-stripped table-bordered table-hover'>
          <thead>
            <tr>
              <th>title</th>
              <th>description</th>
              <th>home_page_picture</th>
              <th>is_premium?</th>
              <th>rating</th>
              <th>objectives</th>
            </tr>
            </thead> 
            <tbody>
              {
                courses.map((course) =>(
                  <tr key = {course.course_id}>
                    <td>{course.title}</td>
                    <td>{course.description}</td>
                    <td>{course.home_page_picture}</td>
                    <td>{course.is_premium ? 'Yes': 'No'}</td>
                    <td>{course.rating}</td>
                    <td>{course.objectives}</td>
                  </tr>
                ))
              }
            </tbody>

        </table>
      </div>
    </div>
  );
};

export default App;
