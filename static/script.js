// document.addEventListener('scroll', ()=>{
//     let nav = document.querySelector('nav');
//     if (window.scrollY > 0){
//         nav.classList.remove("bg-dark");
//         nav.style.backgroundColor = "#e3f2fd";
//         nav.removeAttribute("data-bs-theme");
//     }
//     else{
//         nav.classList.add("bg-dark");
//         nav.setAttribute("data-bs-theme", "dark");
//     }
// });

document.addEventListener('scroll', () => {
    let nav = document.querySelector('nav');
    let dropdown = document.querySelector('.user-name');
    let searchButton = document.querySelector('.search-button');
    //let helloMessage = document.querySelector('.hello-message');

    if (window.scrollY > 0) {
        nav.classList.remove("bg-dark");
        nav.style.backgroundColor = "#e3f2fd";
        nav.removeAttribute("data-bs-theme");
        dropdown.classList.remove("link-light");

        // Change styles for search button and hello message
        searchButton.classList.remove("btn-light");
        searchButton.classList.add("btn-dark");
        //helloMessage.style.color = "#000"; // Use style.color to change text color
    } else {
        nav.classList.add("bg-dark");
        nav.setAttribute("data-bs-theme", "dark");
        dropdown.classList.add("link-light");


        // Revert styles for search button and hello message
        searchButton.classList.remove("btn-dark");
        searchButton.classList.add("btn-light");
        //helloMessage.style.color = "#e3f2fd"; // Revert text color
    }
});
