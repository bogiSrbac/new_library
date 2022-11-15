function separate(array, firstLastName, id) {
    let nameList = firstLastName.split(/\s+/)
    let user = JSON.parse(localStorage.getItem(array))
    user.id = parseInt(id)
    user.last_name = nameList[0]
    user.first_name = nameList[1]
    localStorage.setItem(array, JSON.stringify(user))
    console.log(user)
}
export default separate;