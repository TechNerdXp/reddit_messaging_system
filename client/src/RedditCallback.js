import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function RedditCallback() {
    const [code, setCode] = useState(null);
    const navigate = useNavigate();
 
    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        setCode(code);
    }, []);

    useEffect(() => {
        if (code) {
            // Send the `code` to your backend
            fetch('/api/reddit/authenticate', {
                credentials: 'include',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code }),
            }).finally(() => {
                navigate('/reddit_auth');
            });
        }
    }, [code]);

    return (
        <div className="flex w-[100vw] h-[100vh]">
            <p className="m-auto">Authenticating...</p>
        </div>
    );
}

export default RedditCallback;
