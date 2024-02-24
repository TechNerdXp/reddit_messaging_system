import React, { useState } from 'react';
import FetchPosts from './FetchPosts';
import DisplayPosts from './DisplayPosts';

function Home() {
    const [posts, setPosts] = useState([]);

    return (
        <div className="flex items-center">
            <div className="w-[55vw] mx-auto">
                <div className="text-white rounded-xl shadow-md p-6 bg-gradient-to-r from-green-500 to-cyan-600">
                    <h1 className="text-xl font-semibold">Welcome to Our App</h1>
                    <p className="text-gray-200 pt-3">This is the main page of our app. Here, you can input your keywords and select the subreddits you want to search in.</p>
                </div>
                <FetchPosts className="bg-white rounded-xl shadow-md" setPosts={setPosts} />
                <DisplayPosts className="bg-white rounded-xl shadow-md" posts={posts} />
            </div>
        </div>

    );
}

export default Home;
