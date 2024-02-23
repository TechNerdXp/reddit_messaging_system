import React, { useState } from 'react';
import { WithContext as ReactTags } from 'react-tag-input';
import { Switch } from '@headlessui/react';


function RedditPosts({ posts, setPosts }) {
    const [subreddit, setSubreddit] = useState('Python');  // initial value
    const [limit, setLimit] = useState(10);  // initial value
    const [postType, setPostType] = useState('hot');  // initial value
    const [keywords, setKeywords] = useState([]);  // initial value
    const [exactMatch, setExactMatch] = useState(false);  // initial value

    const handleSubmit = () => {
        fetch(`http://localhost:5000/reddit?subreddit=${subreddit}&limit=${limit}&postType=${postType}&keywords=${keywords.map(keyword => keyword.text).join(',')}&exactMatch=${exactMatch}`)
            .then(response => response.json())
            .then(data => setPosts(data));
    };

    const handleSubredditChange = (event) => {
        setSubreddit(event.target.value);
    };

    const handleLimitChange = (event) => {
        setLimit(event.target.value);
    };

    const handlePostTypeChange = (event) => {
        setPostType(event.target.value);
    };

    const handleAddKeyword = (keyword) => {
        setKeywords([...keywords, keyword]);
    };

    const handleDeleteKeyword = (i) => {
        setKeywords(keywords.filter((keyword, index) => index !== i));
    };

    const handleExactMatchChange = (value) => {
        setExactMatch(value);
    };

    return (
        <div className="p-4 mx-auto bg-white rounded-xl shadow-md overflow-hidden m-3 w-full">
            <div className="flex justify-between items-end">
                <label>
                    Subreddit:&nbsp;
                    <input
                        type="text"
                        value={subreddit}
                        onChange={handleSubredditChange}
                        className="border-2 border-gray-300 p-1 rounded-md"
                        title="Enter the subreddit"
                    />
                </label>
                <label>
                    &nbsp;Limit:&nbsp;
                    <input
                        type="number"
                        value={limit}
                        onChange={handleLimitChange}
                        className="border-2 border-gray-300 p-1 rounded-md ml-2"
                        title="Enter the limit"
                    />
                </label>
                <label>
                    &nbsp;Post Type:&nbsp;
                    <select
                        value={postType}
                        onChange={handlePostTypeChange}
                        className="border-2 border-gray-300 p-1 rounded-md ml-2"
                        title="Select the post type"
                    >
                        <option value="hot">Hot</option>
                        <option value="new">New</option>
                        <option value="controversial">Controversial</option>
                        <option value="rising">Rising</option>
                        <option value="top">Top</option>
                    </select>
                </label>

            </div>
            <div className="flex justify-between items-end">
                <div className="py-6 h-22 w-1/2 text-wrap">
                    <ReactTags
                        tags={keywords}
                        handleDelete={handleDeleteKeyword}
                        handleAddition={handleAddKeyword}
                        placeholder="Add new keyword"
                        inputFieldPosition="top"
                        allowDragDrop={false}
                        delimiters={[188, 13]}
                    />
                </div>
                <Switch.Group as="div" className="flex items-center space-x-4 pb-6" title="Exact or Fuzzy search">
                    <Switch
                        checked={exactMatch}
                        onChange={handleExactMatchChange}
                        className={`${exactMatch ? 'bg-blue-600' : 'bg-gray-200'
                            } relative inline-flex items-center h-6 rounded-full w-11`}
                    >
                        <span className="sr-only">Exact Match Keywords</span>
                        <span
                            className={`${exactMatch ? 'translate-x-6' : 'translate-x-1'
                                } inline-block w-4 h-4 transform bg-white rounded-full`}
                        />
                    </Switch>
                    <Switch.Label>Exact Match Keywords</Switch.Label>
                </Switch.Group>
                <div>
                    <button onClick={handleSubmit} className="p-1 px-2 bg-blue-600 text-white rounded-md mb-6">Submit</button>
                </div>

            </div>
        </div>
    );
}

export default RedditPosts;
