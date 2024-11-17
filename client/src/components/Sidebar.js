// components/Sidebar.js
import React from 'react';

function Sidebar({ isOpen, onNavigate }) {
  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <h2>uifry</h2>
      <ul>
        <li onClick={() => onNavigate('dashboard')}>Dashboard</li>
        <li onClick={() => onNavigate('analytics')}>Analytics</li>
        <li onClick={() => onNavigate('my-wallet')}>My Wallet</li>
        <li onClick={() => onNavigate('accounts')}>Accounts</li>
        <li onClick={() => onNavigate('settings')}>Settings</li>
        <li onClick={() => onNavigate('security')}>Security</li>
        <li onClick={() => onNavigate('help')}>Help Centre</li>
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
