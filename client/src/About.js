import React from 'react';

function About() {
    return (
        <div className="p-6 max-w-[55vw] mx-auto bg-white rounded-xl shadow-md flex items-center space-x-4">
            <div>
                <h1 className="text-xl font-semibold text-black">About Our App</h1>
                <p className="text-gray-500">Welcome to our Reddit Keyword Search App! This application is designed to help you explore the vast world of Reddit in a more targeted and efficient way.</p>
                <p className="text-gray-500">Our app uses the Reddit API to search for specific keywords within various subreddits. This allows users to find relevant discussions, posts, and comments that are most pertinent to their interests or business.</p>
                <p className="text-gray-500">If you have any questions or need support, please don't hesitate to reach out to us at <a href="mailto:technerdxp@gmail.com" className="text-blue-500 hover:text-blue-800">technerdxp@gmail.com</a>. We're here to help!</p>
                <p className="text-gray-500">Thank you for choosing our Reddit Keyword Search App!</p>
            </div>
        </div>
    );
}

export default About;
