import React, { useState, useEffect } from 'react';

const AdminSubReddits = () => {
    const [data, setData] = useState([]);
    const [username, setUsername] = useState('');
    const [subreddits, setSubreddits] = useState('');
    const [keywords, setKeywords] = useState('');
    const [id, setId] = useState(null);

    useEffect(() => {
        fetch('/api/admins-and-subreddits')
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => console.error(error));
    }, []);

    const createAdminAndSubreddit = () => {
        fetch('/api/admins-and-subreddits', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, subreddits, keywords }),
        })
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error(error));
    };

    const updateAdminAndSubreddit = () => {
        fetch(`/api/admins-and-subreddits/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, subreddits, keywords }),
        })
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error(error));
    };

    const deleteAdminAndSubreddit = (id) => {
        if (!window.confirm('Are you sure you want to delete this admin and subreddits?')) {
            return;
        }
        fetch(`/api/admins-and-subreddits/${id}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => console.log(data.message))
        .catch(error => console.error(error));
    };

    return (
        <div className="p-4 bg-gray-100">
            {/* Display the data */}
            {data.map((item, index) => (
                <div key={index} className="p-4 m-2 bg-white rounded shadow">
                    <h3 className="text-xl font-bold">{item.username}</h3>
                    <p className="text-gray-600">{item.subreddits}</p>
                    <p className="text-gray-600">{item.keywords}</p>
                    <button className="px-4 py-2 mr-2 text-white bg-blue-500 rounded hover:bg-blue-700" onClick={() => {setUsername(item.username); setSubreddits(item.subreddits); setKeywords(item.keywords); setId(item.id);}}>Edit</button>
                    <button className="px-4 py-2 text-white bg-red-500 rounded hover:bg-red-700" onClick={() => deleteAdminAndSubreddit(item.id)}>Delete</button>
                </div>
            ))}
            {/* Add form for creating and updating admins and subreddits */}
            <form className="p-4 m-2 bg-white rounded shadow">
                <input className="w-full p-2 mb-2 border rounded" type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" />
                <textarea className="w-full p-2 mb-2 border rounded" value={subreddits} onChange={e => setSubreddits(e.target.value)} placeholder="Subreddits" />
                <textarea className="w-full p-2 mb-2 border rounded" value={keywords} onChange={e => setKeywords(e.target.value)} placeholder="Keywords" />
                <button className="px-4 py-2 mr-2 text-white bg-green-500 rounded hover:bg-green-700" type="button" onClick={createAdminAndSubreddit}>Create</button>
                <button className="px-4 py-2 text-white bg-yellow-500 rounded hover:bg-yellow-700" type="button" onClick={updateAdminAndSubreddit}>Update</button>
            </form>
        </div>
    );
    
};

export default AdminSubReddits;
