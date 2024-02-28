import React, { useEffect, useState } from 'react';

const TestComponent = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/api/test', {
      method: 'GET',
      credentials: 'include', // include credentials in the request
    })
    .then(response => response.text()) // parse response as text
    .then(data => {
      setData(data); // set data in state
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }, []); // empty dependency array means this effect runs once on mount

  return (
    <div>
      <h1>Response from /api/test:</h1>
      {data && <pre>{data}</pre>}
    </div>
  );
};

export default TestComponent;
