import React, { useState, useEffect } from 'react';
import { ArrowTopRightOnSquareIcon } from '@heroicons/react/24/solid'


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
        <div className="p-6 mx-auto bg-white rounded-xl shadow-md flex items-center space-x-4">
            <table className="table-auto w-full">
                <thead>
                    <tr>
                        <th className="px-4 py-2">#</th>
                        <th className="px-4 py-2">Title</th>
                        <th className="px-4 py-2">Author</th>
                        <th className="px-4 py-2">Subreddit</th>
                        <th className="px-4 py-2">Admin</th>
                        <th className="px-4 py-2">Content</th>
                        <th className="px-4 py-2">Chats on Assistant</th>
                        <th className="px-4 py-2">Chats on Reddit</th>
                        <th className="px-4 py-2">Link to the post</th>
                        <th className="px-4 py-2">Message Status</th>
                    </tr>
                </thead>
                <tbody>
                    {posts.map((post, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'bg-gray-200' : ''}>

                            <td className="border px-4 py-2">{index + 1}</td>
                            <td className="border px-4 py-2">{post.title}</td>
                            <td className="border px-4 py-2 text-blue-500">u/{post.author}</td>
                            <td className="border px-4 py-2 text-blue-500">r/{post.subreddit}</td>
                            <td className="border px-4 py-2 text-blue-500">u/{post.admin}</td>
                            <td className="border px-4 py-2">{truncate(post.text, 100)}</td>
                            <td className="border px-4 py-2">
                                <a href={`https://platform.openai.com/threads/${post.openai_thread_id}`} target="_blank">
                                    <ArrowTopRightOnSquareIcon className="h-6 w-6 text-gray-500" />
                                </a>
                            </td>
                            <td className="border px-4 py-2">
                                <a href={`https://www.reddit.com/message/messages/${post.reddit_message_id}`} target="_blank">
                                    <ArrowTopRightOnSquareIcon className="h-6 w-6 text-gray-500" />
                                </a>
                            </td>
                            <td className="border px-4 py-2">
                                <a href={`${post.post_url}`} target="_blank">
                                    <ArrowTopRightOnSquareIcon className="h-6 w-6 text-gray-500" />
                                </a>
                            </td>
                            <td className="border px-4 py-2">{post.message_status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default PostsTable;
