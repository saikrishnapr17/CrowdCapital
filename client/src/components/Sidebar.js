// components/Sidebar.js
import React from 'react';

function Sidebar({ isVisible, onClose }) {
  return (
    
    <div className={`sidebar ${isVisible ? 'visible' : 'hidden'}`}>
      {isVisible && (
        <button className="close-button" onClick={onClose}>✖</button>
      )}
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
        <p>Rama Riaz</p>
        <p>Web Developer</p>
      </div>
    </div>
  );
}

export default Sidebar;
