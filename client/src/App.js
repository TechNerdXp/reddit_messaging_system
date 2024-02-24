import React from 'react';
import { HashRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';

// Import your page components
import Home from './Home';
import About from './About';

function App() {
  return (
    <Router>
      <div className="bg-gray-100 min-h-[100vh]">
        <nav className="px-4">
          <ul className="flex space-x-4 p-4">
            <li>
              <Link to="/" className="text-blue-500 hover:text-blue-800">Home</Link>
            </li>
            <li>
              <Link to="/about" className="text-blue-500 hover:text-blue-800">About</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
