import React, { useState, useEffect } from 'react';

function ConfigUpdater() {
    const [configs, setConfigs] = useState({});

    useEffect(() => {
        console.log('fetching configs'); // nothing is happening here. why useeffect is  not working
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
        <div className="flex items-center">
            <div className="w-[55vw] mx-auto">
                {Object.entries(configs).map(([key, value]) => (
                    <div className="flex flex-col" key={key}>
                        <label>{key}</label>
                        <input className="w-50 field" type="text" value={value} onChange={(event) => handleValueChange(key, event)} />
                        <button className="button" onClick={() => handleSubmit(key)}>Update</button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ConfigUpdater;
