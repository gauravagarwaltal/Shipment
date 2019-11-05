import React, { useEffect, useState } from 'react';
import bg from './BG.jpeg';
import './App.css';
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";
import ConfirmDeposit from './components/ConfirmDeposit';
import ChannelDetailsPage from './components/ChannelDetailsPage';
import { ToastContainer } from 'react-toastify';
import Header from './Header';
import AboutPage from './AboutPage';
import HomePage from './HomePage';
import NotFoundPage from './NotFoundPage';
import CreateTransaction from './components/CreateTransaction';
import PendingResponses from './redisApi/PendingResponses';
import PendingRequests from './components/PendingRequests';
// import SocketReact from './SocketApi/testing';

const App = () => {
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const imageUrl = windowWidth >= 650 ? bg : bg;

  const handleWindowResize = () => {
    setWindowWidth(window.innerWidth);
  };

  useEffect(() => {
    window.addEventListener('resize', handleWindowResize);

    return () => {
      window.removeEventListener('resize', handleWindowResize);
    }
  });

  return (
    <div className="container-fluid" style={{ height: window.innerWidth, backgroundImage: `url(${imageUrl})` }}>
      <ToastContainer autoClose={3000} hideProgressBar />
      <Router>
        <Header />
        <Switch>
          <Route path="/" exact component={HomePage} />
          <Redirect from="/about-page" to="about" />
          <Route path="/about" component={AboutPage} />
          <Route path="/channeldetails" component={ChannelDetailsPage} />
          <Route path="/transaction" component={CreateTransaction} />

          <Route path="/confirmdeposit" component={ConfirmDeposit} />
          <Route path="/pendingResponses" component={PendingResponses} />
          <Route path="/pendingRequests" component={PendingRequests} />

          <Route component={NotFoundPage} />
        </Switch>

      </Router>

    </div>
  );

};

export default App;