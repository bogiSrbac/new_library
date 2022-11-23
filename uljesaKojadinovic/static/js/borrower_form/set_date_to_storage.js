// set date to local storage

function setDateToStorage() {
    var dateField = document.getElementById('lendDate')
    var dateReturn = document.getElementById('returnDate')
    dateField.addEventListener('change', (e) => {
        let newData = JSON.parse(localStorage.getItem('bookForBorrow'))
        newData['lend_date'] = e.target.value;
        let oldDate = new Date(e.target.value);
        let newDateFirst = new Date()
        let newDate = new Date(newDateFirst.setDate(oldDate.getDate() + 15))
        dateReturn.value = newDate.getFullYear() + '-' + (newDate.getMonth() + 1).toString().padStart(2, "0") + '-' + newDate.getDate().toString().padStart(2, "0");
        localStorage.setItem('bookForBorrow', JSON.stringify(newData))
    })

}

export default setDateToStorage;