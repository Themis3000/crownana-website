// crow cursor thing
const cursor_box = document.createElement("div");
cursor_box.id = "cursor_box";
document.body.appendChild(cursor_box);
const crow_cursor = document.createElement("img");
crow_cursor.className = "crow-cursor";
crow_cursor.src = "/resources/images/crow_cursor.svg";
const crow_cursor_open = document.createElement("img");
crow_cursor_open.className = "crow-cursor";
crow_cursor_open.src = "/resources/images/crow_cursor_open.svg";
cursor_box.appendChild(crow_cursor);
cursor_box.appendChild(crow_cursor_open);
window.onmousemove = (e) => {
    const x = e.pageX;
    const y = e.pageY;
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