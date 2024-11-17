import React from 'react';
import TransactionsTable from './TransactionsTable';
import '../styles.css';
import { FaArrowUp, FaArrowDown, FaTimes } from 'react-icons/fa';

function MyWallet({ onNavigate }) {
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
            <button className="wallet-action-button">
              <FaArrowUp /> Send
            </button>
            <button className="wallet-action-button">
              <FaArrowDown /> Deposit
            </button>
          </div>
        </div>
      </div>

      <div className="wallet-transactions-section">
        <h2>Recent Transactions</h2>
        <TransactionsTable />
      </div>
    </div>
  );
}

export default MyWallet;
