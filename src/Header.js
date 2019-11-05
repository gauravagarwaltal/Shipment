import React from "react";
import { NavLink } from "react-router-dom";

function Header() {
    const activeStyle = { color: "grey" };
    return (
        <h2>
            <nav>
                <NavLink activeStyle={activeStyle} exact to="/">
                    Home
                </NavLink>
                {" | "}
                <NavLink activeStyle={activeStyle} to="/channeldetails">
                    Channel Details
                </NavLink>
                {" | "}
                <NavLink activeStyle={activeStyle} to="/confirmdeposit">
                    Channel Deposit
                </NavLink>
                {" | "}
                <NavLink activeStyle={activeStyle} to="/transaction">
                    New Transaction
                </NavLink>
                {" | "}
                <NavLink activeStyle={activeStyle} to="/pendingRequests">
                    Pending Requests
                </NavLink>
                {" | "}
                <NavLink activeStyle={activeStyle} to="/pendingResponses">
                    Pending Response
                </NavLink>
                {" | "}
                <NavLink activeStyle={activeStyle} to="/about">
                    About
                </NavLink>
            </nav>
        </h2>
    );
}

export default Header;
