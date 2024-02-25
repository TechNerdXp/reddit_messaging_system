import React, { useState, useEffect } from 'react';

function RedditAuth() {
    const [authUrl, setAuthUrl] = useState('');

    useEffect(() => {
        // Fetch the authorization URL from your backend
        fetch('http://localhost:5000/api/reddit/auth-url')
            .then(response => response.json())
            .then(data => setAuthUrl(data.authUrl));
    }, []);

    return (
        <div className="flex w-[100vh] h-[100vh]">
            {authUrl ? (

                <a className="p-6 button m-auto" href={authUrl}>Authorize with Reddit</a>
            ) : (
                <p className="m-auto">Loading...</p>
            )}
        </div>
    );
}

export default RedditAuth;
