import React, { useState, useEffect, useRef } from 'react';
import '../styles.css';
import { Chart } from 'chart.js/auto';
import { FaPlus } from 'react-icons/fa';

function Investments({ onNavigate }) {
  const [businesses, setBusinesses] = useState([]);
  const [selectedBusiness, setSelectedBusiness] = useState(null);
  const [investingBusiness, setInvestingBusiness] = useState(null);
  const chartInstanceRef = useRef(null);

  useEffect(() => {
    // Fetch business list from API
    const fetchBusinesses = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/businesses/info');
        if (response.ok) {
          const data = await response.json();
          setBusinesses(data.businesses);
        } else {
          console.error('Failed to fetch business list');
        }
      } catch (error) {
        console.error('Error fetching business list:', error);
      }
    };

    fetchBusinesses();
  }, []);

  // Effect to render chart after selecting a business
  useEffect(() => {
    if (selectedBusiness) {
      const ctx = document.getElementById('equityChart');

      // Destroy existing chart instance if it exists
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }

      if (ctx) {
        // Create a new chart and store its instance
        chartInstanceRef.current = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: ['Equity Offered', 'Remaining Goal'],
            datasets: [{
              data: [selectedBusiness.equity, selectedBusiness.goal - selectedBusiness.equity],
              backgroundColor: ['#6359E9', '#1d1d41'],
              borderWidth: 0,
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: true,
                position: 'bottom',
              }
            }
          }
        });
      }
    }
  }, [selectedBusiness]);

  const handleBusinessClick = (business) => {
    setSelectedBusiness(business);
  };

  const handleBackClick = () => {
    setSelectedBusiness(null);
  };

  const handleInvestClick = (business) => {
    setInvestingBusiness(business);
  };

  const handleCancelInvest = () => {
    setInvestingBusiness(null);
  };

  return (
    <div>
      {/* Business List Section */}
      {selectedBusiness === null && investingBusiness === null && (
        <div className="investments-page">
          <div className="investments-header">
            <h2>Community Businesses</h2>
            <button className="light-rounded-button" onClick={() => onNavigate('enlist-business')}>
              <FaPlus /> Enlist Your Business
            </button>
          </div>
          <div className="business-list">
            {businesses.map((business, index) => (
              <button
                key={index}
                className="business-button"
                onClick={() => handleBusinessClick(business)}
              >
                {business.business_name}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Business Details Section */}
      {selectedBusiness !== null && investingBusiness === null && (
        <div className="business-details-page">
          <div className="navbar">
            <button className="close-button" onClick={handleBackClick}>X</button>
          </div>
          <div className="details-content">
            <h2>Business Name</h2>
            <p className="subheading">{selectedBusiness.business_name}</p>

            <h2>Owner Name</h2>
            <p className="subheading">{selectedBusiness.owner_name || 'Placeholder for Owner\'s Name'}</p>

            <h2>Description</h2>
            <p className="subheading">{selectedBusiness.description || 'Placeholder for Business Description'}</p>

            <h2>Goal/Equity Offered</h2>
            <div id="chart-container">
              {/* Placeholder for Pie Chart */}
              <canvas id="equityChart"></canvas>
            </div>

            <button className="invest-button" onClick={() => handleInvestClick(selectedBusiness)}>
              Invest
            </button>
          </div>
        </div>
      )}

      {/* Investment Form Section */}
      {investingBusiness !== null && (
        <div className="investment-form-page">
          <div className="investment-form-card">
            <h3>{investingBusiness.business_name}</h3>
            <label>
              <input
                type="number"
                placeholder="Amount to be Invested ($)"
              />
            </label>
            <label>
              <input
                type="number"
                placeholder="Percentage of Equity"
              />
            </label>
            <div className="investment-actions">
              <button className="light-rounded-button">Purchase</button>
              <button className="light-rounded-button cancel" onClick={handleCancelInvest}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Investments;
