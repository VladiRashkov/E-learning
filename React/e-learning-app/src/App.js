import React, { useState, useEffect } from 'react';
import Login from './login';
import api from './api';

const App = () => {
  const [courses, setCourses] = useState([]);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState(''); // Search term state

  // Function to decode JWT token and extract user_id
  const parseJwt = (token) => {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => `%${('00' + c.charCodeAt(0).toString(16)).slice(-2)}`)
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch (error) {
      console.error('Invalid token');
      return null;
    }
  };

  const fetchCourses = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await api.get('/courses', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log(response.data);
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
      if (error.response && error.response.status === 307) {
        alert('A request to join the course has been sent for approval.');
      } else {
        alert('Failed to join the course.');
      }
    }
  };

  // Fetch enrolled courses and open them in a new window
  const viewEnrolledCourses = async () => {
    try {
      const tokenData = parseJwt(token); // Decode the token to get user_id
      const user_id = tokenData?.user_id; // Extract user_id

      if (!user_id) {
        alert('Unable to fetch user information.');
        return;
      }

      const response = await api.get(`/enroll/enrolled_courses/${user_id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const enrolledCourses = response.data;
      const enrolledWindow = window.open('', '_blank');
      enrolledWindow.document.write('<h1>Enrolled Courses</h1>');
      enrolledWindow.document.write('<ul>');
      enrolledCourses.forEach(course => {
        enrolledWindow.document.write(`
          <li>
            <strong>Title:</strong> ${course.title} <br/>
            <strong>Description:</strong> ${course.description}
          </li>
        `);
      });
      enrolledWindow.document.write('</ul>');
    } catch (error) {
      console.error('Error fetching enrolled courses:', error);
      alert('Failed to fetch enrolled courses.');
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
          <button onClick={viewEnrolledCourses} className="btn btn-primary">View Enrolled Courses</button>
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
            onChange={handleSearchChange}
          />
        </div>

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
                    {course.is_premium ? (
                      <button onClick={() => joinCourse(course.title)} className="btn btn-primary">
                        Request Enrollment
                      </button>
                    ) : (
                      <button onClick={() => joinCourse(course.title)} className="btn btn-primary">
                        Join Course
                      </button>
                    )}
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
