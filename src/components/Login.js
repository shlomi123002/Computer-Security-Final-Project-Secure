import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper, Link } from '@mui/material';
import { styled } from '@mui/system';
import { useNavigate } from 'react-router-dom';
import BackgroundImage  from '../images/communication_LTD.jpg'; 

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

// LoginWrapper is centered within the full screen container
const LoginWrapper = styled(Paper)({
  padding: '40px',
  maxWidth: '400px',
  backgroundColor: '#f5f5f5',
});

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username === '1' && password === '1') { 
      navigate('/Dashboard'); // פנייה לבאק כדי לבדוק
    } else {
      alert('Invalid username or password');
    }
  };

  return (
    <FullScreenContainer>
      <LoginWrapper elevation={6}>
        <Typography variant="h3" align="center" gutterBottom>
          Comunication LTD
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