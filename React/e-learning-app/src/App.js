import React, { useState, useEffect, useCallback } from 'react';
import Login from './login';
import api from './api';
import './App.css';

const App = () => {
  const [courses, setCourses] = useState([]);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

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

  const fetchCourses = useCallback(async () => {
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
  }, [token]);

  useEffect(() => {
    if (token) {
      fetchCourses();
    }
  }, [token, fetchCourses]);

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('token');
  };

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

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

  const viewEnrolledCourses = async () => {
    try {
      const tokenData = parseJwt(token);
      const user_id = tokenData?.user_id;
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
      console.log(enrolledCourses)
      const enrolledWindow = window.open('/enrolled_courses.html', '_blank');
      console.log(enrolledWindow)
      
      
        enrolledWindow.enrolledCourses = enrolledCourses;
     
    } catch (error) {
      console.error('Error fetching enrolled courses:', error);
      alert('Failed to fetch enrolled courses.');
    }
  };

  const filteredCourses = courses.filter(course =>
    course.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (!token) {
    return <Login onLogin={(token) => setToken(token)} />;
  }

  return (
    <div className="App" style={{ backgroundColor: '#000000', minHeight: '100vh', padding: '20px' }}>
      <nav className="navbar" style={{ backgroundColor: '#FFFFFF', borderRadius: '5px' }}>
        <div className="container-fluid">
          <a className="navbar-brand" href="/" style={{ fontSize: '24px', color: '#3e3193', fontWeight: 'bold' }}>
            E-Learning App
          </a>
          <div className="button-group">
            <button onClick={viewEnrolledCourses} className="btn-purple">
              View Enrolled Courses
            </button>
            <button onClick={handleLogout} className="btn-purple">
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="container mt-3">
        <input
          type="text"
          className="form-control"
          placeholder="Search for a course..."
          value={searchTerm}
          onChange={handleSearchChange}
        />

        {loading && <p style={{ color: '#FFFFFF' }}>Loading courses...</p>}
        {error && <p className="error" style={{ color: 'red' }}>{error}</p>}

        <table className="table table-striped table-bordered table-hover mt-3">
          <thead>
            <tr style={{ backgroundColor: '#FFFFFF' }}>
              <th>Title</th>
              <th>Description</th>
              <th>Home Page Picture</th>
              <th>Is Premium?</th>
              <th>Rating</th>
              <th>Objectives</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredCourses.length > 0 ? (
              filteredCourses.map((course, index) => (
                <tr key={index} style={{ backgroundColor: '#FFFFFF' }}>
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
                  <td>
                    {course.is_premium ? (
                      <button
                        onClick={() => joinCourse(course.title)}
                        className="btn-purple"
                      >
                        Request Enrollment
                      </button>
                    ) : (
                      <button
                        onClick={() => joinCourse(course.title)}
                        className="btn-purple"
                      >
                        Join course
                      </button>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr style={{ backgroundColor: '#FFFFFF' }}>
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
