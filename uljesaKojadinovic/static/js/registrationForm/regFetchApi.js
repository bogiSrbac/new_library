const registrationFetchApi = async (userEmail, userPassword, userPasswordConfirm, firstName, lastName, phonenumber, membership_duration, fee) => {
    let url = "http://127.0.0.1:8000/api/user/signup/";
    console.log(userEmail, userPassword, userPasswordConfirm, firstName, lastName, phonenumber, membership_duration, fee)
    const registrationData = {
        email: `${userEmail}`,
        password: `${userPassword}`,
        confirm_password: `${userPasswordConfirm}`,
        first_name: `${firstName}`,
        last_name: `${lastName}`,
        phone_number: `${phonenumber}`,
        membership_duration: `${membership_duration}`,
        fee: `${fee}`,
    }
    let datesToReturn;
    await fetch(url, {
        method: "POST",
        mode: 'cors',
        credentials: "same-origin",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify(registrationData),
    }).then((response) => {
        return response.json();
    }).then((data) => {
        datesToReturn = data
        console.log(datesToReturn)

        return datesToReturn

    });
    return datesToReturn
}

export default registrationFetchApi;