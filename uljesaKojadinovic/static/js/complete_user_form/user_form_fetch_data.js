const if_current_user_has_book = async (user) => {
    let url = `http://127.0.0.1:8000/users/${user}`;
    let datesToReturn;
    await fetch(url, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((response) => {
        return response.json();
    }).then((data) => {
        datesToReturn = data
        console.log('user',  datesToReturn)
        return datesToReturn

    });
    return datesToReturn
}

export default if_current_user_has_book;