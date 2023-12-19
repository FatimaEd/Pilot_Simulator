function hideById(elementId) {
    let element = document.getElementById(elementId);
    element.classList.add("hidden");
}

function showById(elementId) {
    let element = document.getElementById(elementId);
    element.classList.remove("hidden");
}

function hideElement(element) {
    element.classList.add("hidden");
}

function showElement(element) {
    element.classList.remove("hidden");
}

function setInnerHtml(elementId, value) {
    let element = document.getElementById(elementId);
    element.innerHTML = value;
}
