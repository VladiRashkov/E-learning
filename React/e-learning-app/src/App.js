import React, {useState, useEffect} from 'react'
import api from './api'


const App = () => {
  const [courses, setCourses] = useState([]);
  const [formData, setFormData] = useState({

    title:'',
    description:'',
    home_page_picture:'',
    is_premium:false,
    rating: '',
    objectives:''
  });

  const fetchCourses = async () =>{
    const response = await api.get('/courses');
    setCourses(response.data)
  };

  useEffect(() =>{
    fetchCourses();
  }, []);

  const handleInputChange = (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked: event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleFormSubmit = async(event) =>{
    event.preventDefault();
    await api.post('/courses', formData);
    fetchCourses()
    setFormData({
      title:'',
      description:'',
      home_page_picture:'',
      is_premium:false,
      rating: '',
      objectives:''
    })
  }

  return(
    <div>
      <nav className='navbar navbar bg-primary'>
        <div className='container-fluid'>
          <a className='navbar-brand' href='#'>
            E-Learning App
          </a>
        </div>
      </nav>
    </div>
  )

}

export default App;
