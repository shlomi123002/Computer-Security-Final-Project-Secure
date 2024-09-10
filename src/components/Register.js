import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper, Link } from '@mui/material';
import { styled } from '@mui/system';
import axios from 'axios';
import passwordValue from "../backend/config.json";


const RegisterWrapper = styled(Paper)({
  padding: '40px',
  margin: '20px auto',
  maxWidth: '400px',
  backgroundColor: '#f5f5f5',
});

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/register/', {
        username: username,
        email: email,
        password: password,
      });
      alert(`User ${response.data.username} registered successfully`);
    } catch (error) {
      console.error("There was an error registering the user!", error);
      alert('One of the fields is incorrect');
    }
  };

  return (
    <RegisterWrapper elevation={6}>
      <Typography variant="h5" align="center" gutterBottom>
        Create an Account
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
          label="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
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
        <Typography variant="body1">
          The password must contain {passwordValue.password_len} characters. <br/>
          The password must contain {passwordValue.password_requirements.uppercase} upper case. <br/>
          The password must contain {passwordValue.password_requirements.special_char} special characters. <br/>
          The password must contain {passwordValue.password_requirements.number} numbers. <br/>
        </Typography>
        <Box mt={3}>
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Register
          </Button>
        </Box>
      </form>
    </RegisterWrapper>
  );
};

export default Register;
