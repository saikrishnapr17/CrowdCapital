// TransactionsTable.js
import React from 'react';

function TransactionsTable({ transactions }) {
  if (!transactions || transactions.length === 0) {
    return <div>No transactions found</div>;
  }

  return (
    <div className="transactions-table">
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Date</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction, index) => (
            <tr key={index}>
              <td>{transaction.type}</td>
              <td>{transaction.date}</td>
              <td>{transaction.amount}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionsTable;
