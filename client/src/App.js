// App.js
import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import DashboardCard from './components/DashboardCard';
import AnalyticsChart from './components/AnalyticsChart';
import TransactionsTable from './components/TransactionsTable';
import './styles.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Toggle function to open/close sidebar
  const toggleSidebar = () => {
    setSidebarOpen(prevState => !prevState);
  };

  return (
    <div className="app-container">
      <Sidebar isOpen={sidebarOpen} />
      {sidebarOpen && <div className="overlay" onClick={toggleSidebar}></div>}
      <div className="main-content">
        <Navbar toggleSidebar={toggleSidebar} />
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
