// components/Contribute.js
import React, { useState } from 'react';
import '../styles.css';

function Contribute({ onNavigate }) {
  const [amount, setAmount] = useState('');

  const handleContribute = () => {
    console.log('Contributing amount:', amount);
  };

  return (
    <div className="contribute-page">
      <div className="navbar">
        <button className="close-button" onClick={() => onNavigate('community')}>X</button>
      </div>
      <h2 className="page-header">Contribute</h2>
      <div className="form-card">
        <input
          type="number"
          placeholder="Enter the Amount ($)"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="input-field"
        />
        <div className="action-buttons">
          <button className="action-button submit" onClick={handleContribute}>Submit</button>
          <button className="action-button cancel" onClick={() => onNavigate('community')}>Cancel</button>
        </div>
      </div>
    </div>
  );
}

export default Contribute;
