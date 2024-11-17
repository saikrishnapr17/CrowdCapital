// components/Contribute.js
import React, { useState } from 'react';
import '../styles.css';

function Contribute({ onNavigate }) {
  const [amount, setAmount] = useState('');

  const handleSubmit = () => {
    alert(`You have contributed $${amount}`);
    onNavigate('community');
  };

  const handleCancel = () => {
    onNavigate('community');
  };

  return (
    <div className="contribute-page">
      <h2 className="contribute-header">Contribute</h2>
      <input
        type="number"
        className="contribute-input"
        placeholder="Enter the amount ($):"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <div className="contribute-actions">
        <button className="contribute-button submit" onClick={handleSubmit}>Submit</button>
        <button className="contribute-button cancel" onClick={handleCancel}>Cancel</button>
      </div>
    </div>
  );
}

export default Contribute;
