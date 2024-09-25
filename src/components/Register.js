import React, { useState } from "react";
import { TextField, Button, Box, Typography, Paper } from "@mui/material";
import { styled } from "@mui/system";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import CloseIcon from "@mui/icons-material/Close";
import CheckIcon from "@mui/icons-material/Check";
import passwordValue from "../backend/config.json";

const RegisterWrapper = styled(Paper)({
  padding: "40px",
  margin: "20px auto",
  maxWidth: "400px",
  backgroundColor: "#f5f5f5",
});

const requirementStyle = (isValid) => ({
  display: "flex",
  alignItems: "center",
  color: isValid ? "green" : "red",
  marginTop: "5px",
});

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");

  // Track password validation states
  const [passwordValidations, setPasswordValidations] = useState({
    length: false,
    uppercase: false,
    specialChar: false,
    number: false,
  });

  const navigate = useNavigate();

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setPassword(value);

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
      const response = await axios.post('http://localhost:8000/register', {
        username: username,
        email: email,
        password: password,
      });
      alert(`User registered successfully`);
      navigate('/'); // Redirect to login page after successful registration
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
          onChange={handlePasswordChange}
          fullWidth
          margin="normal"
          required
        />

        <Typography variant="body1" gutterBottom>
          Password Requirements:
        </Typography>
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
            Register
          </Button>
          <Typography align="center" marginTop={2}>
            <Button onClick={() => navigate('/')} color="secondary">
              Login Page
            </Button>
          </Typography>
        </Box>
      </form>
    </RegisterWrapper>
  );
};

export default Register;
