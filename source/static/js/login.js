async function loginButtonClick() {
    let username = document.getElementById("username");
    let password = document.getElementById("password");

    let successful = await login(username.value, password.value);

    if (successful) {
        location.reload();
    } else {
        showById("invalid-cred-text");
        username.value = "";
        password.value = "";
        username.focus();
    }
}