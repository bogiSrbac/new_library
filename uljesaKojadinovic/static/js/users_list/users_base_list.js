let inputLetter = document.getElementById('inputLetter');
// let inputLetterBorrower = document.getElementById('inputLetterBorrower');
let landDate = document.getElementById('lendDate');
let chooseUser = document.getElementById('chooseUser');
let alertPlaceholder = document.getElementById('liveAlertPlaceholder');
let setBorrowerId = document.getElementById('setBorrower');
let listOfLetters = ['A', 'B', 'C', 'Č', "Ć", 'D', "Dž", "Đ", 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', "NJ", 'O', 'P', 'R', 'S', "Š", 'T', 'U', 'V', 'Z', "Ž",]

//enableing set borrower button


import setBorrowerDataToLocalStorage from "../set_borrower_to_local_storage/set_borrower_function.js";
import enableSetBorrowerButton from "../set_borrower_to_local_storage/enable_button_for_set_user.js";

//importig alert function
import alert from "../alerts/alert_unsuccess.js";

function createLetterOptions(listOfChar) {
    inputLetter.innerHTML = '';
    inputLetter.innerHTML += `<option selected>Choose...</option>`;
    for (let i = 0; i < listOfChar.length; i++) {
        inputLetter.innerHTML += `<option class="letter-options">${listOfChar[i]}</option>`;
    }
}

createLetterOptions(listOfLetters);
//borrower letter list

// function createBorrowerLetterOptions(listOfChar) {
//     inputLetterBorrower.innerHTML = '';
//     inputLetterBorrower.innerHTML += `<option selected>Choose...</option>`;
//     for (let i = 0; i < listOfChar.length; i++) {
//         inputLetterBorrower.innerHTML += `<option class="letter-options">${listOfChar[i]}</option>`;
//     }
// }
// createBorrowerLetterOptions(listOfLetters)


//fetch function get users data
import getUsersData from "./users_base_fetch_api.js";

let letterOptions = document.querySelectorAll('.letter-options');
let usersLetterList = async (letter, selesctForm, listOfChar) => {

    let data = await getUsersData(letter);
              console.log('new try', 'letterValue')

    let listOfUsers = [];
    let listOfID = [];
    if (data.length > 0) {
        alertPlaceholder.innerHTML = '';
        for (let i = 0; i < data.length; i++) {
            let userFullName = data[i]['last_name'] + ' ' + data[i]['first_name'];
            listOfUsers.push(userFullName)
            listOfID.push(data[i]['id'])
        }
    } else {
        let message = `There is no users in database with first letter ${letter} in last name!`;
        let type = 'danger';
        alert(alertPlaceholder, message, type)
    }

    setUsersSelect(listOfUsers, listOfID, selesctForm, listOfChar)
}

function getUsersFromDatabase(clickLetter, selesctForm, listOfChar) {
    clickLetter.addEventListener('change', function () {
        let letterValue = this.value;
        usersLetterList(letterValue, selesctForm, listOfChar)

    }, false)
}

getUsersFromDatabase(inputLetter, chooseUser, listOfLetters);

//set user to borrower
let nameFieldBorrowFormNew = document.getElementById('borrowerName');
let userBorrowerId = document.getElementById('userBorrowerId');


//function to separate name and last name to set in local storage
import separate from "../set_borrower_to_local_storage/seperate_name_in_list.js";

import setNameInBorrowBookForm from "../set_borrower_to_local_storage/setNameInBorrowerBookForm.js";

let nameFieldBorrowForm1 = document.getElementById('borrowerName');
let userBorrowerId1 = document.getElementById('userBorrowerId');

function setBorrower(inputField, id, array) {
    inputField.addEventListener('change', function () {
        let borrower = this.options[this.selectedIndex].text;
        let borrowerId = this.value;
        setNameInBorrowBookForm(nameFieldBorrowForm1, userBorrowerId1, borrower, borrowerId)
        separate(array, this.options[this.selectedIndex].text, this.value)
        enableSetBorrowerButton(setBorrowerId);
        let newUser = localStorage.getItem('user')
        console.log(JSON.parse(newUser))
    })
}

setBorrower(chooseUser, userBorrowerId, 'user')

//set users in select
function setUsersSelect(users, id, selesctForm, listOfChar) {
    selesctForm.innerHTML = '';
    selesctForm.innerHTML = `<option selected>Choose...</option>`;
    for (let j = 0; j < users.length; j++) {
        selesctForm.innerHTML += `<option class="users-options" value=${id[j]}>${users[j]}</option>`;
    }
    selesctForm.disabled = false;

    // createLetterOptions(listOfChar);

}



