import React, { useState, useEffect } from 'react';

const UserSubreddits = () => {
    const [admins, setAdmins] = useState([]);
    const [subreddits, setSubreddits] = useState({});
    const [editedKeywords, setEditedKeywords] = useState({});

    useEffect(() => {
        fetch('/api/get-admins')
            .then(response => response.json())
            .then(data => {
                setAdmins(data);
                data.forEach(admin => {
                    fetch(`/api/user-subreddits/${admin}`)
                        .then(response => response.json())
                        .then(data => {
                            setSubreddits(prevState => ({ ...prevState, [admin]: data }));
                        });
                });
            });
    }, []);
    

    const handleAddSubreddit = (admin) => {
        const newSubreddit = { username: admin, subreddit: '', keywords: '' };
        fetch('/api/user-subreddits', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newSubreddit)
        })
        .then(response => response.json())
        .then(data => {
            console.log(admin);
            console.log(data);
            if (data.status === 'success') {
                setSubreddits(prevState => ({ ...prevState, [admin]: [...prevState[admin], newSubreddit] }));
            }
        });
    };
    
    const handleDeleteSubreddit = (admin, subreddit) => {
        fetch('/api/user-subreddits', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: admin, subreddit })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                setSubreddits(prevState => {
                    const updatedSubreddits = prevState[admin].filter(s => s.subreddit !== subreddit);
                    return { ...prevState, [admin]: updatedSubreddits };
                });
            }
        });
    };
    
    const handleUpdateSubreddit = (admin, subreddit, keywords) => {
        fetch('/api/user-subreddits', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: admin, subreddit, keywords })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                setSubreddits(prevState => {
                    const updatedSubreddits = prevState[admin].map(s => s.subreddit === subreddit ? { ...s, keywords } : s);
                    return { ...prevState, [admin]: updatedSubreddits };
                });
            }
        });
    };
    
    return (
        <div className="p-4">
            {admins.map(admin => (
                <div key={admin} className="mb-4">
                    <h2 className="text-xl font-bold mb-2">{admin}</h2>
                    {subreddits[admin] !== undefined ? (
                        subreddits[admin].map((subreddit, index) => {
                            // Initialize editedKeywords for each subreddit
                            setEditedKeywords(prevState => ({
                                ...prevState,
                                [`${admin}_${subreddit.name}`]: subreddit.keywords ? subreddit.keywords.join(',') : ''
                            }));

                            const editedKey = `${admin}_${subreddit.name}`;

                            return (
                                <div key={index} className="mb-2">
                                    <input type="text" value={subreddit.name} className="border p-2 mr-2" />
                                    <textarea
                                        value={editedKeywords[editedKey]}
                                        onChange={(e) => setEditedKeywords(prevState => ({ ...prevState, [editedKey]: e.target.value }))}
                                        className="border p-2"
                                    />
                                    <button onClick={() => handleUpdateSubreddit(admin, subreddit.name, editedKeywords[editedKey])} className="mt-2 p-2 bg-blue-500 text-white">Update Subreddit</button>
                                    <button onClick={() => handleDeleteSubreddit(admin, subreddit.name)} className="mt-2 p-2 bg-red-500 text-white">Delete Subreddit</button>
                                </div>
                            );
                        })
                    ) : (
                        <button onClick={() => handleAddSubreddit(admin)} className="mt-2 p-2 bg-green-500 text-white">Add Subreddit</button>
                    )}
                </div>
            ))}
        </div>
    );
    
    
};

export default UserSubreddits;
