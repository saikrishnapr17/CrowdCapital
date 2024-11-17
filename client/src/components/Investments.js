// components/Investments.js
import React, { useState } from 'react';
import '../styles.css';
import { Chart } from 'chart.js/auto';

function Investments() {
  const businesses = [
    "Business Name 1",
    "Business Name 2",
    "Business Name 3",
    "Business Name 4",
    "Business Name 5",
    "Business Name 6",
    "Business Name 7",
  ];

  const [selectedBusiness, setSelectedBusiness] = useState(null);

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
          </div>
          <div className="business-list">
            {businesses.map((business, index) => (
              <button
                key={index}
                className="business-button"
                onClick={() => handleBusinessClick(business)}
              >
                {business}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Business Details Section */}
      {selectedBusiness !== null && (
        <div className="business-details-page">
          <div className="navbar">
            <button className="hamburger-menu" onClick={() => alert('Toggle Sidebar')}>&#9776;</button>
            <button className="close-button" onClick={handleBackClick}>X</button>
          </div>
          <div className="details-content">
            <h2>Business Name</h2>
            <p className="subheading">{selectedBusiness}</p>

            <h2>Owner Name</h2>
            <p className="subheading">Placeholder for Owner's Name</p>

            <h2>Description</h2>
            <p className="subheading">Placeholder for Business Description</p>

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

// Script to render the Pie Chart when the business details are opened.
document.addEventListener('DOMContentLoaded', function () {
  const ctx = document.getElementById('equityChart');
  if (ctx) {
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ['Equity Offered', 'Remaining Goal'],
        datasets: [{
          data: [40, 60], // Placeholder data for pie chart
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
});
