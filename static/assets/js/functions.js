function generateRandomNumber() {
    var formInputs = document.getElementById('myForm').elements;
    console.log(formInputs);

    // Iterasi melalui semua elemen input
    for (var i = 0; i < formInputs.length; i++) {
        // Jika elemen input adalah elemen text
        if (formInputs[i].name === "age") {
            continue
        }

        if (formInputs[i].type === "number") {
            // Menghasilkan angka acak antara 0 dan 1 dengan maksimal 3 digit dibelakang koma
            var randomNumber = (Math.random() * 4).toFixed(2);

            // Memasukkan angka ke dalam input
            formInputs[i].value = randomNumber;
        }
    }
}