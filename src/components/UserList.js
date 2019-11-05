import React from "react";
// import PropTypes from "prop-types";
// import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import './UserList.css'
function UserList(props) {
    return (
        <div>
            <h2>User DataBase</h2>
            <table id='table' className="table">
                <thead>
                    <tr>
                        <th>&nbsp;</th>
                        <th>Name</th>
                        <th>Address</th>
                        <th>Category</th>
                        <th>Listening On</th>
                    </tr>
                </thead>
                <tbody>
                    {props.users.map(user => {
                        return (
                            <tr key={user.id}>
                                <td>
                                    <button
                                        className="btn btn-outline-danger"
                                        onClick={() => {
                                            const min = 1000;
                                            const max = 100000000;
                                            const rand = Math.floor(min + Math.random() * (max - min));
                                            console.log(rand)
                                            props.createNewChannel(rand, user.address).then(() => {
                                                // Add Channel Id in List
                                                // set default state as an last state
                                                // set listening socket from UserList 
                                                toast.success("Channel Created with id " + rand);
                                            });
                                        }}
                                    >
                                        CreateChannel
                                </button>
                                </td>
                                <td>{user.name}</td>
                                <td>{user.address}</td>
                                <td>{user.category}</td>
                                <td>{user.listen}</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
}

// UserList.propTypes = {
//     deleteCourse: PropTypes.func.isRequired,
//     courses: PropTypes.arrayOf(
//         PropTypes.shape({
//             id: PropTypes.number.isRequired,
//             title: PropTypes.string.isRequired,
//             authorId: PropTypes.number.isRequired,
//             category: PropTypes.string.isRequired
//         })
//     ).isRequired
// };

export default UserList;
