// crow cursor thing
const cursor_box = document.createElement("div");
cursor_box.id = "cursor_box";
cursor_box.style.pointerEvents = "all";
document.body.appendChild(cursor_box);
const crow_cursor = document.createElement("img");
crow_cursor.className = "crow-cursor";
crow_cursor.src = "/resources/images/crow_cursor.svg";
const crow_cursor_open = document.createElement("img");
crow_cursor_open.className = "crow-cursor";
crow_cursor_open.src = "/resources/images/crow_cursor_open.svg";
cursor_box.appendChild(crow_cursor);
cursor_box.appendChild(crow_cursor_open);

window.onmousemove = (e) => { updateCursor(e); console.log("window move"); }
document.onmouseover = (e) => { updateCursor(e); console.log("document over"); }

function updateCursor(e) {
    const mouseX = e.pageX;
    const mouseY = e.pageY - window.scrollY;
    crow_cursor.style.top = `${mouseY}px`;
    crow_cursor.style.left = `${mouseX}px`;
    crow_cursor_open.style.top = `${mouseY}px`;
    crow_cursor_open.style.left = `${mouseX}px`;
    crow_cursor.style.display = "block";
    cursor_box.style.pointerEvents = "none";
}

window.onmouseout = () => {
    crow_cursor.style.display = "none";
    crow_cursor_open.style.display = "none";
}
const caw_audio = new Audio('/resources/audio/caw1.mp3');
window.onclick = () => {
    crow_cursor.style.display = "none";
    crow_cursor_open.style.display = "block";
    caw_audio.play();
    caw_audio.addEventListener("ended", () => {
        crow_cursor.style.display = "block";
        crow_cursor_open.style.display = "none";
    });
}

//inspect animation
const inspect_container = document.createElement("div");
inspect_container.id = "inspect";
document.body.appendChild(inspect_container);
const inspect_images = [];
document.addEventListener("keydown", async (e) => {
    if (inspect_images.length === 0) {
        for (let i = 1; i <= 134; i++) {
            const img = document.createElement("img");
            img.src = `/resources/images/inspect/${i}.png`;
            img.className = "inspect-img";
            img.decoding = "sync";
            inspect_images.push(img);
        }
    }
    if (e.key.toLowerCase() === "f") {
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

//home button adder
if (!document.querySelector("[name=noHome][content=true]")) {
    const homeA = document.createElement("a");
    homeA.id = "home-btn";
    homeA.href = "/index.html";
    const homeImg = document.createElement("img");
    homeImg.src = "/resources/images/home.png";
    homeImg.alt = "home button image";
    document.body.appendChild(homeA);
    homeA.appendChild(homeImg);
}
