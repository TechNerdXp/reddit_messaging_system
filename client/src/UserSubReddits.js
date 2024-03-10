import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';

const UserSubreddits = () => {
    const { register, handleSubmit, reset } = useForm();
    const [userSubreddits, setUserSubreddits] = useState([]);

    useEffect(() => {
        // Load user subreddits on component mount
        fetch('/api/user-subreddits')
            .then(response => response.json())
            .then(data => setUserSubreddits(data))
            .catch(error => console.error(error));
    }, []);

    const onSubmit = data => {
        // Add new subreddit
        fetch('/api/user-subreddits', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(responseData => {
                if (responseData.status === 'success') {
                    // Update local state and clear form
                    setUserSubreddits([...userSubreddits, data]);
                    reset();
                }
            })
            .catch(error => console.error(error));
    };

    const deleteUserSubreddit = (username, subreddit) => {
        // Delete subreddit
        fetch('/api/user-subreddits', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, subreddit }),
        })
            .then(response => response.json())
            .then(responseData => {
                if (responseData.status === 'success') {
                    // Update local state
                    setUserSubreddits(userSubreddits.filter(us => us.username !== username || us.subreddit !== subreddit));
                }
            })
            .catch(error => console.error(error));
    };

    return (
        <div>
            <form onSubmit={handleSubmit(onSubmit)}>
                <input {...register('username')} placeholder="Username" required />
                <input {...register('subreddit')} placeholder="Subreddit" required />
                <input {...register('keywords')} placeholder="Keywords" required />
                <button type="submit">Add Subreddit</button>
            </form>

            {userSubreddits.map((us, index) => (
                <div key={index}>
                    <h2>{us.username}</h2>
                    <p>{us.subreddit}</p>
                    <p>{us.keywords}</p>
                    <button onClick={() => deleteUserSubreddit(us.username, us.subreddit)}>Delete</button>
                </div>
            ))}
        </div>
    );
};

export default UserSubreddits;
