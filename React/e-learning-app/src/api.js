// api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Adjust this to match your FastAPI server URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
