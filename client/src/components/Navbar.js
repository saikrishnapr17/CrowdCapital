// components/Navbar.js
import React from 'react';

function Navbar({ toggleSidebar }) {
  return (
    <div className="navbar">
      <button className="hamburger-menu" onClick={toggleSidebar}>
        &#9776;
      </button>
      {/* Add any additional navbar content here */}
    </div>
  );
}


export default Navbar;