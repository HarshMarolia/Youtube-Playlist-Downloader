$(document).ready(function () {
    if ($('.typed').length) {
        var typed = new Typed('.typed', {
            strings: ["Download your entire YouTube playlist in just a few steps!!"],
            loop: true,
            typeSpeed: 100,
            backSpeed: 50,
            backDelay: 2000
        });
    }
});
const btn = document.querySelector('#dbutt');
btn.addEventListener('click', () => {
    swal("Yayy", "Your Downloading has begun!", { icon: "success", });
});