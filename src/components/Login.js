import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper } from '@mui/material';
import { styled } from '@mui/system';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import BackgroundImage from '../images/background.jpg';

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
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/login/', {
        username: username,
        password: password
      });

      if (response.status === 200) {
        navigate('/Dashboard', { state: { username } });
      } else {
        setError('Invalid username or password');
      }
    } catch (error) {
      if (error.response) {
        setError(error.response.data.detail || 'An error occurred');
      } else if (error.request) {
        setError('No response from server');
      } else {
        setError('Error in setting up the request');
      }
    }
  };

  const handleForgotPassword = () => {
    navigate('/forgot-password', { state: { username } });
  };

  const handleRegister = () => {
    navigate('/Register', { state: { username } });
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
            <Button onClick={handleForgotPassword} color="secondary">
              Forgot your password?
            </Button>
          </Typography>
          <Typography align="center">
            <Button onClick={handleRegister} color="secondary">
              Register
            </Button>
          </Typography>
        </Box>
      </LoginWrapper>
    </FullScreenContainer>
  );
};

export default Login;