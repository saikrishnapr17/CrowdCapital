// components/MyWallet.jsx
import React from 'react';
import TransactionsTable from './TransactionsTable';
import '../styles.css';
import { FaArrowUp, FaArrowDown } from 'react-icons/fa';

function MyWallet({ onNavigate }) {
  return (
    <div className="my-wallet-container">
      <div className="wallet-header">
        <h1>My Wallet</h1>
        <div className="balance-card">
          <h2>Balance: $15,595.01</h2>
          <button className="wallet-action-button">
            <FaArrowUp /> Send
          </button>
          <button className="wallet-action-button">
            <FaArrowDown /> Deposit
          </button>
        </div>
      </div>

      <div className="wallet-transactions-section">
        <h2>Recent Transactions</h2>
        <TransactionsTable />
      </div>

      <button onClick={() => onNavigate('dashboard')} className="back-to-dashboard-button">Back to Dashboard</button>
    </div>
  );
}

export default MyWallet;
