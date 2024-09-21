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
