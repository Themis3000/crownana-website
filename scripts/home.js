//welcome audio and lobby
const background_wrapper = document.getElementById("background_wrapper");
const welcome = new Audio("../audio/välkommen.m4a");
const lobby = new Audio('../audio/Charlie\'s Here.wav');
lobby.loop = true;
welcome.play();
welcome.addEventListener("ended", () => {
   lobby.play();
   background_wrapper.style.display = "flex";
});

// banana bread menu thing
const menu_containers = document.querySelectorAll('.menu-item-container');
const banana_element_right = document.createElement('img');
banana_element_right.className = "banana-bread banana-right";
banana_element_right.src = "../images/banana_bread.png";
const banana_element_left = document.createElement('img');
banana_element_left.className = "banana-bread banana-left";
banana_element_left.src = "../images/banana_bread.png";
for (const menu_container of menu_containers) {
    menu_container.addEventListener("mouseenter", () => {
        menu_container.prepend(banana_element_left);
        menu_container.append(banana_element_right);
    });
    menu_container.addEventListener("mouseleave", () => {
       menu_container.removeChild(banana_element_left);
       menu_container.removeChild(banana_element_right);
    });
}


//hover audios
const blog_audio = new Audio("../audio/blog.mp3");
const gallery_audio = new Audio("../audio/gallery.mp3");
const about_audio = new Audio("../audio/about.mp3");
const blog_menu = document.getElementById("blog-menu");
const gallery_menu = document.getElementById("gallery-menu");
const about_menu = document.getElementById("about-menu");
blog_menu.addEventListener("mouseenter", () => {
   blog_audio.play();
});
blog_menu.addEventListener("mouseleave", () => {
    blog_audio.pause();
    blog_audio.fastSeek(0);
});
gallery_menu.addEventListener("mouseenter", () => {
   gallery_audio.play();
});
gallery_menu.addEventListener("mouseleave", () => {
    gallery_audio.pause();
    gallery_audio.fastSeek(0);
});
about_menu.addEventListener("mouseenter", () => {
   about_audio.play();
});
about_menu.addEventListener("mouseleave", () => {
    about_audio.pause();
    about_audio.fastSeek(0);
});