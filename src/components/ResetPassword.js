import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper, Link } from '@mui/material';
import { styled } from '@mui/system';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import CloseIcon from "@mui/icons-material/Close";
import CheckIcon from "@mui/icons-material/Check";
import passwordValue from "../backend/config.json";
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


const requirementStyle = (isValid) => ({
  display: "flex",
  alignItems: "center",
  color: isValid ? "green" : "red",
  marginTop: "5px",
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
  const [passwordValidations, setPasswordValidations] = useState({
    
    length: false,
    uppercase: false,
    specialChar: false,
    number: false,
  });

  const username = location.state?.username;

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setNewPassword(value);

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
      const response = await axios.post('http://localhost:8000/reset-password/', {
        user_name : username,
        recovery_code: recoveryCode,
        new_password: newPassword,
      });
      setMessage(response.data.msg);
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
            <Typography align="center">
            <Button onClick={()=>{navigate('/');}} color="secondary">
              Login page
            </Button>
          </Typography>
          </Box>
        </form>
      </ResetPasswordWrapper>
    </FullScreenContainer>
  );
};

export default ResetPassword;
