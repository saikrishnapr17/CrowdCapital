import React, { useState } from 'react';
import '../styles.css';
import { FaTimes } from 'react-icons/fa';

function SMSFraudCheck({ onNavigate }) {
  const [smsContent, setSmsContent] = useState('');
  const [result, setResult] = useState(null);
  const [isChecking, setIsChecking] = useState(false);

  const handleCheckClick = async () => {
    setIsChecking(true);
    setResult(null);
    try {
      const response = await fetch('http://localhost:5000/check_sms', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sms_content: smsContent }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsChecking(false);
    }
  };

  return (
    <div className="sms-fraud-check-container">
      <div className="sms-fraud-header">
        <button onClick={() => onNavigate('dashboard')} className="close-button">
          <FaTimes />
        </button>
        <h1>SMS Fraud Check</h1>
      </div>
      <div className="sms-fraud-input-section">
        <textarea
          className="sms-fraud-input"
          placeholder="Enter SMS content here..."
          value={smsContent}
          onChange={(e) => setSmsContent(e.target.value)}
        ></textarea>
        <button className="sms-fraud-check-button" onClick={handleCheckClick}>Check Now</button>
        <div className="sms-fraud-result">
          {isChecking ? (
            <p>Waiting for API data...</p>
          ) : result ? (
            <p>{result.message}</p>
          ) : null}
        </div>
      </div>
    </div>
  );
}

export default SMSFraudCheck;
