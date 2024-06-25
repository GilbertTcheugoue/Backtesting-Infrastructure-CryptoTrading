import React, { useState } from 'react';
import axios from 'axios';

const RegisterUserForm = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/register/', {
        username,
        email,
        password
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error registering user');
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>User Registration</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
        </label>
        <label>
          Email:
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Password:
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        <button type="submit">Register User</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default RegisterUserForm;
