# Shipment-UI

### Dependency Prerequisite

- [BlockChain](https://www.trufflesuite.com/docs/ganache/quickstart)
- [MetaMask Extension](https://addons.mozilla.org/en-US/firefox/addon/ether-metamask/)
- [Redis-server](https://github.com/gauravagarwaltal/Shipment/blob/master/shipment_redis/README.md)

Mac:
```
$ brew install node
$ npm install -g ganache-cli
```

Linux:

Install [Node.js](https://nodejs.org/en/download/). Then,
```
$ npm install -g ganache-cli
```

Run Shipment Redis Server:
```
PYTHONPATH=. python  Redis/RedisServer.py
```

Run Shipment UserInterface:
```
cd ../shipment_ui
npm start
```
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.
