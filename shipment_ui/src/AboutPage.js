import React from "react";
import { CheckTimeOut } from "./Utils/TimeUtils";
// import { GetReceipt } from "./contract/contract_transaction";

class AboutPage extends React.Component {

  componentDidMount() {
    console.log(CheckTimeOut(1576143863))
  }

  render() {
    return (
      <>
        <h2>About</h2>
        <p>This app uses React.</p>

      </>
    );
  }
}

export default AboutPage;

/*
local storage management

last fetched block(on chain ethereum block) ->
    let key = this.state.sender + '_last_fetched_block'

active channel id ->
    let key = this.state.sender + 'active_channel_ids'

waiting channel id ->
    let key = this.state.sender + 'waiting_channel_ids'

last signed state ->
    let key = this.state.sender + <channel_id> + '_last_signed_state'

    add contract_address when possible
    because it can be exploitted between different instance of this contract
    state structure -> Channel_id(number), Count(number), Alice_Cash(number), Bob_Cash(number), Signature(string wiht 0x)
    local storage -> all values will be concat using '_'
User dataBase ->
  let key = user_accounts

All latest update made by the application list
  all event by handler, state requested and state response are  added by all respective actions
  and can be deleted by the <sender> only in local storage
  just for information kind of list
    let key = this.state.sender + '_updates'
    */
