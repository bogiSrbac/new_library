const getUsersData = async (letter) => {
    let url = `http://127.0.0.1:8000/api/filters/users-filtered/${letter}`;
    let datesToReturn;

    await fetch(url, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
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

export default getUsersData;