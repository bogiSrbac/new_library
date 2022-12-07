// send new payload od borrow book data


const set_new_borrow_book_data_to_db = async (payload, token) => {
    let url = `http://127.0.0.1:8000/api/borrow/borrow-book-new`;
    let datesToReturn;

    await fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(payload)
    }).then((response) => {
        return response.json();
    }).then((data) => {
        datesToReturn = data
        console.log(datesToReturn)
        return datesToReturn

    });
    return datesToReturn
}

export default set_new_borrow_book_data_to_db;