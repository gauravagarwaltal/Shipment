const axios = require('axios');

const RedisHandlerURL = 'http://localhost:5002';

const FetchRequests = async (address, request_type) => {
    try {
        var bodyFormData = new FormData();
        // bodyFormData.set('channel_id', channelId);
        bodyFormData.set('address', address);
        bodyFormData.set('request_type', request_type);
        const resp = await axios({
            method: 'post',
            url: RedisHandlerURL + '/fetch_request',
            data: bodyFormData
        })
        if (resp.status === 200) {
            return resp.data;
        }
        return resp.data;
    } catch (error) {
        console.log("Redis connectivity issue")
        console.log(error)
    }
}

const SetRequest = async (address, request_type, request_data) => {
    try {
        var bodyFormData = new FormData();
        // bodyFormData.set('channel_id', channelId);
        bodyFormData.set('address', address);
        bodyFormData.set('request_type', request_type);
        bodyFormData.set('request_data', request_data);
        const resp = await axios({
            method: 'post',
            url: RedisHandlerURL + '/set_request',
            data: bodyFormData
        })
        if (resp.status === 200) {
            console.log('200 status')
            return resp.data;
        }
        console.log('00 status')
        return null;
    } catch (error) {
        console.log("Redis connectivity issue")
        console.log(error)
    }
}

const UpdateRequest = async (address, request_type, index, request_data) => {
    try {
        var bodyFormData = new FormData();
        // bodyFormData.set('channel_id', channelId);
        bodyFormData.set('address', address);
        bodyFormData.set('request_type', request_type);
        bodyFormData.set('index', index);
        bodyFormData.set('request_data', request_data);
        const resp = await axios({
            method: 'post',
            url: RedisHandlerURL + '/update_request',
            data: bodyFormData
        })
        if (resp.status === 200) {
            return resp.data;
        }
        return null;
    } catch (error) {
        console.log("Redis connectivity issue")
        console.log(error)
    }
}

const DeleteRequest = async (address, request_type, index) => {
    try {
        var bodyFormData = new FormData();
        // bodyFormData.set('channel_id', channelId);
        bodyFormData.set('address', address);
        bodyFormData.set('request_type', request_type);
        bodyFormData.set('index', index);
        const resp = await axios({
            method: 'post',
            url: RedisHandlerURL + '/delete_request',
            data: bodyFormData
        })
        if (resp.status === 200) {
            return resp.data;
        }
        return null;
    } catch (error) {
        console.log("Redis connectivity issue")
        console.log(error)
    }
}

const PublishData = async () => {


    var previous_response_length = 0
    let xhr = new XMLHttpRequest()
    xhr.open("GET", "http://127.0.0.1:6379/SUBSCRIBE/hello", true);
    xhr.onreadystatechange = checkData;
    xhr.send(null);

    function checkData() {
        if (xhr.readyState === 3) {
            const response = xhr.responseText;
            const chunk = response.slice(previous_response_length);
            previous_response_length = response.length;
            console.log(chunk);
        }
    }
}

export { FetchRequests, SetRequest, UpdateRequest, DeleteRequest, PublishData };