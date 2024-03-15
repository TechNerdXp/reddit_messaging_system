import React, { useState, useEffect } from 'react';

const InfoLogs = () => {
    const [logs, setLogs] = useState('');

    useEffect(() => {
        fetch('/info_logs')
            .then(response => response.text())
            .then(data => setLogs(data))
            .catch(error => console.error('Error:', error));
    }, []);

    return (
        <div className="p-6 mx-auto bg-white rounded-xl shadow-md flex items-center space-x-4">
            <div>
                <div className="text-xl font-medium text-black">Log Information</div>
                <p className="text-gray-500">
                    <pre className="whitespace-pre-wrap">{logs}</pre>
                </p>
            </div>
        </div>
    );
};

export default InfoLogs;
