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
    }, [isAuthenticated]);
    
    const revokeAuth = () => {
        if (window.confirm("Are you sure you want to revoke reddit authentication?")) {
            fetch('/api/reddit/revoke-auth', {credentials: 'include'})
                .then(response => response.json())
                .then(data => setIsAuthenticated(false));
        }
    };

    return (
        <div className="flex w-[100vw] h-[100vh]">
            {isAuthenticated ? (
                <p className="m-auto font-bold text-cyan cursor-default">Authenticated as {username}<span className="text-gray-500"> | </span><span className="text-blue-900 hover:text-blue-800 cursor-pointer" onClick={revokeAuth}>Revoke Auth</span></p>
            ) : authUrl ? (
                <a className="p-6 button m-auto" href={authUrl}>Authorize with Reddit</a>
            ) : (
                <p className="m-auto font-bold text-cyan">Loading...</p>
            )}
        </div>
    );
}

export default RedditAuth;
