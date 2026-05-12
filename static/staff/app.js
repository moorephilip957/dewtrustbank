const sidebar = document.getElementById("sidebar");
const menuToggle = document.getElementById("menuToggle");
const mainContent = document.getElementById("mainContent");

const overlay = document.querySelector(".sidebar-overlay");
const closeSidebar = document.querySelector(".close-sidebar");

/*
|--------------------------------------------------------------------------
| Sidebar Toggle
|--------------------------------------------------------------------------
*/

menuToggle.addEventListener("click", () => {

    // Mobile
    if (window.innerWidth < 992) {

        sidebar.classList.toggle("mobile-active");
        overlay.classList.toggle("active");

    } else {

        // Desktop Collapse
        sidebar.classList.toggle("collapsed");
        mainContent.classList.toggle("expanded");

    }

});

/*
|--------------------------------------------------------------------------
| Close Sidebar Mobile
|--------------------------------------------------------------------------
*/

overlay.addEventListener("click", closeMobileSidebar);
closeSidebar.addEventListener("click", closeMobileSidebar);

function closeMobileSidebar() {

    sidebar.classList.remove("mobile-active");
    overlay.classList.remove("active");

}