import React from "react";
// import { Link } from "react-router-dom";
import UserList from './components/UserList';
import { CreateNewChannel } from './contract/contract_transaction';
import { Users } from "./mockData/mockUsers";


function HomePage() {
  return (
    <div className="jumbotron">
      <h1>Shipment Application</h1>
      <p>React, Flux, and React Router for ultra-responsive web apps.</p>
      {/* <Link to="plasmacash" className="btn btn-primary">
        Plasma Cash
      </Link>
      {"  "}
      <Link to="multichannel" className="btn btn-primary">
        Payment Channel
      </Link> */}
      <UserList users={Users} createNewChannel={CreateNewChannel} />
    </div>
  );
}

export default HomePage;
