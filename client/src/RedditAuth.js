import React, { useState, useEffect } from 'react';

function RedditAuth() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [authUrl, setAuthUrl] = useState('');
    const [username, setUsername] = useState(null);

    useEffect(() => {
        fetch('/api/reddit/is-authenticated', { credentials: 'include' })
            .then(response => response.json())
            .then(data => {
                setIsAuthenticated(data.isAuthenticated);
                setUsername(data.username);

                if (!data.isAuthenticated) {
                    fetch('/api/reddit/auth-url', { credentials: 'include' })
                        .then(response => response.json())
                        .then(data => setAuthUrl(data.authUrl));
                }
            });
    }, []);

    return (
        <div className="flex w-[100vw] h-[100vh]">
            {isAuthenticated ? (
                <p className="m-auto font-bold text-cyan">Authenticated as {username}</p>
            ) : authUrl ? (
                <a className="p-6 button m-auto" href={authUrl}>Authorize with Reddit</a>
            ) : (
                <p className="m-auto font-bold text-cyan">Loading...</p>
            )}
        </div>
    );
}

export default RedditAuth;
