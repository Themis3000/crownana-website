const autoplayEvent = new Event("autoplay-allowed");
const star = document.getElementById("star");

star.addEventListener("animationend", () => {
    console.log("animation end");
});

// document.body.dispatchEvent(autoplayEvent);
