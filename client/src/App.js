// App.js
import React from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import DashboardCard from './components/DashboardCard';
import AnalyticsChart from './components/AnalyticsChart';
import TransactionsTable from './components/TransactionsTable';
import './styles.css';

function App() {
  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content">
        <Navbar />
        <div className="dashboard-cards">
          <DashboardCard title="Total Income" amount="$632,000" percentage={1.29} />
          <DashboardCard title="Total Outcome" amount="$632,000" percentage={-1.29} />
          <DashboardCard title="Card Balance" amount="$15,595.01" />
        </div>
        <div className="analytics-section">
          <AnalyticsChart />
        </div>
        <div className="transactions-section">
          <TransactionsTable />
        </div>
      </div>
    </div>
  );
}

export default App;
