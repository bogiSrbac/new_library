// import loginFetchApi from "./logi_fetch_api.js";
function createLoginForm(addToModalTag, addModalTitle) {
    addToModalTag.innerHTML = '';
    addToModalTag.innerHTML += `<form id="login-form" method="post" enctype="application/x-www-form-urlencoded">`;
    addToModalTag.innerHTML += `<div class="mb-3">`;
    addToModalTag.innerHTML += `<label for="email" class="col-form-label">Email:</label>`;
    addToModalTag.innerHTML += `<input type="email" class="form-control" id="email" name="email">`;
    addToModalTag.innerHTML += `</div>`;
    addToModalTag.innerHTML += `<div class="mb-3">`;
    addToModalTag.innerHTML += `<label for="password" class="col-form-label">Password:</label>`;
    addToModalTag.innerHTML += `<input type="password" class="form-control" id="password" name="password">`;
    addToModalTag.innerHTML += `<button type="submit" class="btn btn-primary mt-3" id="formButton">Login</button>`;
    addToModalTag.innerHTML += `</div></form>`;
    addModalTitle.innerHTML = 'User login form';
}
export default createLoginForm;










