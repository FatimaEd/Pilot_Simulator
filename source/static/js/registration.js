async function registerButtonClick() {
    let username = document.getElementById("username");
    let fullName = document.getElementById("full_name");
    let password = document.getElementById("password");

    let payload = {
        "username": username.value,
        "full_name": fullName.value,
        "password": password.value
    }

    let response = await postData("/api/registration", payload);

    if (response.status === 200) {
        location.reload();
    } else {
        showById("reg-failed-text");
        username.focus();
    }
}
