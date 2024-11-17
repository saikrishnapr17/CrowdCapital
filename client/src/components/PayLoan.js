// components/PayLoan.js
import React, { useState } from 'react';
import '../styles.css';

function PayLoan({ onNavigate }) {
  const [payAmount, setPayAmount] = useState('');

  const handlePay = () => {
    console.log('Paying loan amount:', payAmount);
  };

  const handleDeny = () => {
    console.log('Deny payment');
    onNavigate('community');
  };

  return (
    <div className="pay-loan-page">
      <div className="navbar">
        <button className="close-button" onClick={() => onNavigate('community')}>X</button>
      </div>
      <h2 className="page-header">Pay Loan</h2>
      <div className="form-card">
        <p><strong>Remaining Amount:</strong> $2000</p>
        <input
          type="number"
          placeholder="Enter Amount ($)"
          value={payAmount}
          onChange={(e) => setPayAmount(e.target.value)}
          className="input-field"
        />
        <div className="action-buttons">
          <button className="action-button submit" onClick={handlePay}>Pay</button>
          <button className="action-button cancel" onClick={handleDeny}>Deny</button>
        </div>
      </div>
    </div>
  );
}

export default PayLoan;
