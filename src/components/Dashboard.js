import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper, MenuItem, Select, InputLabel, FormControl } from '@mui/material';
import { styled } from '@mui/system';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import BackgroundImage from '../images/background.jpg';

const FullScreenContainer = styled('div')({
  height: '110vh',
  width: '100vw',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  backgroundImage: `url(${BackgroundImage})`,
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  backgroundRepeat: 'no-repeat',
});


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
  const [selectedPackage, setSelectedPackage] = useState('');
  const [selectedSector, setSelectedSector] = useState('');
  const navigate = useNavigate();  
  const { state } = useLocation();
  const { username } = state;

  // Define the available packages
  const packages = [
    { name: 'Basic', speed: '50 Mbps', data: '200GB', price: '$20' },
    { name: 'Normal', speed: '200 Mbps', data: '500GB', price: '$30' },
    { name: 'Premium', speed: '400 Mbps', data: '1000GB', price: '$40' },
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();

    const clientData = {
      userName: username,
      clientFirstName,
      clientLastName,
      clientPhoneNumber,
      clientEmail,
      selectedPackage, // Include the selected package
      selectedSector
    };

    try {
      const response = await axios.post('http://localhost:8000/Dashboard', clientData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
    
      if (response.status === 200) {
        alert('Client added successfully');
        setFirstName('');
        setLastName('');
        setPhoneNumber('');
        setEmail('');
        setSelectedPackage('');
      } else {
        alert('Failed to add client');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.');
    }
  }

  const handleViewClients = () => {
    navigate('/client-table', { state: { username: username ,selectedPackage : selectedPackage , selectedSector : selectedSector } });
  };

  const handleChangePassword = () => {
    navigate('/change-password', { state: { username: username } });
  };

  const handleLoginPage = () => {
    navigate('/');
  };

  return (
    <FullScreenContainer>
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

          <FormControl fullWidth margin="normal" required>
            <InputLabel>Select Package</InputLabel>
            <Select
              value={selectedPackage}
              onChange={(e) => setSelectedPackage(e.target.value)}
              label="Select Package"
            >
              {packages.map((pkg) => (
                <MenuItem key={pkg.name} value={pkg.name}>
                  {pkg.name} - {pkg.speed}, {pkg.data}, {pkg.price}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth margin="normal" required>
            <InputLabel>Select Sector</InputLabel>
            <Select
              value={selectedSector}
              onChange={(e) => setSelectedSector(e.target.value)}
              label="Select Sector"
            >
              <MenuItem value="Private customer">Private customer</MenuItem>
              <MenuItem value="Small Business">Small Business</MenuItem>
              <MenuItem value="Corporates">Corporates</MenuItem>
            </Select>
          </FormControl>

          <Box mt={3}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Add Client
            </Button>
          </Box>
        </form>

        <Box mt={2} textAlign="center">
          <Button onClick={handleViewClients} variant="contained" color="inherit" fullWidth>
            View All Clients
          </Button>
        </Box>

        <Box mt={2} textAlign="center">
          <Button color="secondary" onClick={handleChangePassword}>
            Change Password
          </Button>
        </Box>
        <Box mt={2} textAlign="center">
          <Button color="secondary" onClick={handleLoginPage}>
            Log Out
          </Button>
        </Box>
      </DashboardWrapper>
    </FullScreenContainer>
  );
};

export default Dashboard;