import React, { useState } from 'react';
import FetchPosts from './FetchPosts';
import DisplayPosts from './DisplayPosts';

function Home() {
    const [posts, setPosts] = useState([]);

    return (
        <div className="space-x-4 max-w-[55vw] flex items-center mx-auto">
            <div>
                <h1 className="text-xl font-semibold text-black">Welcome to Our App</h1>
                <p className="text-gray-500">This is the main page of our app. Here, you can input your keywords and select the subreddits you want to search in.</p>

                <FetchPosts className="bg-white rounded-xl shadow-md" setPosts={setPosts} />
                <DisplayPosts className="bg-white rounded-xl shadow-md" posts={posts} />
            </div>
        </div>

    );
}

export default Home;
