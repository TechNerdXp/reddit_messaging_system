import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';

// Import your page components
import Home from './Home';
import About from './About';
import PostsTable from './PostsTable';
import RedditCallback from './RedditCallback';
import RedditAuth from './RedditAuth';
import TestComponent from './TestComponent';

function App() {
  return (
    <Router>
      <div className="min-h-[100vh] bg-gradient-to-r from-gray-200 to-gray-100">
        <nav className="px-4">
          <ul className="flex space-x-4 p-4 font-bold">
            <li>
              <Link to="/" className="text-blue-600 hover:text-blue-800">Home</Link>
            </li>
            <li>
              <Link to="/about" className="text-blue-600 hover:text-blue-800">About</Link>
            </li>
            <li>
              <Link to="/posts" className="text-blue-600 hover:text-blue-800">Posts</Link>
            </li>
            <li>
              <Link to="/reddit_auth" className="text-blue-600 hover:text-blue-800">Reddit Auth</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/posts" element={<PostsTable />} />
          <Route path="/reddit_callback" element={<RedditCallback />} />
          <Route path="/reddit_auth" element={<RedditAuth />} /> 
          <Route path="/test" element={<TestComponent />} /> 
        </Routes>
      </div>
    </Router>
  );
}

export default App;
