document.addEventListener("DOMContentLoaded", function () {
    const menuIcon = document.querySelector(".menu-icon");
    const navLinks = document.querySelector(".nav-links");

    menuIcon.addEventListener("click", function (event) {
        event.stopPropagation(); // Prevent click propagation issues
        navLinks.classList.toggle("active");
    });

    // Close menu when clicking outside
    document.addEventListener("click", function (event) {
        if (!navLinks.contains(event.target) && !menuIcon.contains(event.target)) {
            navLinks.classList.remove("active");
        }
    });
});


document.getElementById("read-more-btn").addEventListener("click", function () {
    event.preventDefault();
    var para = document.getElementById("about-para");
            

    para.classList.toggle("expanded");
    this.textContent = para.classList.contains("expanded") ? "Read Less" : "Read More";
    
});
    