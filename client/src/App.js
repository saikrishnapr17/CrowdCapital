// App.js
import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import DashboardCard from './components/DashboardCard';
import AnalyticsChart from './components/AnalyticsChart';
import TransactionsTable from './components/TransactionsTable';
import './styles.css';

function App() {
  const [isSidebarVisible, setIsSidebarVisible] = useState(false); // Menu is closed initially

  const handleMenuClick = () => {
    setIsSidebarVisible(true);
  };

  const handleCloseSidebar = () => {
    setIsSidebarVisible(false);
  };

  return (
    <div className="app-container">
      <Sidebar isVisible={isSidebarVisible} onClose={handleCloseSidebar} />

      {/* Overlay */}
      {isSidebarVisible && <div className="overlay" onClick={handleCloseSidebar}></div>}

      <div className={`main-content ${isSidebarVisible ? 'shifted' : ''}`}>
        <Navbar onMenuClick={handleMenuClick} />
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
