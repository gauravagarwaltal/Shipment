import React from "react";
import { CreateNewChannel } from "../contract/contract_transaction";
import ConfirmDeposit from "./ConfirmDeposit";
import { ABC } from "../redisApi/GetSetData";

function HomePage() {
    return (
        <div className="jumbotron">
            <h1>ShipMent WebSite Administration</h1>
            <p>Feel Free to Use this WebSite and raise concert to help us</p>
            <ABC />
            <ConfirmDeposit onSubmit={CreateNewChannel} />
        </div>
    );
}

export default HomePage;
