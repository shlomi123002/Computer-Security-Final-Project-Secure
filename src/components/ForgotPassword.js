import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper, Link } from '@mui/material';
import { styled } from '@mui/system';
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

const ForgotPasswordWrapper = styled(Paper)({
  padding: '40px',
  margin: '20px auto',
  maxWidth: '400px',
  backgroundColor: '#f5f5f5',
});

const ForgotPassword = () => {
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // סימולציה של שליחת קוד התאוששות
    alert(`Recovery code sent to ${email}`);
  };

  return (
    <FullScreenContainer>
      <ForgotPasswordWrapper elevation={6}>
        <Typography variant="h5" align="center" gutterBottom>
          Forgot Password
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            fullWidth
            margin="normal"
            required
          />
          <Box mt={3}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Send Recovery Code
            </Button>
            <Typography align="center">
              <Link href="/" color="secondary">
                login page
              </Link>
            </Typography>
          </Box>
        </form>
      </ForgotPasswordWrapper>
    </FullScreenContainer>
  );
};

export default ForgotPassword;
