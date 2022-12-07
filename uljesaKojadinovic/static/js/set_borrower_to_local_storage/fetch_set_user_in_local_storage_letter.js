const getUsersDataByLetterLocalStorage = async (pk, token) => {
    let url = `http://127.0.0.1:8000/api/user/user/${pk}`;
    let datesToReturn;

    await fetch(url, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "Authorization": `Bearer ${token}`,
        },
    }).then((response) => {
        return response.json();
    }).then((data) => {
        datesToReturn = data
        console.log(datesToReturn)
        return datesToReturn

    });
    return datesToReturn
}

export default getUsersDataByLetterLocalStorage;