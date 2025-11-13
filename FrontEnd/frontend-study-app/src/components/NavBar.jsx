import './NavBar.css'
import { Link } from 'react-router-dom'
import { GiNotebook } from "react-icons/gi";

export default function Navbar() {
    return <nav className="nav"> 
    <div className='title-icon'>
        <a href="/" className="site-title">Study App</a>
         <GiNotebook className='icon'/>
    </div>
        <ul>
            <li className='active'>
                <a href="/home">Home</a>
            </li>
            <li className='active'>
                <a href="/Edit">Edit</a>
            </li>
            <li className='active'>
                <a href="/Upload">Upload</a>
            </li>
        </ul>
    </nav>
}