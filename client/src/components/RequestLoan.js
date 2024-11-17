// components/RequestLoan.js
import React, { useState } from 'react';
import '../styles.css';

function RequestLoan({ onNavigate }) {
  const [amount, setAmount] = useState('');
  const [reason, setReason] = useState('');
  const [emi, setEmi] = useState('');

  const handleSubmit = () => {
    console.log('Requesting loan for amount:', amount);
  };

  return (
    <div className="request-loan-page">
      <div className="navbar">
        <button className="close-button" onClick={() => onNavigate('community')}>X</button>
      </div>
      <h2 className="page-header">Request Loan</h2>
      <div className="form-card">
        <input
          type="number"
          placeholder="Enter Amount ($)"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="input-field"
        />
        <textarea
          placeholder="Reason for Loan"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          className="input-textarea"
        />
        <input
          type="text"
          placeholder="EMI:"
          value={emi}
          onChange={(e) => setEmi(e.target.value)}
          className="input-field"
        />
        <div className="action-buttons">
          <button className="action-button submit" onClick={handleSubmit}>Submit</button>
          <button className="action-button cancel" onClick={() => onNavigate('community')}>Cancel</button>
        </div>
      </div>
    </div>
  );
}

export default RequestLoan;
