import React from "react";
import ClientClass from "./SocketApi/Client";

class AboutPage extends React.Component {
  render() {
    return (
      <>
        <h2>About</h2>
        <p>This app uses React.</p>
        <ClientClass />
      </>
    );
  }
}

export default AboutPage;
