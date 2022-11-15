//set users in select
function setBooksSelect(book, id, selesctForm) {
    selesctForm.innerHTML += `<option class="users-options" value=${id}>${book}</option>`;
    selesctForm.disabled = false;
}

export default setBooksSelect;