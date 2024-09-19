import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper } from '@mui/material';
import { styled } from '@mui/system';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';


const DashboardWrapper = styled(Paper)({
  padding: '40px',
  margin: '20px auto',
  maxWidth: '600px',
  backgroundColor: '#f5f5f5',
});

const Dashboard = () => {
  const [clientFirstName, setFirstName] = useState('');
  const [clientLastName, setLastName] = useState('');
  const [clientPhoneNumber, setPhoneNumber] = useState('');
  const [clientEmail, setEmail] = useState('');
  const navigate = useNavigate();  // Initialize useNavigate
  const {state} = useLocation();
  const { username } = state;

  const handleSubmit = async (e) => {
    e.preventDefault();

    const clientData = {
      userName: username,
      clientFirstName,
      clientLastName,
      clientPhoneNumber,
      clientEmail,
    };

    try {
      const response = await axios.post('http://localhost:8000/Dashboard', clientData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
    
      if (response.status === 200) {
        alert('Client added successfully');
        // Clear the form fields after successful submission
        setFirstName('');
        setLastName('');
        setPhoneNumber('');
        setEmail('');
      } else {
        alert('Failed to add client');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.');
    }
  }

  const handleChangePassword = () => {
    navigate('/change-password', { state: { username: username } });
  };

  const handleLoginPage = () => {
    navigate('/');
  };

  return (
    <DashboardWrapper elevation={6}>
      <Typography variant="h5" align="center" gutterBottom>
        Hello {username}
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Client First Name"
          value={clientFirstName}
          onChange={(e) => setFirstName(e.target.value)}
          fullWidth
          margin="normal"
          required
        />
        <TextField
          label="Client Last Name"
          value={clientLastName}
          onChange={(e) => setLastName(e.target.value)}
          fullWidth
          margin="normal"
          required
        />
        <TextField
          label="Client Phone Number"
          value={clientPhoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          fullWidth
          margin="normal"
          required
        />
        <TextField
          label="Client Email"
          value={clientEmail}
          onChange={(e) => setEmail(e.target.value)}
          fullWidth
          margin="normal"
          required
        />
        <Box mt={3}>
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Add Client
          </Button>
        </Box>
      </form>
      <Box mt={2}>
        <Typography variant="body1">
          Recently added client: {clientFirstName} {clientLastName}
        </Typography>
        <Box mt={2} textAlign="center">
          <Button color="secondary" onClick={handleChangePassword}>
            Change Password
          </Button>
        </Box>
        <Box mt={2} textAlign="center">
          <Button color="secondary" onClick={handleLoginPage}>
            Login Page
          </Button>
        </Box>
      </Box>
    </DashboardWrapper>
  );
};

export default Dashboard;
