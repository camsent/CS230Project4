const element = document.getElementById('random-element');
const viewportHeight = window.innerHeight;
const viewportWidth = window.innerWidth;
const elementHeight = element.offsetHeight; // Use offsetHeight for actual rendered height
const elementWidth = element.offsetWidth; // Use offsetWidth for actual rendered width

const randomTop = Math.floor(Math.random() * (viewportHeight - elementHeight));
const randomLeft = Math.floor(Math.random() * (viewportWidth - elementWidth));

element.style.top = randomTop + 'px';
element.style.left = randomLeft + 'px';
