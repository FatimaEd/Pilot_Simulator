/*
This js file contains all the necessary HTTP methods (post,get,patch,delete) using ajax so that it can be reused
when necessary.
We have kept our current username as variable, so that it can be verified against flask's session.
*/


async function createResponse(response) {
    const contentLength = response.headers.get('Content-Length');

    if (contentLength === '0' || !contentLength) {
        return {
            "body": null,
            "status": response.status
        };
    } else {
        return {
            "body": await response.json(),
            "status": response.status
        };
    }
}


async function postData(apiUrl, payload) {

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    return  createResponse(response);
}


async function patchData(apiUrl, payload, username) {

    const response = await fetch(apiUrl, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });


    const contentLength = response.headers.get('Content-Length');

    if (contentLength === '0' || !contentLength) {
        return null;
    } else {
        return await response.json();
    }
}

async function getData(apiUrl) {

    const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    return createResponse(response);
}

async function deleteData(apiUrl) {

    const response = await fetch(apiUrl, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const contentLength = response.headers.get('Content-Length');

    if (contentLength === '0' || !contentLength) {
        return null;
    } else {
        return await response.json();
    }
}

async function login(username, password) {

    let payload = {
        "username": username,
        "password": password
    }

    const response = await fetch("/api/login", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    return response.ok;
}