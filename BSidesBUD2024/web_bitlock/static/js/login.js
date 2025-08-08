function login() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let errorMessage = document.getElementById("errorMessage");

    fetch("/login", {
        method: "POST",
        body: encrypt(JSON.stringify({
            username,
            password
        }), "Porcica1"),
    }).then(async res => {
        if (res.ok) {
            window.location = "/";
        } else {
            errorMessage.innerText = await res.text();
            errorMessage.classList.remove("d-none");
        }
    });
}

function encrypt(plaintext, key) {
    let ciphertext = "";
    
    for (let i = 0; i < plaintext.length; i++) {
        ciphertext += String.fromCharCode(plaintext.charCodeAt(i) ^ key.charCodeAt(i % key.length));
    }

    return btoa(ciphertext);
}
