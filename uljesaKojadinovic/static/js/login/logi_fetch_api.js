function loginFetchApi(userEmaill, userPassword) {
    const loginData = {
        email: `${userEmaill}`,
        password: `${userPassword}`,
    }
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest()
        xhr.responseType = 'json';
        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.response);
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                })
            }
        };
        xhr.onerror = function(){
            reject({
                status: status,
                statusText: xhr.statusText
            });
        }
        xhr.open('POST', 'http://127.0.0.1:8000/api/token/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', 'application/json',);
        xhr.send(JSON.stringify(loginData));
    })

}

export default loginFetchApi;