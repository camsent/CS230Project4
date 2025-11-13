import React, { useState } from 'react';
import './LoginPage.css'
import { FaUser, FaLock } from "react-icons/fa"
import { useNavigate, Link } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:8000';

export async function loginUser(username, password) {
    const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include', 
        body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
        throw new Error('Login failed');
    }

    return await response.json();
}

const LoginPage = () => {

    const [data, setData] = useState({ username: '', password: '' });
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        const { username, password } = data;

        try {
            await loginUser(username, password);
            alert('Login successful!');
            navigate('/home');
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="wrapper">
            <form onSubmit={handleLogin}>
                <h1>Login</h1>
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
                <button type="submit" disabled={!data.username || !data.password}>Login</button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <div className="register-link">
                    <p>Don’t have an account? <Link to="/register">Register</Link></p>
                </div>
            </form>
        </div>
    );
}

export default LoginPage;