// components/TransactionsTable.js
import React from 'react';

function TransactionsTable() {
  return (
    <div className="transactions-table">
      <h2>Transaction</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Date</th>
            <th>Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Adobe After Effect</td>
            <td>Sat, 20 Apr 2020</td>
            <td>$80.09</td>
            <td>Deposited</td>
          </tr>
          <tr>
            <td>McDonald's</td>
            <td>Fri, 19 Apr 2020</td>
            <td>$7.03</td>
            <td>Deposited</td>
          </tr>
          <tr>
            <td>Levi's</td>
            <td>Tue, 19 Apr 2020</td>
            <td>$30.09</td>
            <td>Deposited</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default TransactionsTable;
