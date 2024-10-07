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
  const [token, setToken] = useState(null);  // Add token state to manage login

  const fetchCourses = async () => {
    try {
      const response = await api.get('/courses', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      console.log(response.data);
      setCourses(response.data.items || response.data);
    } catch (error) {
      if (error.response && error.response.status === 403) {
        console.error('Unauthorized: ', error.response.data.detail);
      } else {
        console.error('An error occurred:', error);
      }
    }
  };

  useEffect(() => {
    if (token) {
      fetchCourses();
    }
  }, [token]);

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
    try {
      await api.post('/courses', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      fetchCourses();  // Refresh courses after submitting a new one
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
    }
  };

  // Conditional rendering
  if (!token) {
    return <Login onLogin={(token) => setToken(token)} />;  // Pass token to App
  }

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
            <label htmlFor="title" className="form-label">Title</label>
            <input
              type="text"
              className="form-control"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
            />
          </div>

          <div>
            <label htmlFor='description' className='form-label'>Description</label>
          </div>

          {/* Add other input fields here */}
        </form>

        <table className='table table-stripped table-bordered table-hover'>
          <thead>
            <tr>
              <th>Title</th>
              <th>Description</th>
              <th>Home Page Picture</th>
              <th>Is Premium?</th>
              <th>Rating</th>
              <th>Objectives</th>
            </tr>
          </thead>
          <tbody>
            {courses.length > 0 ? (
              courses.map((course, index) => (
                <tr key={index}>
                  <td>{course.title}</td>
                  <td>{course.description}</td>
                  <td>
                    {course.home_page_picture ? (
                      <img
                        src={`data:image/jpeg;base64,${course.home_page_picture}`}
                        alt="Course"
                        style={{ width: '100px', height: 'auto' }}
                      />
                    ) : 'No Image'}
                  </td>
                  <td>{course.is_premium ? 'Yes' : 'No'}</td>
                  <td>{course.rating}</td>
                  <td>{course.objectives || 'No objectives'}</td>
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
