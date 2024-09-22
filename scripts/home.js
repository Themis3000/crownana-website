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

// crow cursor thing
const document_wrapper = document.getElementById("document-wrapper");
document_wrapper.style.cursor = "none";
const crow_cursor = document.createElement("img");
crow_cursor.className = "crow-cursor";
crow_cursor.src = "../images/crow_cursor.svg";
const crow_cursor_open = document.createElement("img");
crow_cursor_open.className = "crow-cursor";
crow_cursor_open.src = "../images/crow_cursor_open.svg";
document_wrapper.appendChild(crow_cursor);
document_wrapper.appendChild(crow_cursor_open);
window.onmousemove = (e) => {
    const x = e.clientX;
    const y = e.clientY;
    crow_cursor.style.top = `${y}px`;
    crow_cursor.style.left = `${x}px`;
    crow_cursor_open.style.top = `${y}px`;
    crow_cursor_open.style.left = `${x}px`;
}
window.onmouseover = () => {
    crow_cursor.style.display = "block";
}
window.onmouseout = () => {
    crow_cursor.style.display = "none";
    crow_cursor_open.style.display = "none";
}
const caw_audio = new Audio('../audio/caw1.mp3');
window.onclick = () => {
    crow_cursor.style.display = "none";
    crow_cursor_open.style.display = "block";
    caw_audio.play();
    caw_audio.addEventListener("ended", () => {
        crow_cursor.style.display = "block";
        crow_cursor_open.style.display = "none";
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

//inspect animation
const inspect_container = document.getElementById("inspect");
const inspect_images = [];
for (let i = 1; i <= 134; i++) {
    const img = document.createElement("img");
    img.src = `../images/inspect/${i}.png`;
    img.className = "inspect-img";
    inspect_images.push(img);
}
document.addEventListener("keydown", async (e) => {
    console.log("click");
    if (e.key === "f") {
        console.log("clicked button");
        for (const inspect_image of inspect_images) {
            inspect_container.appendChild(inspect_image);
            await sleep((1/15)*1000);
            inspect_container.removeChild(inspect_image);
        }
    }
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}