// components/RequestLoan.js
import React, { useState } from 'react';
import '../styles.css';

function RequestLoan({ onNavigate, userId }) {
  const [amount, setAmount] = useState('');
  const [reason, setReason] = useState('');
  const [emi, setEmi] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async () => {
    setMessage('');
    try {
      const response = await fetch(`http://127.0.0.1:5000/community/${userId}/request_loan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: Number(amount),
          description: reason,
          credit_score: emi, // Assuming EMI field as credit_score placeholder
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(data.message);
      } else {
        const errorData = await response.json();
        setMessage(errorData.error);
      }
    } catch (error) {
      setMessage('An error occurred. Please try again.');
      console.error('Error:', error);
    }
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
          placeholder="EMI:" // Placeholder for credit score input
          value={emi}
          onChange={(e) => setEmi(e.target.value)}
          className="input-field"
        />
        <div className="action-buttons">
          <button className="action-button submit" onClick={handleSubmit}>Submit</button>
          <button className="action-button cancel" onClick={() => onNavigate('community')}>Cancel</button>
        </div>
        {message && <p className="loan-message">{message}</p>}
      </div>
    </div>
  );
}

export default RequestLoan;

