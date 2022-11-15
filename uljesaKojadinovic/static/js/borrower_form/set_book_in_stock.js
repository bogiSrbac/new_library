function setBookAndQuantity(htmlTagBook, htmlTagStock, book, stock) {
    htmlTagBook.innerHTML = "";
    htmlTagStock.innerHTML = "";
    htmlTagBook.value = book;
    htmlTagStock.value = stock;
}
export default setBookAndQuantity;