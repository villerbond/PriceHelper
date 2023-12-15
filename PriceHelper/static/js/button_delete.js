const container = document.querySelector(".prod");
const button = container.querySelector(".button-delete");

container.addEventListener("mouseover", function(event) {
    if (event.target.classList.contains('button-delete')) {
        event.target.style.display = "block";
    }
});

container.addEventListener("mouseout", function(event) {
    if (event.target.classList.contains('button-delete')) {
        event.target.style.display = "none";
    }
});