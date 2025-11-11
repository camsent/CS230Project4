import React, { useState } from 'react';
import './LoginPage.css'
import { FaUser, FaLock } from "react-icons/fa"
import { useNavigate, Link } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:8000';

export async function registerUser(username, password) {
    const response = await fetch(`${API_URL}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: "include",
        body: JSON.stringify({ username, password }),
    });
    
    if (!response.ok) {
        throw new Error("Registration failed");
    }
    return await response.json();
}


const RegisterPage = ({ onChange }) => {

    const [data, setData] = useState({ username: '', password: '' });
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSignUp = async (e) => {
        e.preventDefault();
        const { username, password } = data;

        try {
            await registerUser(username, password);
            // await loginUser(username, password); // auto-login after registration
            alert('Sign up successful! Redirecting to Login...');
            navigate('/');
        } catch (err) {
            setError(err.message);
        }
    };


    return (
        <div className="wrapper">
            <form onSubmit={handleSignUp}>
                <h1>Register</h1>
                <div className="input-box">
                    <input
                        type="text"
                        placeholder="Username"
                        value={data.username}
                        onChange={(e) => setData({ ...data, username: e.target.value })}
                        required
                    />
                    <FaUser className='icon' />
                </div>
                <div className="input-box">
                    <input
                        type="password"
                        placeholder="Password"
                        value={data.password}
                        onChange={(e) => setData({ ...data, password: e.target.value })}
                        required
                    />
                    <FaLock className='icon' />
                </div>
                <button type="submit" disabled={!data.username || !data.password}>Sign Up</button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <div className="register-link">
                    <p>Already have an account? <Link to="/">Login</Link></p>
                </div>
            </form>
        </div>
    );
}

export default RegisterPage;