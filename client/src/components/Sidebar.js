// components/Sidebar.js
import React from 'react';

function Sidebar() {
  return (
    <div className="sidebar">
      <h2>uifry</h2>
      <ul>
        <li>Dashboard</li>
        <li>Analytics</li>
        <li>My Wallet</li>
        <li>Accounts</li>
        <li>Settings</li>
        <li>Security</li>
        <li>Help Centre</li>
        <li>Dark Mode</li>
      </ul>
      <div className="user-info">
        <img src="/path/to/user-image.png" alt="User" />
        <p>Ali Riaz</p>
        <p>Web Developer</p>
      </div>
    </div>
  );
}

export default Sidebar;