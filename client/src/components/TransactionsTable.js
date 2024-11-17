import React from 'react';
import '../styles.css';

const transactions = [
  { name: 'Adobe After Effect', date: 'Sat, 20 Apr 2020', amount: 80.09 },
  { name: 'McDonald\'s', date: 'Fri, 19 Apr 2020', amount: -7.03 },
  { name: 'Levi\'s', date: 'Tue, 19 Apr 2020', amount: 30.09 },
];

function TransactionsTable() {
  return (
    <div className="transactions-table">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Date</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction, index) => (
            <tr key={index}>
              <td>{transaction.name}</td>
              <td>{transaction.date}</td>
              <td style={{ color: transaction.amount > 0 ? 'green' : 'red' }}>
                {transaction.amount > 0 ? `+${transaction.amount}` : transaction.amount}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionsTable;