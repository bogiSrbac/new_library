// set user data to user form
var userName = document.getElementById('userName');
var userLastName = document.getElementById('userLastName');
var userPhoneNumber = document.getElementById('userPhoneNumber');
var userEmail = document.getElementById('userEmail');
var membershipDuration = document.getElementById('membershipDuration');
var feeForUser = document.getElementById('feeForUser');
var endDate = document.getElementById('end_date');
var isActive = document.getElementById('is_active');

function set_user_data_tu_user_form() {
    let data = JSON.parse(localStorage.getItem('user'))
    userName.value = data['first_name'];
    userLastName.value = data['last_name'];
    userPhoneNumber.value = data['phone_number'];
    userEmail.value = data['email'];

    let memb = data['membership_duration'];
    for (let i = 0; i < membershipDuration.length; i++) {
        if(membershipDuration[i].text === memb){
            membershipDuration.selectedIndex = i;
            break
        }
    }

    let fee = data['fee'];
    for (let j = 0; j < feeForUser.length; j++) {
        if(feeForUser[j].text === fee.toString() + '.00'){
            feeForUser.selectedIndex = j;
            break
        }
    }

    endDate.value = data['end_date'];
    if(data['is_active']){
        isActive.checked = true
    } else {
        isActive.checked = false
    }

}

export default set_user_data_tu_user_form;
























