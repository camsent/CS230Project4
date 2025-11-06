import React, { useState } from 'react';
import './LoginPage.css'
import { FaUser, FaLock } from "react-icons/fa"
import { Link } from 'react-router-dom';

const RegisterPage = () => {

const [username, setUsername] = useState('')
const [password, setPassword] = useState('')

const handleSubmit = (e) => {
        e.preventDefault();
}

    return (
        <div className="wrapper">
            <form action=''>
                <h1>Sign Up</h1>
                <div className="input-box">
                    <input type="text" 
                    placeholder="Username" 
                    onChange={(e) => setUsername(e.target.value)} required />
                    <FaUser className='icon' />
                </div>
                <div className="input-box">
                    <input type="password" 
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)} required />
                    <FaLock className='icon' />
                </div>
                <Link to="/">
                    <button type="submit">Sign Up</button>
                </Link>    
                <div className="register-link">
                    <p>Already have an account? <Link to="/">Login</Link></p>
                </div>
            </form>
        </div>
    )
}

export default RegisterPage;