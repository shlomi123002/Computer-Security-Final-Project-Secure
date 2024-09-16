import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper } from '@mui/material';
import { styled } from '@mui/system';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

const FullScreenContainer = styled('div')({
  height: '100vh',
  width: '100vw',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  backgroundColor: '#f5f5f5',
});

const ResetPasswordWrapper = styled(Paper)({
  padding: '40px',
  margin: '20px auto',
  maxWidth: '400px',
});

const ResetPassword = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [recoveryCode, setRecoveryCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const email = location.state?.email; // Get email from state

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/reset-password/', {
        email: email,
        recovery_code: recoveryCode,
        new_password: newPassword,
      });
      setMessage(response.data.msg);
      // Redirect to login after successful reset
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (error) {
      setError('Invalid recovery code or failed to reset password');
    }
  };

  return (
    <FullScreenContainer>
      <ResetPasswordWrapper elevation={6}>
        <Typography variant="h5" align="center" gutterBottom>
          Reset Password
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Recovery Code"
            value={recoveryCode}
            onChange={(e) => setRecoveryCode(e.target.value)}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            label="New Password"
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
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
              Reset Password
            </Button>
          </Box>
        </form>
      </ResetPasswordWrapper>
    </FullScreenContainer>
  );
};

export default ResetPassword;
