// components/WithdrawContribution.js
import React, { useState } from 'react';
import '../styles.css';

function WithdrawContribution({ onNavigate }) {
  const [withdrawAmount, setWithdrawAmount] = useState('');

  const handleWithdraw = () => {
    console.log('Withdraw amount:', withdrawAmount);
  };

  return (
    <div className="withdraw-contribution-page">
      <div className="navbar">
        <button className="close-button" onClick={() => onNavigate('community')}>X</button>
      </div>
      <h2 className="page-header">Withdraw Contribution</h2>
      <div className="form-card">
        <p><strong>Amount Contributed:</strong> $1500</p>
        <input
          type="number"
          placeholder="Enter Amount ($)"
          value={withdrawAmount}
          onChange={(e) => setWithdrawAmount(e.target.value)}
          className="input-field"
        />
        <div className="action-buttons">
          <button className="action-button submit" onClick={handleWithdraw}>Withdraw</button>
          <button className="action-button cancel" onClick={() => onNavigate('community')}>Cancel</button>
        </div>
      </div>
    </div>
  );
}

export default WithdrawContribution;
