import React from "react"
import './RenderSubscribedDetails.css'
import { toast } from "react-toastify";

function RenderObject(props) {
    return (
        <tbody>
            {
                Object.keys(props.details).map(request => {
                    return (
                        <tr key={request}>
                            <td>
                                <button
                                    className="btn btn-outline-danger"
                                    onClick={() => {
                                        props.handleDeleteClick(props.details[request]).then(() => {
                                            // Add Channel Id in List
                                            // set default state as an last state
                                            // set listening socket from UserList 
                                            toast.success("Channel Created");
                                        });
                                    }}
                                >
                                    CreateChannel
                                </button>
                            </td>
                            <td>{props.details[request]}</td>
                            <td>props.details[request].count</td>
                            <td>props.details[request].A_Cash</td>
                            <td>props.details[request].B_Cash</td>
                        </tr>
                    )

                }
                )
            }
        </tbody>
    )
}

function RenderSubscribedDetails(props) {

    return (
        <div>
            <table id="table" className="table">
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>value</th>
                    </tr>
                </thead>

                <RenderObject details={props.details} handleDeleteClick={props.handleDeleteClick} />
            </table>
        </div>
    )
}

export default RenderSubscribedDetails;
