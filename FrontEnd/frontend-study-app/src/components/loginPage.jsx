import React from 'react';
import './LoginPage.css'
import { FaUser, FaLock } from "react-icons/fa"
import { useNavigate, Link } from 'react-router-dom';

const LoginPage = () => {

    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        const username = e.target.username.value.trim();
        const password = e.target.password.value.trim();

        // Check if both fields are filled (required attributes help too)
        if (username && password) {
            navigate('/home'); // go to home only if inputs are filled
        }
    };

    return (
        <div className="wrapper">
            <form onSubmit={handleSubmit}>
                <h1>Login</h1>
                <div className="input-box">
                    <input type="text" name="username" placeholder="Username" required />
                    <FaUser className='icon' />
                </div>
                <div className="input-box">
                    <input type="password" name="password" placeholder="Password" required />
                    <FaLock className='icon' />
                </div>
                <button type="submit">Login</button>   
                <div className="register-link">
                    <p>Don't have an account? <Link to="/register">Register</Link></p>
                </div>
            </form>
        </div>
    )
}

export default LoginPage;