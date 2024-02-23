import React from 'react';

function DisplayPosts({ posts }) {
    return (
        <div>
            {posts.map((post, index) => (
                <div key={index} className="mx-auto bg-white rounded-xl shadow-md overflow-hidden m-3 mb-6 w-full">
                    <div className="md:flex">
                        <div className="p-4">
                            <h2 className="text-lg font-bold text-gray-900">{post.title}</h2>
                            <p className="mt-2 text-gray-500 text-wrap">{post.text}</p>
                            {/* <div className="mt-2 text-gray-500" dangerouslySetInnerHTML={{ __html: post.html }}></div> */}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default DisplayPosts;
