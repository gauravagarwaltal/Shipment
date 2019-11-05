var express = require('express')
var app = express()

app.post('/fetch_states', (function (req, res) {
    console.log(req.body)
    var data = req.body.channel_id;
    data = data + " " + req.body.address
    data = data + " " + req.body.request_type
    data = data + " " + req.body.address
    let response = JSON.stringify(data)
    res.send(response);
}))

app.post('/add_state', (function (req, res) {
    res.send("Tutorial on Angular");
}))

app.post('/delete_state', (function (req, res) {
    res.send("Tutorial on Angular");
}))

app.get('/publish', (function (req, res) {
    res.send('this route will implemented in future');
}))

app.get('/subscribe', (function (req, res) {
    res.send('this route will implemented in future');
}))

app.get('/unsubscribe', (function (req, res) {
    res.send('this route will implemented in future');
}))


app.get('/', (function (req, res) {
    res.send('Welcome to Redis Nodejs Server');
}))

var server = app.listen(5000, function () { });

// @app.route('/fetch_request', methods = ['POST'])
// def fetch_request():
// _channel_id = request.form['channel_id']
// _address = request.form['address']
// _request_type = request.form['request_type']
// fetched_request = redis_handler.get_list_value(_channel_id, _address, _request_type)
// payload = { 'requests': fetched_request }
// return jsonify(payload), 200


// @app.route('/set_request', methods = ['POST'])
// def set_request():
// _channel_id = request.form['channel_id']
// _address = request.form['address']
// _request_type = request.form['request_type']
// _request_data = request.form['request_data']
// index = redis_handler.set_list_value(_channel_id, _address, _request_type, _request_data)
// payload = { 'index': index }
// return jsonify(payload), 200


// @app.route('/update_request', methods = ['POST'])
// def update_request():
// _channel_id = request.form['channel_id']
// _address = request.form['address']
// _request_type = request.form['request_type']
// _index = request.form['index']
// _request_data = request.form['request_data']
// index = redis_handler.update_list_value(_channel_id, _address, _request_type, _index, _request_data)
// payload = { 'index': index }
// return jsonify(payload), 200


// @app.route('/delete_request', methods = ['POST'])
// def delete_request():
// _channel_id = request.form['channel_id']
// _address = request.form['address']
// _request_type = request.form['request_type']
// _index = request.form['index']
// index = redis_handler.delete_list_value(_channel_id, _address, _request_type, _index)
// payload = { 'index': index }
// return jsonify(payload), 200
