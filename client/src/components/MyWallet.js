import React, { useState } from 'react';
import TransactionsTable from './TransactionsTable';
import '../styles.css';
import { FaArrowUp, FaArrowDown, FaTimes } from 'react-icons/fa';

function MyWallet({ onNavigate }) {
  const [isSendMoneyVisible, setIsSendMoneyVisible] = useState(false);
  const [isDepositVisible, setIsDepositVisible] = useState(false);
  const [phoneNumber, setPhoneNumber] = useState('');
  const [amount, setAmount] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [depositAmount, setDepositAmount] = useState('');
  const [depositMessage, setDepositMessage] = useState('');

  const handleSendClick = () => {
    setIsSendMoneyVisible(!isSendMoneyVisible);
    setIsDepositVisible(false);
  };

  const handleDepositClick = () => {
    setIsDepositVisible(!isDepositVisible);
    setIsSendMoneyVisible(false);
  };

  const handleConfirmSendClick = async () => {
    setIsSubmitting(true);
    setMessage('');

    try {
      const response = await fetch('http://127.0.0.1:5000/transactions/transfer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sender_id: 'user_id', // Replace 'user_id' with actual sender ID
          recipient_phone: phoneNumber,
          amount,
        }),
      });

      if (response.ok) {
        setMessage('Money sent successfully!');
      } else {
        setMessage('Failed to send money. Please try again.');
      }
    } catch (error) {
      setMessage('An error occurred. Please try again.');
      console.error('Error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleConfirmDepositClick = async () => {
    setIsSubmitting(true);
    setDepositMessage('');

    try {
      const response = await fetch(`http://localhost:5000/users/${phoneNumber}/deposit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amount: depositAmount }),
      });

      if (response.ok) {
        setDepositMessage('Deposit successful!');
      } else {
        setDepositMessage('Failed to deposit. Please try again.');
      }
    } catch (error) {
      setDepositMessage('An error occurred. Please try again.');
      console.error('Error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="my-wallet-container">
      <div className="wallet-header">
        <button onClick={() => onNavigate('dashboard')} className="close-button">
          <FaTimes />
        </button>
        <h1>My Wallet</h1>
      </div>
      <div className="balance-section">
        <div className="balance-card">
          <h2>Balance: $15,595.01</h2>
          <div className="wallet-actions">
            <button className="wallet-action-button" onClick={handleSendClick}>
              <FaArrowUp /> Send
            </button>
            <button className="wallet-action-button" onClick={handleDepositClick}>
              <FaArrowDown /> Deposit
            </button>
          </div>
        </div>
      </div>

      {isSendMoneyVisible && (
        <div className="send-money-section">
          <h3>Send Money</h3>
          <div className="send-money-form">
            <label>
              Recipient Phone Number:
              <input
                type="text"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
              />
            </label>
            <label>
              Amount:
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
              />
            </label>
            <button
              className="confirm-button"
              onClick={handleConfirmSendClick}
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Sending...' : 'Confirm'}
            </button>
            {message && <p className="send-money-message">{message}</p>}
          </div>
        </div>
      )}

      {isDepositVisible && (
        <div className="deposit-section">
          <h3>Deposit Money</h3>
          <div className="deposit-form">
            <label>
              Upload Image:
              <input type="file" />
            </label>
            <label>
              Amount:
              <input
                type="number"
                value={depositAmount}
                onChange={(e) => setDepositAmount(e.target.value)}
              />
            </label>
            <button
              className="confirm-button"
              onClick={handleConfirmDepositClick}
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Depositing...' : 'Submit'}
            </button>
            {depositMessage && <p className="deposit-message">{depositMessage}</p>}
          </div>
        </div>
      )}

      <div className="wallet-transactions-section">
        <h2>Recent Transactions</h2>
        <TransactionsTable />
      </div>
    </div>
  );
}

export default MyWallet;
