import React, { useState } from 'react';
import './App.css';
import axios from 'axios';
import logoImage from './images/pathholetrackerlogo.png';
import { BrowserRouter as Router, Route, Redirect } from 'react-router-dom';



const App = () => {
  const [showLoginForm, setShowLoginForm] = useState(true);
  const [showRegistrationForm, setShowRegistrationForm] = useState(false);

  const toggleLoginForm = () => {
    setShowLoginForm(!showLoginForm);
    setShowRegistrationForm(false);
  };


  const toggleRegistrationForm = () => {
    setShowRegistrationForm(!showRegistrationForm);
    setShowLoginForm(false);
  };

  const toggleOTPForm = () => {
     window.location.href = 'http://localhost:5000/otplogin'
  };
  

  const [signPhone, setSignPhone] = useState('');
  const [signPassword, setSignPassword] = useState('');
  const [loginError, setLoginError] = useState('');

  const validateLoginForm = () => {
    setLoginError('');
    if (!signPhone || !signPassword) {
      setLoginError('All fields are required');
      return false;
    }
    return true;
  };

  const handleLogin = async() => {
    if (validateLoginForm()) {
      try {
          const response = await axios.post('http://127.0.0.1:5000/login', {
            signPhone,
            signPassword
          });
          if (response.data.message == 1){
             window.location.href = 'http://localhost:5000/homepage'
          }else{
            setLoginError('Invalid Login Credentials! Try again');
          }
        }catch (error) {
          setLoginError('Error registering user:', error.message);
        }
    }
  };

  // Login form state and validation
  const [regPhone, setRegPhone] = useState('');
  const [regPassword, setRegPassword] = useState('');
  const [regName, setRegName] = useState('');
  const [regMail, setRegMail] = useState('');
  const [registerError, setRegisterError] = useState('');

   const validateRegisterForm = () => {
    setRegisterError('');
    if (!regPhone || !regPassword || !regName || !regMail) {
      setRegisterError('All fields are required');
      return false;
    }
    return true;
  };

  const handleRegister = async () => {
    if (validateRegisterForm()) {
        try {
          const response = await axios.post('http://127.0.0.1:5000/register', {
            regPhone,
            regPassword,
            regName,
            regMail,
          });
          if (response.data.message == 0){
            setRegisterError('User Details Already Registered. Please login.');
          }else{
            setRegisterError('Registration Completed. Please Login!');
          }
        }catch (error) {
          setRegisterError('Error registering user:', error.message);
        }
    }
  };

  return (
    <div className="indexBackground">
      <img
        src={logoImage}
        alt="Logo"
        style={{ width: '100px', height: '100px', marginBottom: '20px', background: '#ffffff7d' }}
      />

      <div
        style={{
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          padding: '20px',
          borderRadius: '10px',
          width: '300px',
          textAlign: 'center',
        }}
      >
        {/* Login form */}
        {showLoginForm && (
          <form className="indexform">
            <h3>Sign In</h3>
            <label>
              <input
                type="text"
                name="signPhone"
                className="inputbox"
                placeholder="Phone Number"
                value={signPhone}
                onChange={(e) => setSignPhone(e.target.value)}
              />
            </label>
            <br />
            <label>
              <input
                type="password"
                name="signPassword"
                className="inputbox"
                placeholder="Password"
                value={signPassword}
                onChange={(e) => setSignPassword(e.target.value)}
              />
            </label>
            <br />
            <button type="button" className="submitbutton" onClick={handleLogin}>
              Sign In
            </button>
            {loginError && <p style={{ color: 'red' }}>{loginError}</p>}
            <p>
              Not Registered?{' '}
              <span id="registerlink" className="link" onClick={toggleRegistrationForm}>
                Register
              </span>{' '}
              Here
            </p>
            <p>
              Mail OTP?{' '}
              <span id="mailottplink" className="link" onClick={toggleOTPForm}>
                Login
              </span>{' '}
              Here
            </p>
          </form>
        )}

        {/* Registration form */}
        {showRegistrationForm && (
          <form className="indexform registrationForm">
            <h3>Register</h3>
            <label>
              <input type="text" name="regName" className="inputbox" placeholder="Full Name" value={regName} onChange={(e) => setRegName(e.target.value)} />
            </label>
            <br />
            <label>
              <input type="text" name="regPhone" className="inputbox" placeholder="Phone" value={regPhone} onChange={(e) => setRegPhone(e.target.value)} />
            </label>
            <br />
            <label>
              <input type="text" name="regMail" className="inputbox" placeholder="Email" value={regMail} onChange={(e) => setRegMail(e.target.value)} />
            </label>
            <br />
            <label>
              <input type="password" name="regPassword" className="inputbox" placeholder="Password" value={regPassword} onChange={(e) => setRegPassword(e.target.value)} />
            </label>
            <br />
            <button type="button" className="submitbutton" onClick={handleRegister}>
              Register
            </button>
            {registerError && <p style={{ color: 'red' }}>{registerError}</p>}
            <p>
              Already Registered?{' '}
              <span id="loginlink" className="link" onClick={toggleLoginForm}>
                Login Here!
              </span>{' '}
              Here
            </p>
          </form>
        )}
      </div>
    </div>
  );
};

export default App;
