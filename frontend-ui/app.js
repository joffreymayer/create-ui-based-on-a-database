// Animation of appearing upwards...
const jobs = document.querySelectorAll(".jobs-item")

const observer = new IntersectionObserver(
    entries => {
        entries.forEach(entry => {
            entry.target.classList.toggle("show", entry.isIntersecting)
            if (entry.isIntersecting) observer.unobserve(entry.target)
        })
    })

jobs.forEach(job => {
    observer.observe(job)
})

// This code will randomly allocate images to all the cards (by looping through all the images and allocating each `<img>` an image in my folder):
let images = document.querySelectorAll('img');
let imageList = ['/create-ui-based-on-a-database/frontend-ui/img/img-1.jpg', '/create-ui-based-on-a-database/frontend-ui/img/img-2.jpg', '/create-ui-based-on-a-database/frontend-ui/img/img-3.jpg', '/create-ui-based-on-a-database/frontend-ui/img/img-4.jpg', '/create-ui-based-on-a-database/frontend-ui/img/img-5.jpg', '/frontend-ui/img/img-6.jpg', '/create-ui-based-on-a-database/frontend-ui/img/img-7.jpg', '/create-ui-based-on-a-database/frontend-ui/img/img-8.jpg']; // List of all(!) the images' paths.

images.forEach(image => {
    let randomImage = imageList[Math.floor(Math.random()*imageList.length)];
    image.src = randomImage;
});
