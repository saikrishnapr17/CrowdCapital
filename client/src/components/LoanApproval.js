// components/LoanApproval.js
import React from 'react';
import '../styles.css';

function LoanApproval({ onNavigate }) {
  const handleApprove = () => {
    console.log('Loan approved');
  };

  const handleDeny = () => {
    console.log('Loan denied');
  };

  return (
    <div className="loan-approval-page">
      <div className="navbar">
        <button className="close-button" onClick={() => onNavigate('community')}>X</button>
      </div>
      <h2 className="page-header">Loan Approval</h2>
      <div className="form-card">
        <p><strong>Loan Amount Requested:</strong> $2000</p>
        <p><strong>Requested By:</strong> John Doe</p>
        <p><strong>Approved By:</strong></p>
        <ul className="contributors-list">
          <li>Name 1</li>
          <li>Name 2</li>
          <li>Name 3</li>
        </ul>
        <p><strong>Reason for Loan:</strong> Description</p>
        <div className="action-buttons">
          <button className="action-button submit" onClick={handleApprove}>Approve</button>
          <button className="action-button cancel" onClick={handleDeny}>Deny</button>
        </div>
      </div>
    </div>
  );
}

export default LoanApproval;
