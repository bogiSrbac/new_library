// button click event to set user data in borrower form and user form

// imported function to set user data to user form

import set_user_data_tu_user_form from "../user_form_scripts/set_user_data_to_form.js";

let setBorrowerId3 = document.getElementById('setBorrower');
function setNameInBorrowBookForm(nameFieldToSet, userBorrowerIdToSet, nameToSet, id) {
        setBorrowerId3.addEventListener('click', ele => {
            nameFieldToSet.value = nameToSet;
            userBorrowerIdToSet.value = id;
            set_user_data_tu_user_form();
        })
    }

export default setNameInBorrowBookForm;