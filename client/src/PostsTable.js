import React, { useState, useEffect } from 'react';

const PostsTable = () => {
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        fetch('/api/db/posts', {credentials: 'include'})
            .then(response => response.json())
            .then(data => setPosts(data));
        
        console.log(posts)
    }, []);

    const truncate = (str, n) => (str.length > n) ? str.substr(0, n - 1) + '...' : str;
    return (
        <div className="p-6 max-w-[80vw] mx-auto bg-white rounded-xl shadow-md flex items-center space-x-4">
            <table className="table-auto w-full">
                <thead>
                    <tr>
                        <th className="px-4 py-2">#</th>
                        <th className="px-4 py-2">Title</th>
                        <th className="px-4 py-2">Author</th>
                        <th className="px-4 py-2">Content</th>
                        <th className="px-4 py-2">Chats</th>
                    </tr>
                </thead>
                <tbody>
                    {posts.map((post, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'bg-gray-200' : ''}>

                            <td className="border px-4 py-2">{index + 1}</td>
                            <td className="border px-4 py-2">{post.title}</td>
                            <td className="border px-4 py-2 text-blue-500">u/{post.author}</td>
                            <td className="border px-4 py-2">{truncate(post.text, 100)}</td>
                            <td className="border px-4 py-2">{post.id}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default PostsTable;
