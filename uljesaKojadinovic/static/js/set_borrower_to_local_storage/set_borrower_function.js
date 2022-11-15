function setBorrowerDataToLocalStorage(buttonCgange, array, id, ln, fn) {
    let nameLastName = JSON.parse(localStorage.getItem(array))
    buttonCgange.addEventListener('click', () => {
        nameLastName.id = parseInt(id)
        nameLastName.last_name = ln
        nameLastName.first_name = fn
        localStorage.setItem('user', JSON.stringify(nameLastName))
        console.log(JSON.parse(localStorage.getItem(nameLastName)), 'kkkkk')
    })


}

export default setBorrowerDataToLocalStorage;