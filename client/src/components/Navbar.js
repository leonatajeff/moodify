import React from "react";
import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="navbar">
      <div className="navbar-text">
        <NavLink to="/" activeStyle={{ color:'white' }}>Home</NavLink>
        <NavLink to="/About" activeStyle={{ color:'white' }}>About</NavLink>
        <NavLink to="/Community" activeStyle={{ color:'white' }}>Community</NavLink>
      </div>
      <div className="donate-nav">
        <NavLink className="donate-nav-button" to="/Donate">
          Send Love
        </NavLink>
      </div>
    </div>
  );
}
