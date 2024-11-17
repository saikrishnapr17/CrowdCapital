// Investments.js
import React, { useState, useEffect } from 'react';
import '../styles.css';
import { Chart } from 'chart.js/auto';
import { FaPlus } from 'react-icons/fa';

function Investments({ onNavigate }) {
  const [businesses, setBusinesses] = useState([]);
  const [selectedBusiness, setSelectedBusiness] = useState(null);

  useEffect(() => {
    // Fetch business list from API
    const fetchBusinesses = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/business/list');
        if (response.ok) {
          const data = await response.json();
          setBusinesses(data);
        } else {
          console.error('Failed to fetch business list');
        }
      } catch (error) {
        console.error('Error fetching business list:', error);
      }
    };

    fetchBusinesses();
  }, []);

  const handleBusinessClick = (business) => {
    setSelectedBusiness(business);
  };

  const handleBackClick = () => {
    setSelectedBusiness(null);
  };

  return (
    <div>
      {/* Business List Section */}
      {selectedBusiness === null && (
        <div className="investments-page">
          <div className="investments-header">
            <h2>Community Businesses</h2>
            <button
              className="business-button"
              onClick={() => onNavigate('enlist-business')}
              style={{ display: 'inline-flex', alignItems: 'center', marginBottom: '20px' }}
            >
              <FaPlus style={{ marginRight: '8px' }} /> Enlist Your Business
            </button>
          </div>
          <div className="business-list">
            {businesses.map((business, index) => (
              <button
                key={index}
                className="business-button"
                onClick={() => handleBusinessClick(business)}
              >
                {business.name}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Business Details Section */}
      {selectedBusiness !== null && (
        <div className="business-details-page">
          <div className="navbar">
            <button className="close-button" onClick={handleBackClick}>X</button>
          </div>
          <div className="details-content">
            <h2>Business Name</h2>
            <p className="subheading">{selectedBusiness.name}</p>

            <h2>Owner Name</h2>
            <p className="subheading">{selectedBusiness.owner || 'Placeholder for Owner\'s Name'}</p>

            <h2>Description</h2>
            <p className="subheading">{selectedBusiness.description || 'Placeholder for Business Description'}</p>

            <h2>Goal/Equity Offered</h2>
            <div id="chart-container">
              {/* Placeholder for Pie Chart */}
              <canvas id="equityChart"></canvas>
            </div>

            <button className="invest-button">Invest</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Investments;
