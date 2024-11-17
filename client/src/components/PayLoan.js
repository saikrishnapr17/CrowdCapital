import React, { useState } from 'react';
import '../styles.css';

function PayLoan({ onNavigate, userId, loanId }) {
  const [payAmount, setPayAmount] = useState('');
  const [message, setMessage] = useState('');

  const handlePay = async () => {
    setMessage('');
    try {
      const response = await fetch(`http://127.0.0.1:5000/community/${userId}/loan/${loanId}/make_payment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          payment_amount: Number(payAmount),
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

  const handleDeny = () => {
    setMessage('');
    onNavigate('community');
  };

  return (
    <div className="pay-loan-page">
      <div className="navbar">
        <button className="close-button" onClick={() => onNavigate('community')}>X</button>
      </div>
      <h2 className="page-header">Pay Loan</h2>
      <div className="form-card">
        <p><strong>Remaining Amount:</strong> $2000</p> {/* Replace with dynamic remaining amount */}
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
        {message && <p className="loan-message">{message}</p>}
      </div>
    </div>
  );
}

export default PayLoan;
