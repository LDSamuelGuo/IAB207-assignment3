// Scroll to section code

function checkPage() {
    if (document.getElementById('pageID').innerHTML == 'home') {
        autoScroll();
    } else {
        window.location.href = '../index.html';
        setTimeout(() => {
            autoScroll();
        }, 1000)

    }
}
function autoScroll() {
    // Offset by 5vh, converted is equal to 46.45 px
    let width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

    let yOffset;

    if (width <= 930) {
        yOffset = -240;
    } else {
        yOffset = -180;
    }

    const element = document.getElementById('events');
    const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;

    window.scrollTo({ top: y, behavior: 'smooth' });
}

// document.getElementById('events-link').addEventListener('click', autoScroll);
document.getElementById('events-link').addEventListener('click', checkPage);

// Offset by 5vh, converted is equal to 46.45 px
let width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
// Scroll position check to change colour of event link if past there on page
let yOffset;

if (width <= 930) {
    yOffset = 120;
} else {
    yOffset = 60;
}
// Get event link id
const element = document.getElementById('events-link');


document.addEventListener('scroll', () => {

    // Get current window y position
    const top = window.pageYOffset || document.documentElement.scrollTop
    console.log(top);
    // Check if current y pos is greater than or equal to events section y position and change colour if true
    if (top >= (1450 + yOffset)) {
        element.classList.add('active');
    } else {
        element.classList.remove('active');
    }

});