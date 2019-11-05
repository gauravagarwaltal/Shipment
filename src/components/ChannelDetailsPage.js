import React, { useState } from "react";
// import courseStore from "../stores/courseStore";
// import { toast } from "react-toastify";
// import * as courseActions from "../actions/courseActions";
import { GetChannelDetails } from "../contract/contract_transaction";
import ManageDetailsView from "./ManageDetailsView";
// import { fetchLastState } from "../Api/FetchBrowserData";
import ChannelList from "./ChannelList";

const ChannelDetailsPage = props => {
    const [errors, setErrors] = useState(false);
    const [channelId, setChannelId] = useState("");
    const [details, setDetails] = useState("");
    const [value, setValue] = useState("");
    const [channels, setChannels] = React.useState(JSON.parse(localStorage.getItem("PayMentChannels") || "[]"));
    // const [course, setCourse] = useState({
    //     id: null,
    //     slug: "",
    //     title: "",
    //     authorId: null,
    //     category: ""
    // });

    async function onAddChange(event) {
        event.preventDefault();
        var index = channels.indexOf(value);
        if (index < 0) {
            channels.push(value)
            localStorage.setItem('PayMentChannels', JSON.stringify(channels));
        }
        console.log("onAddChange Called ", value)
    }

    async function onDeleteChange(event) {
        event.preventDefault();
        var index = channels.indexOf(value);
        if (index > -1) {
            channels.splice(index, 1);
        }
        // channels.push(value)
        // alert(channels)
        localStorage.setItem('PayMentChannels', JSON.stringify(channels));
        // localStorage.removeItem('Tempchannels')
        console.log("onDeleteChange Called ", value)
    }

    const onValueChange = event => setValue(event.target.value);

    async function handleSubmit(event) {
        event.preventDefault();
        setErrors("");
        if (Number.isNaN(parseInt(channelId, 10))) {
            setErrors("Enter Interger channel Id")
        }
        else {
            let value = await GetChannelDetails(channelId)
            setDetails(value);
        }
    }

    const onOptionChange = event => setChannelId(event.target.value)

    return (
        <>
            <h2>Channel Details</h2>
            <div>
                <div>
                    <h3>Add or remove channel (using channel id) from localStorage</h3>
                    <form id="form">
                        <input value={value} type="text" onChange={onValueChange} />
                        <button id="button" onClick={onAddChange}>Add Channel Id </button>
                        <button id="button" onClick={onDeleteChange}>Delete Channel Id </button>
                    </form>
                    <p>channel -> '{JSON.stringify(channels)}'</p>
                </div>
                <div>
                    <form id="form" onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="channelId">Channel Id</label>
                            <div className="field">
                                <ChannelList onChange={onOptionChange} />
                            </div>
                            {errors && <div className="alert alert-danger">{errors}</div>}
                        </div>
                        <button id="button">Get Channel Details</button>
                    </form>
                    {(errors === '') && (
                        <div >
                            <h2>Channel Details of channel id -> {channelId}</h2>
                            <ManageDetailsView details={details} />
                        </div>
                    )}
                </div>
                {/* <EditFiles /> */}
            </div>
        </>
    );
};

export default ChannelDetailsPage;
