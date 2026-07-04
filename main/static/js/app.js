const lenis = new Lenis({
    duration:1.2,
    smoothWheel:true
});

function raf(time){

    lenis.raf(time);

    requestAnimationFrame(raf);

}

requestAnimationFrame(raf);
// Success message auto hide

const success = document.getElementById("success-message");

if (success) {
    setTimeout(() => {
        success.style.transition = "all .5s ease";
        success.style.opacity = "0";
        success.style.transform = "translateY(-10px)";

        setTimeout(() => {
            success.remove();
        }, 500);

    }, 5000);
}