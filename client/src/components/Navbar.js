import React from "react";
import { NavLink } from 'react-router-dom';

export default function Navbar() {
    return (
        <nav>
            <div class="navbar">
                <NavLink to='/'>Generate</NavLink>
                <NavLink to='/About'>About</NavLink>
                <NavLink to='/Community'>Community</NavLink>
            </div>
        </nav>
    );
}