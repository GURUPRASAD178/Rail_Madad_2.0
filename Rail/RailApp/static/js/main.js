// Scroll-to-top button
document.addEventListener("DOMContentLoaded", function () {
    const toTop = document.createElement("button");
    toTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    toTop.className = "btn btn-warning position-fixed bottom-0 end-0 m-4 d-none";
    document.body.appendChild(toTop);

    window.addEventListener("scroll", () => {
        toTop.classList.toggle("d-none", window.scrollY < 300);
    });

    toTop.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});

// Highlight nav on scroll (if using scrollspy manually)
const navLinks = document.querySelectorAll('.nav-link');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
    });
});
