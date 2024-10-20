import React, { useState, useEffect } from 'react';
import Login from './login';  // Import Login component
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
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchCourses = async () => {
    setLoading(true);
    setError('');  // Reset error state
    try {
      const response = await api.get('/courses', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setCourses(response.data.items || response.data);
    } catch (error) {
      console.error('An error occurred:', error);
      setError('Failed to fetch courses. Please try again.');
      if (error.response && error.response.status === 401) {
        setToken(null);
        localStorage.removeItem('token');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchCourses();
    }
  }, [token]);

  const handleInputChange = (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    try {
      await api.post('/courses', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
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
    } catch (error) {
      console.error('Error submitting course:', error);
      setError('Error submitting course. Please try again.');
    }
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('token');
  };

  if (!token) {
    return <Login onLogin={(token) => setToken(token)} />;
  }

  return (
    <div>
      <nav 
        className="navbar" 
        style={{ 
          backgroundColor: '#F5F5DC', 
          height: '100px', 
          border: '2px solid #FFFFFF',
          borderRadius: '5px' 
        }}>
        <div className="container-fluid navbar">
          <a 
            className="navbar-brand" 
            href="/" 
            style={{ fontSize: '24px', fontWeight: 'Medium', color: '#000000' }}>
            E-Learning App
          </a>
          <button onClick={handleLogout} className="btn btn-danger" >Logout</button>
        </div>
      </nav>
      <div className="container">
        <form onSubmit={handleFormSubmit}>
          <div className="mb-3 mt-3">
            <label htmlFor="title" className="form-label" style={{ backgroundColor: '#ffffff' }}>Title</label>
            <input
              style={{ backgroundColor: '#F5F5DC' }}
              type="text"
              className="form-control"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              required
            />
          </div>
          {/* Other input fields */}
          <button type="submit" className="btn btn-primary">Add Course</button>
        </form>

        {loading && <p>Loading courses...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}

        <table className='table table-stripped table-bordered table-hover'>
          <thead>
            <tr style={{ backgroundColor: '#FFFFFF' }}>
              <th style={{ color: '#101820' }}>Title</th>
              <th style={{ color: '#101820' }}>Description</th>
              <th style={{ color: '#101820' }}>Home Page Picture</th>
              <th style={{ color: '#101820' }}>Is Premium?</th>
              <th style={{ color: '#101820' }}>Rating</th>
              <th style={{ color: '#101820' }}>Objectives</th>
            </tr>
          </thead>
          <tbody>
            {courses.length > 0 ? (
              courses.map((course, index) => (
                <tr key={index} style={{ backgroundColor: '#F5F5DC' }}>
                  <td style={{ color: '#000000' }}>{course.title}</td>
                  <td style={{ color: '#000000' }}>{course.description}</td>
                  <td>
                    {course.home_page_picture ? (
                      <img
                        src={`data:image/jpeg;base64,${course.home_page_picture}`}
                        alt="Course"
                        style={{ width: '100px', height: 'auto' }}
                      />
                    ) : 'No Image'}
                  </td>
                  <td style={{ color: '#000000' }}>{course.is_premium ? 'Yes' : 'No'}</td>
                  <td style={{ color: '#000000' }}>{course.rating}</td>
                  <td style={{ color: '#000000' }}>{course.objectives || 'No objectives'}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6">No courses available</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default App;
