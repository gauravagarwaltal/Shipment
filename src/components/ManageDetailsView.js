import React from "react"
import './ManageDetailsView.css'
function RenderObj(props) {
    return (
        <tbody>
            {
                Object.keys(props.details).map(priKey => {
                    if (!Number.isInteger(parseInt(priKey, 10))) {
                        return (
                            <tr key={priKey}>
                                <td >
                                    <span>{priKey}</span>
                                </td>
                                <td>
                                    <span>{props.details[priKey]}</span>
                                </td>
                            </tr>
                        )

                    }
                }
                )
            }
        </tbody>
    )
}

function ManageDetailsView(props) {

    return (
        <div>
            <table id="table" className="table">
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>value</th>
                    </tr>
                </thead>
                <RenderObj details={props.details} />
            </table>
        </div>
    )
}

export default ManageDetailsView;
