const getDatesForCheck = async (lang, userId, chaletId, csfrToken) => {
    let url = `/${lang}/reserved-dates/`;
    let dataToSend = {
        "chaletID": chaletId,
        "userId": userId,
    }
    let datesToReturn;
    await fetch(url, {
         method: "POST",
         credentials: "same-origin",
         headers: {
            Accept: "application/json",
            "X-Requested-With": "XMLHttpRequest",
             "X-CSRFToken": csfrToken,
         },
         body: JSON.stringify(dataToSend)
    }).then((response) => {
            return response.json();
        }).then((data) => {
            datesToReturn = data.message
        console.log(datesToReturn)
        for(let key in datesToReturn['userWarrning']){
            console.log(datesToReturn['userWarrning'][key][0])
        }

            return datesToReturn

        });
    return datesToReturn
}

export default getDatesForCheck;