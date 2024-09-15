import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper, Link } from '@mui/material';
import { styled } from '@mui/system';
import { useNavigate } from 'react-router-dom';
import BackgroundImage from '../images/communication_LTD.jpg';
import axios from 'axios';

const FullScreenContainer = styled('div')({
  height: '100vh',
  width: '100vw',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  backgroundImage: `url(${BackgroundImage})`,
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  backgroundRepeat: 'no-repeat',
});

const LoginWrapper = styled(Paper)({
  padding: '40px',
  maxWidth: '400px',
  backgroundColor: '#f5f5f5',
});

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // To display error messages
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Replace with your actual login API endpoint
      const response = await axios.post('http://localhost:8000/login/', {
        username: username,
        password: password,
      });

      if (response.status === 200) {
        // Navigate to the dashboard on successful login
        navigate('/Dashboard');
      } else {
        setError('Invalid username or password');
      }
    } catch (error) {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        setError(error.response.data.detail || 'An error occurred');
      } else if (error.request) {
        // The request was made but no response was received
        setError('No response from server');
      } else {
        // Something happened in setting up the request that triggered an Error
        setError('Error in setting up the request');
      }
    }
  };

  return (
    <FullScreenContainer>
      <LoginWrapper elevation={6}>
        <Typography variant="h3" align="center" gutterBottom>
          Communication LTD
        </Typography>
        <Typography variant="h5" align="left" gutterBottom>
          Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            fullWidth
            margin="normal"
            required
          />
          {error && (
            <Typography color="error" align="center" marginY={2}>
              {error}
            </Typography>
          )}
          <Box mt={3}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Login
            </Button>
          </Box>
        </form>
        <Box mt={2}>
          <Typography align="center">
            <Link href="/forgot-password" color="secondary">
              Forgot your password?
            </Link>
          </Typography>
          <Typography align="center">
            <Link href="/Register" color="secondary">
              Register
            </Link>
          </Typography>
        </Box>
      </LoginWrapper>
    </FullScreenContainer>
  );
};

export default Login;
