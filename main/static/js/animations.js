gsap.registerPlugin(ScrollTrigger);

/* ---------------- HERO ---------------- */

const tl = gsap.timeline();

tl.from("#navbar",{
    y:-120,
    opacity:0,
    duration:1,
    ease:"power4.out"
})

.from(".hero-badge",{
    y:-20,
    opacity:0,
    duration:.6
},"-=0.4")

.from(".hero-subtitle",{
    y:50,
    opacity:0,
    duration:.8
},"-=0.3")

.from(".hero-text h1",{
    y:120,
    opacity:0,
    duration:1,
    ease:"power4.out"
},"-=0.5")

.from(".hero-description",{
    y:60,
    opacity:0,
    duration:.8
},"-=0.4")

.from(".hero-text a",{
    y:40,
    opacity:0,
    stagger:.15,
    duration:.7
},"-=0.3")

.from(".hero-image",{
    x:180,
    opacity:0,
    duration:1.4,
    ease:"power4.out"
},"-=1")