const lenis = new Lenis({
    duration:1.2,
    smoothWheel:true,
    normalizeWheel: true,
    infinite: false,
});

gsap.registerPlugin(ScrollTrigger);

lenis.on('scroll', ScrollTrigger.update);

gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
});

gsap.ticker.lagSmoothing(0);

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
