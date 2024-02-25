import React, { useState, useEffect } from 'react';

function RedditAuth() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [authUrl, setAuthUrl] = useState('');

    useEffect(() => {
        // Fetch the authentication status from your backend
        fetch('http://localhost:5000/api/reddit/is-authenticated')
            .then(response => response.json())
            .then(data => {
                setIsAuthenticated(data.isAuthenticated);
    
                // Fetch the authorization URL from your backend
                if(!data.isAuthenticated) {
                    fetch('http://localhost:5000/api/reddit/auth-url')
                        .then(response => response.json())
                        .then(data => setAuthUrl(data.authUrl));
                }
            });
    }, []);
    

    return (
        <div className="flex w-[100vh] h-[100vh]">
            {isAuthenticated ? (
                <p className="m-auto font-bold text-cyan">Authenticated</p>
            ) : authUrl ? (
                <a className="p-6 button m-auto" href={authUrl}>Authorize with Reddit</a>
            ) : (
                <p className="m-auto font-bold text-cyan">Loading...</p>
            )}
        </div>
    );
}

export default RedditAuth;
