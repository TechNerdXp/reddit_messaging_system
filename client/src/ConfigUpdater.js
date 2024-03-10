import React, { useState, useEffect } from 'react';

function ConfigUpdater() {
    const [configs, setConfigs] = useState({});

    useEffect(() => {
        fetch('/api/configs')
            .then(response => response.json())
            .then(data => setConfigs(data));
    }, []);

    const handleValueChange = (key, event) => {
        setConfigs({
            ...configs,
            [key]: event.target.value,
        });
    };

    const handleSubmit = (key) => {
        fetch(`/api/configs/${key}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                value: configs[key],
            }),
        });
    };

    return (
        <div>
            {Object.entries(configs).map(([key, value]) => (
                <div key={key}>
                    <label>{key}</label>
                    <input type="text" value={value} onChange={(event) => handleValueChange(key, event)} />
                    <button onClick={() => handleSubmit(key)}>Update</button>
                </div>
            ))}
        </div>
    );
}

export default ConfigUpdater;
