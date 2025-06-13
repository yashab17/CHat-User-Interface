import React from 'react';

const Sidebar = () => {
    return (
        <div className="sidebar">
            <h1 className="brand">ChatApp</h1>
            <button className="new-chat-button">New Chat</button>
            <input type="text" className="search-box" placeholder="Search..." />
            <a href="/login" className="login-link">Login</a>
        </div>
    );
};

export default Sidebar;