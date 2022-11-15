let setBorrowerId3 = document.getElementById('setBorrower');
function setNameInBorrowBookForm(nameFieldToSet, userBorrowerIdToSet, nameToSet, id) {
        setBorrowerId3.addEventListener('click', ele => {
            nameFieldToSet.value = nameToSet;
            userBorrowerIdToSet.value = id;
        })
    }

export default setNameInBorrowBookForm;