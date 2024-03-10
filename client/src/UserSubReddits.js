import React, { useState } from 'react';
import { Switch } from '@headlessui/react';
import TagsInput from 'react-tagsinput';
import 'react-tagsinput/react-tagsinput.css';

function UserSubreddits({ users, setUsers }) {
    const [user, setUser] = useState('');  // initial value
    const [subreddit, setSubreddit] = useState('');  // initial value
    const [keywords, setKeywords] = useState([]);  // initial value
    const [userActive, setUserActive] = useState(false);  // initial value
    const [subredditActive, setSubredditActive] = useState(false);  // initial value

    const handleUserChange = (event) => {
        setUser(event.target.value);
    };

    const handleSubredditChange = (event) => {
        setSubreddit(event.target.value);
    };

    const handleKeywordsChange = (keywords) => {
        setKeywords(keywords);
    };

    const handleUserActiveChange = (value) => {
        setUserActive(value);
    };

    const handleSubredditActiveChange = (value) => {
        setSubredditActive(value);
    };

    const handleSubmit = () => {
        // Add your own logic to update the users state
    };

    return (
        <div className="p-6 mx-auto rounded-xl shadow-md m-3 w-full bg-gradient-to-r from-indigo-100 via-purple-100 to-blue-100">
            <div className="flex justify-between">
                <label className="w-1/3">
                    <span className="label-text">User: </span>
                    <input
                        type="text"
                        value={user}
                        onChange={handleUserChange}
                        className="w-full field"
                        title="Enter the user"
                    />
                </label>
                <Switch
                    checked={userActive}
                    onChange={handleUserActiveChange}
                    className="switch"
                >
                    {userActive ? 'Active' : 'Inactive'}
                </Switch>
            </div>
            <div className="flex justify-between">
                <label className="w-1/3">
                    <span className="label-text">Subreddit: </span>
                    <input
                        type="text"
                        value={subreddit}
                        onChange={handleSubredditChange}
                        className="w-full field"
                        title="Enter the subreddit"
                    />
                </label>
                <Switch
                    checked={subredditActive}
                    onChange={handleSubredditActiveChange}
                    className="switch"
                >
                    {subredditActive ? 'Active' : 'Inactive'}
                </Switch>
            </div>
            <div className="pt-6 h-22 w-3/4 mr-2 text-wrap">
                <TagsInput 
                    value={keywords}
                    onChange={handleKeywordsChange}
                    addOnBlur={true}
                    addOnPaste={true}
                    onlyUnique={true}
                    addKeys={[188, 9, 13]}
                    className="field"
                    tagProps={{className:'pill', classNameRemove: 'pill-remove'}}
                    inputProps={{className: 'w-full focus:outline-none', placeholder: 'Add a keyword'}}
                />
            </div>
            <button onClick={handleSubmit} className="btn">Submit</button>
        </div>
    );
}

export default UserSubreddits;
