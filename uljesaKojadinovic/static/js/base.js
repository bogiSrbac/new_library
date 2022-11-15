const homeConteiner = document.querySelectorAll('.home-conteiner')
const navLinksId = document.querySelectorAll('.nav-link')
const modalBody = document.querySelector('.modal-body')
const modalTitle = document.querySelector('.modal-title')


//modal import
import getLoginModal from "./modal/modal.js";

//login js import
import createLoginForm from "./login/login_jwt.js";
import loginFetchApi from "./login/logi_fetch_api.js";
import setTokenInLocalStorage from "./localStorageSetFunction/setTokenToStorage.js";

//login function
let loginGetJWTokenFunction = async (email, password) => {
    let token = await loginFetchApi(email, password)
    setTokenInLocalStorage('accessToken', token.access, 'set');
}
//registration form
import createRegistrationForm from "./registrationForm/registration_form.js";
//registration function
import registrationFetchApi from "./registrationForm/regFetchApi.js";
let registrationFunction = async (userEmail, userPassword, userPasswordConfirm, firstName, lastName, phonenumber, membership_duration, fee) => {
    let data = await registrationFetchApi(userEmail, userPassword, userPasswordConfirm, firstName, lastName, phonenumber, membership_duration, fee)
}


function setUiInterface(id) {
    homeConteiner.forEach((ele, index) =>{
        if (ele.classList.contains('appear')){
            ele.classList.remove('appear');
        }

    })
    navLinksId.forEach(ele => {
        if(ele.classList.contains('active')){
             ele.classList.remove('active');

        }
    })
    homeConteiner[id].classList.add('appear');
    navLinksId[id].classList.add('active');
    console.log(String.fromCharCode(267))
    if(homeConteiner[id].childNodes[1].innerText === 'LogIn' && homeConteiner[id].classList.contains('appear')){
            createLoginForm(modalBody, modalTitle)
            getLoginModal('show');
            let loginForm = document.getElementById('formButton')
            loginForm.addEventListener('click', ()=>{
                console.log('submit button')
                let email = document.getElementById('email').value
                let password = document.getElementById('password').value
                loginGetJWTokenFunction(email, password)
                getLoginModal('hide')
            })

        }else if(homeConteiner[id].childNodes[1].innerText === 'Registration' && homeConteiner[id].classList.contains('appear')){
            createRegistrationForm(modalBody, modalTitle)
            getLoginModal('show');
            let registrationForm = document.getElementById('reistrationFormButton')
            registrationForm.addEventListener('click', ()=>{
                console.log('submit button')
                let email = document.getElementById('email').value
                let name = document.getElementById('name').value
                let lastName = document.getElementById('last-name').value
                let phonenumber = document.getElementById('phonenumber').value
                let select1 = document.querySelector('.select1-class');
                let select2 = document.querySelector('.select2-class');
                let membership_duration = select1.options[select1.selectedIndex].text;
                let fee = select2.options[select2.selectedIndex].text;
                console.log(membership_duration, fee);
                let password = document.getElementById('password').value
                let passwordConfirm = document.getElementById('password-confirm').value
                registrationFunction(email, password, passwordConfirm,
                    name, lastName, phonenumber, membership_duration, fee)
                getLoginModal('hide')
            })

        }
}

function changePage(listOfLinks) {
    listOfLinks.forEach((ele, index) => {
        ele.addEventListener('click', () => {
            setUiInterface(index)
        })
    })

}

changePage(navLinksId);