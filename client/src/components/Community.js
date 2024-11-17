// components/Community.js
import React from 'react';
import '../styles.css';

function Community({ onNavigate }) {
  return (
    <div className="community-page">
      <div className="navbar">
        <button className="close-button" onClick={() => onNavigate('dashboard')}>X</button>
      </div>
      <h2 className="community-header">Community</h2>
      <div className="community-card">
        <h3 className="community-heading">Amount</h3>
        <p className="community-amount">$30,000</p>
      </div>
      <div className="community-card">
        <h3 className="community-heading">Interest Earned (Overall)</h3>
        <p className="community-interest">Sum of Interests</p>
      </div>
      <div className="community-card">
        <h3 className="community-heading">See Contributors</h3>
        <ul className="contributors-list">
          <li>Person A</li>
          <li>Person B</li>
          <li>Person C</li>
          <li>Person D</li>
        </ul>
      </div>
      <div className="community-actions">
        <button className="community-button" onClick={() => onNavigate('contribute')}>Contribute</button>
        <button className="community-button" onClick={() => onNavigate('request-loan')}>Request Loan</button>
        <button className="community-button" onClick={() => onNavigate('loan-approval')}>Loan Approvals</button>
        <button className="community-button" onClick={() => onNavigate('pay-loan')}>Pay Loan</button>
        <button className="community-button" onClick={() => onNavigate('withdraw-contribution')}>Withdraw Contribution</button>
      </div>
    </div>
  );
}

export default Community;
