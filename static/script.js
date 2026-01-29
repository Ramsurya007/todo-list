// Toggle Profile Dropdown
function toggleProfile() {
    var dropdown = document.getElementById("profile-dropdown");
    if (dropdown.style.display === "none" || dropdown.style.display === "") {
        dropdown.style.display = "block";
    } else {
        dropdown.style.display = "none";
    }
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('img')) {
        var dropdown = document.getElementById("profile-dropdown");
        if (dropdown && dropdown.style.display === "block") {
            dropdown.style.display = "none";
        }
    }
}
