import React from "react";
import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="navbar">
      <div className="navbar-text">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/About">About</NavLink>
        <NavLink to="/Community">Community</NavLink>
      </div>
      <div className="donate">
        <NavLink className="donate-button" to="/Donate">Donate</NavLink>  
      </div>
    </div>
  );
}
