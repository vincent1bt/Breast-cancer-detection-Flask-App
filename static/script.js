function get_prediction(image) {
    const formData = new FormData()
    formData.append('image', image);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => {
        response.json().then(data => {
            const class_predicted = data["class"];
            const confidence = data["confidence"];

            loadingGif.style.display = "none";
            imageClass.innerHTML = `Class: ${class_predicted}`;
            imageConfidence.innerHTML = `Confidence: ${confidence}`;
        });
    })
    .catch(error => {
        console.log("There was an error");
    });
}

function imageUploaded(event) {
    const target = event.target;
    const image = target.files[0];

    if (!image) return;
    
    imageClass.innerHTML = "";
    imageConfidence.innerHTML = "";
    loadingGif.style.display = "block";
    imageContainer.src = window.URL.createObjectURL(image);

    get_prediction(image);
}

function ready() {
    imageClass = document.querySelector("#imageClass");
    imageConfidence = document.querySelector("#imageConfidence");
    imageContainer = document.querySelector("#imageContainer");
    loadingGif = document.querySelector("#loadingGif");

    const inputFile = document.querySelector("#image");
    inputFile.addEventListener('change', imageUploaded);
}

document.addEventListener("DOMContentLoaded", ready);

let imageContainer;
let imageClass;
let imageConfidence;
let loadingGif;