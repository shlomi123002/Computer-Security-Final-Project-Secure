import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Box, Button } from '@mui/material';
import { styled } from '@mui/system';
import axios from 'axios';
import { useNavigate, useLocation } from 'react-router-dom';
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


const ClientList = () => {
  const [clients, setClients] = useState([]);
  const navigate = useNavigate(); 
  const { state } = useLocation();
  const { username } = state;

  const handleLoginPage = () => {
    navigate('/');
  };

const handleDashboard = () => {
    navigate('/dashboard', { state: { username : username } } );
};


  useEffect(() => {
    // Fetch clients from the backend
    const fetchClients = async () => {
      try {
        const response = await axios.get('http://localhost:8000/client-table');
        setClients(response.data); // Assume the data is an array of clients
      } catch (error) {
        console.error('Error fetching clients:', error);
        alert('Failed to fetch client data');
      }
    };

    fetchClients();
  }, []);

  return (
    <FullScreenContainer>
      <Box m={4}>
        <Typography variant="h4" gutterBottom align="center">
          Client List 
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>First Name</TableCell>
                <TableCell>Last Name</TableCell>
                <TableCell>Phone Number</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Package</TableCell>
                <TableCell>Sector</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {clients.map((client) => (
                <TableRow key={client.id}>
                  <TableCell>{client.clientFirstName}</TableCell>
                  <TableCell>{client.clientLastName}</TableCell>
                  <TableCell>{client.clientPhoneNumber}</TableCell>
                  <TableCell>{client.clientEmail}</TableCell>
                  <TableCell>{client.selectedPackage}</TableCell>
                  <TableCell>{client.selectedSector}</TableCell>

                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      <Box mt={2} textAlign="center">
          <Button color="secondary" onClick={handleDashboard}>
          Dashboard
          </Button>
      </Box>
      <Box mt={2} textAlign="center">
          <Button color="secondary" onClick={handleLoginPage}>
          Log Out
          </Button>
      </Box>
      </Box>
    </FullScreenContainer>
  );
};

export default ClientList;
