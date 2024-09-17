import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper } from '@mui/material';
import { styled } from '@mui/system';
import CloseIcon from "@mui/icons-material/Close";
import CheckIcon from "@mui/icons-material/Check";
import passwordValue from "../backend/config.json";
import axios from "axios";
import { useNavigate } from 'react-router-dom';

const ChangePasswordWrapper = styled(Paper)({
  padding: '40px',
  margin: '20px auto',
  maxWidth: '400px',
  backgroundColor: '#f5f5f5',
});

const PasswordChange = () => {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [passwordValidations, setPasswordValidations] = useState({
    length: false,
    uppercase: false,
    specialChar: false,
    number: false,
  });
  const navigate = useNavigate();  // Initialize useNavigate

  const requirementStyle = (isValid) => ({
    display: "flex",
    alignItems: "center",
    color: isValid ? "green" : "red",
    marginTop: "5px",
  });

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setNewPassword(value);

    // Check each password requirement
    setPasswordValidations({
      length: value.length >= passwordValue.password_len,
      uppercase: /[A-Z]/.test(value),
      specialChar: /[!@#$%^&*(),.?":{}|<>]/.test(value),
      number: /[0-9]/.test(value),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.put('http://localhost:8000/change-password/', {
        user_id: 25, 
        current_password: currentPassword,
        new_password: newPassword,
      });
      alert(response.data.msg);
      navigate('/dashboard'); // Navigate to dashboard on successful password change
    } catch (error) {
      alert("Failed to change password. Please check your current password.");
    }
  };

  const handleBackToDashboard = () => {
    navigate('/dashboard'); // Navigate to dashboard
  };

  const handleBackToLogin = () => {
    navigate('/'); // Navigate to login page
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
          onChange={handlePasswordChange}
          fullWidth
          margin="normal"
          required
        />
        <Typography style={requirementStyle(passwordValidations.length)}>
          {passwordValidations.length ? <CheckIcon /> : <CloseIcon />} Must be
          at least {passwordValue.password_len} characters.
        </Typography>
        <Typography style={requirementStyle(passwordValidations.uppercase)}>
          {passwordValidations.uppercase ? <CheckIcon /> : <CloseIcon />} Must
          contain at least {passwordValue.password_requirements.uppercase}{" "}
          uppercase letter.
        </Typography>
        <Typography style={requirementStyle(passwordValidations.specialChar)}>
          {passwordValidations.specialChar ? <CheckIcon /> : <CloseIcon />} Must
          contain at least {passwordValue.password_requirements.special_char}{" "}
          special character.
        </Typography>
        <Typography style={requirementStyle(passwordValidations.number)}>
          {passwordValidations.number ? <CheckIcon /> : <CloseIcon />} Must
          contain at least {passwordValue.password_requirements.number} number.
        </Typography>
        <Box mt={3}>
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Change Password
          </Button>
          <Box mt={2} textAlign="center">
            <Button color="secondary" onClick={handleBackToDashboard}>
              Back to Dashboard
            </Button>
          </Box>
          <Box mt={2} textAlign="center">
            <Button color="secondary" onClick={handleBackToLogin}>
              Back to Login
            </Button>
          </Box>
        </Box>
      </form>
    </ChangePasswordWrapper>
  );
};

export default PasswordChange;
