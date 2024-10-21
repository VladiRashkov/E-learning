import React, { useState, useEffect } from 'react';
import Login from './login';
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
  const [searchTerm, setSearchTerm] = useState(''); // New state for search term

  const fetchCourses = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await api.get('/courses', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log(response.data);  // Add this to log the response
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

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value); // Update search term state
  };

  // Function to join a course
  const joinCourse = async (title) => {
    console.log('Joining course:', title);
    try {
      const response = await api.put('/courses/join_course', null, {
        params: { title },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log('Response:', response);
      alert(`Successfully joined course: ${title}`);
    } catch (error) {
      // console.error('Error joining course:', error);
      alert('Failed to join the course.');
    }
  };
  
  
  // Filtered courses based on search term
  const filteredCourses = courses.filter(course =>
    course.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
          <button onClick={handleLogout} className="btn btn-danger">Logout</button>
        </div>
      </nav>
      <div className="container">
        <div className="mb-3 mt-3">
          <input
            type="text"
            className="form-control"
            placeholder="Search for a course..."
            value={searchTerm}
            onChange={handleSearchChange} // Handle search input change
          />
        </div>
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

        <table className='table table-striped table-bordered table-hover'>
          <thead>
            <tr style={{ backgroundColor: '#FFFFFF' }}>
              <th style={{ color: '#101820' }}>Title</th>
              <th style={{ color: '#101820' }}>Description</th>
              <th style={{ color: '#101820' }}>Home Page Picture</th>
              <th style={{ color: '#101820' }}>Is Premium?</th>
              <th style={{ color: '#101820' }}>Rating</th>
              <th style={{ color: '#101820' }}>Objectives</th>
              <th style={{ color: '#101820' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredCourses.length > 0 ? (
              filteredCourses.map((course, index) => (
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
                  <td>
                    <button onClick={() => joinCourse(course.title)} className="btn btn-primary">
                      Join Course
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7">No courses available</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default App;
