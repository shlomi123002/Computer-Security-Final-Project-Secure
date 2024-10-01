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

const ForgotPasswordWrapper = styled(Paper)({
  padding: '40px',
  margin: '20px auto',
  maxWidth: '400px',
  backgroundColor: '#f5f5f5',
});

const ForgotPassword = () => {
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();



  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/forgot-password', {
        user_name: username,
      });
      setMessage(response.data.msg);
      // Redirect to reset password page after recovery code is sent
      navigate('/reset-password', { state: { username: username } });
    } catch (error) {
      if (error.response && error.response.status === 404) {
        setError('Email not found');
      } else {
        setError('User not found');
      }
    }
  };

  return (
    <FullScreenContainer>
      <ForgotPasswordWrapper elevation={6}>
        <Typography variant="h4" align="center" gutterBottom>
          Forgot Password
        </Typography>
        <Typography variant="h6" align="left" gutterBottom>
          Enter your username to receive an email to reset your password.
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            fullWidth
            margin="normal"
            required
          />
          {error && (
            <Typography align="center" color="error" mt={2}>
              {error}
            </Typography>
          )}
          {message && (
            <Typography align="center" color="primary" mt={2}>
              {message}
            </Typography>
          )}
          <Box mt={3}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Send Recovery Code
            </Button>
          </Box>
        </form>
        <Typography align="center" mt={2}>
          <Button onClick={() => navigate('/')} color="secondary">
            Back to Login
          </Button>
        </Typography>
      </ForgotPasswordWrapper>
    </FullScreenContainer>
  );
};

export default ForgotPassword;
