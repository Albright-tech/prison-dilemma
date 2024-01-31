import React, { useState, useEffect } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

const Register = () => {
  const { isAuthenticated, login } = useAuth();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [redirecting, setRedirecting] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();  // Add this line to prevent the default form submission behavior
  
    try {
      const response = await fetch('http://localhost:5000/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
        credentials: 'include',
      });
  
      if (response.ok) {
        const data = await response.json();
        setMessage(data.message);

        window.location.href = '/';
      } else {
        const data = await response.json();
        setMessage(data.message);
      }
    } catch (error) {
      console.error('Error during registration:', error);
      setMessage('An error occurred during registration.');
    }
  };
  // useEffect(() => {
  //   const redirectUser = async () => {
  //     if (isAuthenticated && redirecting) {
  //       setRedirecting(false);
  //       await navigate('/', { replace: true });
  //     }
  //   };
  
  //   redirectUser();
  // }, [isAuthenticated, redirecting, navigate]);

  // if (isAuthenticated) {
  //   return <Navigate to="/" replace />;
  // }

  return (
    <div className='setup'>
      <div className='watermark'>
        <div className="register-container">
          <form className="register-form" onSubmit={(e) => handleRegister(e)}>
            <h3>Register</h3>
            <label htmlFor="username">Username</label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)} 
              type="text"
              placeholder="Enter Username"
              id="username"
              name="username"
            />
            <label htmlFor="email">Email</label>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)} 
              type="email"
              placeholder="Enter Email"
              id="email"
              name="email"
            />
            <label htmlFor="password">Password</label> 
            <input
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              placeholder="Enter Password"
              id="password"
              name="password"
            />
            <button type="submit">Register</button>
          </form>
          <p>
            Already have an account? <Link to="/login" className='link'>Log in here</Link>
          </p>
          {message && <p className="error-message">{message}</p>}
        </div>
      </div>
    </div>
  );
};

export default Register;