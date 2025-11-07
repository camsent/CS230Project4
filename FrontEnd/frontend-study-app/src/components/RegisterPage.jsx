import React, { useState } from 'react';
import './LoginPage.css'
import { FaUser, FaLock } from "react-icons/fa"
import { Link } from 'react-router-dom';

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


const RegisterPage = ({ onChange }) => {

    const [error, setError] = useState(null);
    const [data, setData] = useState({ username: '', password: '' });

    useEffect(() => {
        onChange(data);
    }, [data, onChange]);

    const handleSignUp = async (e) => {
        e.preventDefault();
        const { username, password } = data;

        try {
            await registerUser(username, password);
            await loginUser(username, password); 
            alert('SignUp successful and logged in!');
            setError(null);
        } catch (err) {
            setError(err.message);
        }
    };


    return (
        <div className="wrapper">
            <form action=''>
                <h1>Sign Up</h1>
                <div className="input-box">
                    <input type="text" 
                    placeholder="Username" 
                    value={data.username}
                    onChange={(e) => setData({ ...data, username: e.target.value })} required />
                    <FaUser className='icon' />
                </div>
                <div className="input-box">
                    <input type="password" 
                    placeholder="Password"
                    value={data.password}
                    onChange={(e) => setData({ ...data, password: e.target.value })} required />
                    <FaLock className='icon' />
                </div>
                
                    <button type="submit">Sign Up</button>
                    {error && <p style={{ color: 'red' }}>{error}</p>}  

                <div className="register-link">
                    <p>Already have an account? <Link to="/">Login</Link></p>
                </div>
            </form>
        </div>
    )
}

export default RegisterPage;