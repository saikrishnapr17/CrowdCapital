import React, { useState, useEffect, useRef } from 'react';
import '../styles.css';
import { Chart } from 'chart.js/auto';
import { FaPlus } from 'react-icons/fa';

function Investments({ onNavigate, userId }) {
  const [businesses, setBusinesses] = useState([]);
  const [selectedBusiness, setSelectedBusiness] = useState(null);
  const [investingBusiness, setInvestingBusiness] = useState(null);
  const [investmentAmount, setInvestmentAmount] = useState('');
  const [userInvestment, setUserInvestment] = useState(0);
  const chartInstanceRef = useRef(null);

  useEffect(() => {
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

  useEffect(() => {
    if (selectedBusiness) {
      const ctx = document.getElementById('equityChart');

      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }

      if (ctx) {
        const remainingAmount = selectedBusiness.goal - selectedBusiness.equity - userInvestment;
        
        chartInstanceRef.current = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: ['Total Equity', 'Your Investment', 'Remaining Goal'],
            datasets: [{
              data: [
                selectedBusiness.equity - userInvestment, // Other investors' equity
                userInvestment, // User's investment
                remainingAmount // Remaining goal
              ],
              backgroundColor: ['#6359E9', '#FF4444', '#1d1d41'],
              borderWidth: 0,
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: true,
                position: 'bottom',
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    let label = context.label || '';
                    if (label) {
                      label += ': ';
                    }
                    label += '$' + context.raw.toFixed(2);
                    return label;
                  }
                }
              }
            }
          }
        });
      }
    }
  }, [selectedBusiness, userInvestment]);

  const handleBusinessClick = (business) => {
    setSelectedBusiness(business);
    setUserInvestment(0); // Reset user investment when selecting new business
  };

  const handleBackClick = () => {
    setSelectedBusiness(null);
    setUserInvestment(0);
  };

  const handleInvestClick = (business) => {
    setInvestingBusiness(business);
  };

  const handleCancelInvest = () => {
    setInvestingBusiness(null);
    setInvestmentAmount('');
  };

  const handleConfirmInvest = async () => {
    if (!investmentAmount) {
      alert('Please enter an amount to invest.');
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:5000/business/${investingBusiness.business_id}/invest`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          amount_invested: Number(investmentAmount),
        }),
      });

      if (response.ok) {
        const data = await response.json();
        // Update the selected business with new values
        setSelectedBusiness(prevBusiness => ({
          ...prevBusiness,
          equity: data.result.business.total_equity,
          goal: data.result.business.total_equity + data.result.business.remaining_amount
        }));
        // Set the user's investment amount
        setUserInvestment(Number(investmentAmount));
        // Update businesses list
        setBusinesses(prevBusinesses => 
          prevBusinesses.map(business => 
            business.business_id === investingBusiness.business_id 
              ? {
                  ...business,
                  equity: data.result.business.total_equity,
                  goal: data.result.business.total_equity + data.result.business.remaining_amount
                }
              : business
          )
        );
        alert(data.message);
        setInvestingBusiness(null);
        setInvestmentAmount('');
      } else {
        const errorData = await response.json();
        alert(errorData.error);
      }
    } catch (error) {
      console.error('Error making investment:', error);
      alert('An error occurred. Please try again.');
    }
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
            {businesses.map((business) => (
              <button
                key={business.business_id}
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
            <p className="subheading">{selectedBusiness.owner_name || "Placeholder for Owner's Name"}</p>

            <h2>Description</h2>
            <p className="subheading">{selectedBusiness.description || 'Placeholder for Business Description'}</p>

            <h2>Goal/Equity Offered</h2>
            <div id="chart-container">
              <canvas id="equityChart"></canvas>
            </div>
            
            {userInvestment > 0 && (
              <p className="investment-info">Your Investment: ${userInvestment.toFixed(2)}</p>
            )}

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
                value={investmentAmount}
                onChange={(e) => setInvestmentAmount(e.target.value)}
              />
            </label>
            <div className="investment-actions">
              <button className="light-rounded-button" onClick={handleConfirmInvest}>Purchase</button>
              <button className="light-rounded-button cancel" onClick={handleCancelInvest}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Investments;