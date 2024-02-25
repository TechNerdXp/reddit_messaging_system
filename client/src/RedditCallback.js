import React, { useEffect, useState } from 'react';

function RedditCallback() {
    const [code, setCode] = useState(null);

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        setCode(code);
    }, []);

    useEffect(() => {
        if (code) {
            // Send the `code` to your backend
            fetch('http://localhost:5000/api/reddit/authenticate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code }),
            });
        }
    }, [code]);

    return <p>Authenticating...</p>;
}

export default RedditCallback;
