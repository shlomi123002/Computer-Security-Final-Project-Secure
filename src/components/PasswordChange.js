import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper , Link } from '@mui/material';
import { styled } from '@mui/system';

const ChangePasswordWrapper = styled(Paper)({
  padding: '40px',
  margin: '20px auto',
  maxWidth: '400px',
  backgroundColor: '#f5f5f5',
});

const PasswordChange = () => {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // סימולציה של שינוי סיסמא
    alert('Password changed successfully');
  };

  return (
    <ChangePasswordWrapper elevation={6}>
      <Typography variant="h5" align="center" gutterBottom>
        Change Your Password
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Current Password"
          type="password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
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
        <Box mt={3}>
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Change Password
          </Button>
          <Typography align="center">
            <Link href="/" color="secondary">
              login page
            </Link>
          </Typography>
        </Box>
      </form>
    </ChangePasswordWrapper>
  );
};

export default PasswordChange;
