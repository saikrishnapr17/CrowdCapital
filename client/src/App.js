// App.js
import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import DashboardCard from './components/DashboardCard';
import AnalyticsChart from './components/AnalyticsChart';
import TransactionsTable from './components/TransactionsTable';
import MyWallet from './components/MyWallet';
import SMSFraudCheck from './components/SMSFraudCheck';
import Investments from './components/Investments';
import Community from './components/Community';
import Contribute from './components/Contribute';
import RequestLoan from './components/RequestLoan';
import EnlistBusiness from './components/EnlistBusiness'; // Import the EnlistBusiness component
import './styles.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activePage, setActivePage] = useState('my-wallet');

  const toggleSidebar = () => {
    setSidebarOpen(prevState => !prevState);
  };

  const handlePageChange = (page) => {
    setActivePage(page);
    setSidebarOpen(false);
  };

  return (
    <div className="app-container">
      <Sidebar isOpen={sidebarOpen} onNavigate={handlePageChange} />
      {sidebarOpen && <div className="overlay" onClick={toggleSidebar}></div>}
      <div className="main-content">
        <Navbar toggleSidebar={toggleSidebar} />
        {activePage === 'dashboard' && (
          <>
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
          </>
        )}
        {activePage === 'my-wallet' && <MyWallet onNavigate={handlePageChange} />}
        {activePage === 'sms-fraud-check' && <SMSFraudCheck onNavigate={handlePageChange} />}
        {activePage === 'investments' && <Investments onNavigate={handlePageChange} />}
        {activePage === 'community' && <Community onNavigate={handlePageChange} />}
        {activePage === 'contribute' && <Contribute onNavigate={handlePageChange} />}
        {activePage === 'request-loan' && <RequestLoan onNavigate={handlePageChange} />}
        {activePage === 'enlist-business' && <EnlistBusiness onNavigate={handlePageChange} />} {/* Add EnlistBusiness page */}
      </div>
    </div>
  );
}

export default App;
