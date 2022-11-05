import React from "react";
import { NavLink } from 'react-router-dom';

export default function Navbar() {
    return (
        <div className="navbar">
            <NavLink to='/'>Home</NavLink>
            <NavLink to='/About'>About</NavLink>
            <NavLink to='/Community'>Community</NavLink>
        </div>
    );
}