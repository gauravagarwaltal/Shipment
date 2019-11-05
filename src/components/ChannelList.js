import React from 'react';

class ChannelList extends React.Component {
    render() {
        const countries = JSON.parse(localStorage.getItem("PayMentChannels") || "[]")
        console.log(countries)
        let countriesList = countries.length > 0
            && countries.map((item) => {
                return (
                    <option key={item} value={item}>{item}</option>
                )
            }, this);

        return (
            <div>
                <select id="channelId" onChange={this.props.onChange}>
                    {countriesList}
                </select>
            </div>
        );
    }
}

export default ChannelList;