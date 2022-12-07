// function to store book data to localstorage

function set_chosen_book_to_storage(bookData) {
    let book = {}
    if(typeof bookData.text !== 'undefined'){
        book["book_name"] = bookData.text;
        book["book"] = bookData.id
    }else {
        book["book_name"] = bookData.book_name
        book["book"] = bookData.id
    }
    console.log(bookData)

    book["id"] = bookData.id;
    book["in_stock"] = bookData.in_stock;
    localStorage.setItem(`bookForBorrow`, JSON.stringify(book))
}

export default set_chosen_book_to_storage;