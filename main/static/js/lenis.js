// Mobile Menu

const menuBtn = document.getElementById("menu-btn");
const mobileMenu = document.getElementById("mobile-menu");

if(menuBtn && mobileMenu){

    menuBtn.addEventListener("click",()=>{

        const isHidden = mobileMenu.classList.toggle("hidden");
        menuBtn.textContent = isHidden ? "☰" : "✕";

    });

    const menuLinks = mobileMenu.querySelectorAll("a");
    menuLinks.forEach(link => {
        link.addEventListener("click", () => {
            mobileMenu.classList.add("hidden");
            menuBtn.textContent = "☰";
        });
    });

}