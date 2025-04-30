document.addEventListener("DOMContentLoaded", function() {
    var searchButton = document.getElementsByClassName("search-button-field")[0];
    if (searchButton) {
        var searchDiv = searchButton.parentNode;
        searchDiv.style.display = "none";
    }
});
