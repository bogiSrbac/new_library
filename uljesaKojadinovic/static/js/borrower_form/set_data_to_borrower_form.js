$(document).ready(function () {
    var url;
    $('#findBook').select2({
        placeholder: "example:Thomas Mann",
        closeOnSelect: true,
        minimumInputLength: 1,
        theme: "bootstrap-5",
        selectionCssClass: "select2--small", // For Select2 v4.1
        dropdownCssClass: "select2--small",
        width: '100%',
        ajax: {
            url: function (params) {
                return `http://127.0.0.1:8000/api/filters/list-author/${params.term}`;
            },
            dataType: 'json',

            processResults: function (data) {
                // Transforms the top-level key of the response object from 'items' to 'results'
                return {
                    results: $.map(data, function (item) {
                        var key = '';
                        var children = []
                        console.log(data)
                        $.map(item, function (newItem) {

                            if (newItem.book_name) {
                                key = "Books"
                                children.push({
                                    "id": newItem.id,
                                    "text": newItem.book_name,
                                    "key": key,
                                    "in_stock": newItem.in_stock,
                                })
                            }
                            if (newItem.first_name) {
                                key = "Authors"
                                children.push({
                                    "id": newItem.id,
                                    "text": newItem.last_name + ' ' + newItem.first_name,
                                    "key": key,
                                    "allData": newItem
                                })
                            }
                            console.log(children)
                        })
                        return {
                            text: key,
                            children: children,
                        }
                    })
                };
            },
            data: function (params) {
                var query = {
                    search: params.term,
                }
                // Query parameters will be ?search=[term]&type=public
                url = query['search']
                return {json: JSON.stringify(query)};
            },
        }
    })
});

import setBooksSelect from "./set_list_of_books.js";
import setBookAndQuantity from "./set_book_in_stock.js";
import set_chosen_book_to_storage from "./set_choosen_book_to_localstorage.js";
import resetDateField from "./reset_date_field.js";

let booksSelect = document.getElementById('chooseBook');
let choosenBook = document.getElementById('choosenBook');
let bookQuantity = document.getElementById('bookQuantity');


$('#findBook').on('select2:select', function (e) {
    var data = e.params.data;
    console.log(data)
    booksSelect.innerHTML = "";

    if (data.key === "Books") {
        choosenBook.value = "";
        bookQuantity.value = "";
        choosenBook.value = data.text;
        bookQuantity.value = data.in_stock;
        set_chosen_book_to_storage(data);
        resetDateField();


    } else if (data.key === "Authors") {
        booksSelect.innerHTML = `<option selected>Books...</option>`;
        let counter = 0
        $.map(data.allData.books, function (items) {
            let book = {}
            book["book_name"] = items.book_name;
            book["ganres"] = items.ganres;
            book["id"] = items.id;
            book["in_stock"] = items.in_stock;
            localStorage.setItem(`book-${counter}`, JSON.stringify(book))
            setBooksSelect(items.book_name, `book-${counter}`, booksSelect)
            counter++;
        })
        $(document).on('change', 'select', function () {
            let bookData = JSON.parse(localStorage.getItem(booksSelect.value))
            if (bookData !== null) {
                let book = bookData.book_name;
                let stock = bookData.in_stock;
                console.log(bookData, 'book data')
                setBookAndQuantity(choosenBook, bookQuantity, book, stock)
                set_chosen_book_to_storage(bookData)
                resetDateField;
            }
        });


        // let book = {}
        // book["book_name"] = item.book_name;
        //
        // localStorage.setItem('book', JSON.stringify())

    }

});

import setDateToStorage from "./set_date_to_storage.js";
setDateToStorage();

localStorage.setItem('bookForBorrow', JSON.stringify({}))