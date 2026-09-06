const autoplayEvent = new Event("autoplay-allowed");
const star = document.getElementById("star");
const okay_button = document.getElementById("accept-sound");
const deny_button = document.getElementById("deny-sound");
const autoplay_div = document.getElementById("autoplay");
const animation = star.getAnimations()[0];


const testAudio = new Audio("/resources/audio/silent.mp3");
testAudio.play()
    .then(() => {
        console.log("Autoplay allowed!");
        document.body.dispatchEvent(autoplayEvent);
    }).catch(() => {
        console.log("No autoplay allowed!");
        autoplay_div.style.display = "block";
        animation.play();
    });

okay_button.addEventListener("click", () => {
    animation.reverse();
    star.addEventListener("animationend", () => {
        autoplay_div.style.display = "None";
        document.body.dispatchEvent(autoplayEvent);
    });
});

deny_button.addEventListener("click", () => {
    alert("Sorry, you'll have to just move along then");
});
