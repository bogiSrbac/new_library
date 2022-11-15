var myModal = new bootstrap.Modal(document.getElementById('libraryModal'), {
    keyboard: true,
    focus: true
})

function getLoginModal(modalShowHide) {
    if(modalShowHide === 'show'){
        myModal.show()
    } else if (modalShowHide==='hide'){
        myModal.hide()
    }
    
}

export default getLoginModal;