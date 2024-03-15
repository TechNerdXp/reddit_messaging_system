import React, { useState, useEffect } from 'react';

const Info = () => {
    const [logs, setLogs] = useState('');

    useEffect(() => {
        fetch('/logs')
            .then(response => response.text())
            .then(data => setLogs(data))
            .catch(error => console.error('Error:', error));
    }, []);

    return (
        <div>
            <h2>Log Information</h2>
            <pre>{logs}</pre>
        </div>
    );
};

export default Info;
