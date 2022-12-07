// function to set user data to local storage

function set_user_data_to_local_storage(userData) {
    let user = JSON.parse(localStorage.getItem('user'));
    user['id'] = userData['id'];
    user['first_name'] = userData['first_name'];
    user['last_name'] = userData['last_name'];
    user['phone_number'] = userData['phone_number'];
    user['email'] = userData['email'];
    user['membership_duration'] = userData['membership_duration'];
    user['fee'] = userData['fee'];
    user['is_active'] = userData['is_active'];
    user['end_date'] = userData['end_date'];
    localStorage.setItem('user', JSON.stringify(user))

}

export default set_user_data_to_local_storage;