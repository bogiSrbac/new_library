function setTokenInLocalStorage(key, data, action){
    if(action === 'set'){
       localStorage.setItem(key, `${data}`)
    }else if (action === 'get'){
       localStorage.getItem(key)
    }else if (action === 'delete'){
        localStorage.removeItem(key)
    }
}

export default setTokenInLocalStorage;





