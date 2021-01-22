/*!
    * Start Bootstrap - Grayscale v6.0.3 (https://startbootstrap.com/theme/grayscale)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
    */
    (function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top - 70,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#mainNav",
        offset: 100,
    });

    // Collapse Navbar
    var navbarCollapse = function () {
        if ($("#mainNav").offset().top > 100) {
            $("#mainNav").addClass("navbar-shrink");
        } else {
            $("#mainNav").removeClass("navbar-shrink");
        }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
    
    // In the case of a variable like this, where it most likely won't be updated somewhere else in your code, it's good practice to declare it as a const.
    const indlimit = 10;
    $('input.single-checkbox').on('change', function(e) {
        // Check how many inputs of class 'single-checkbox' are checked.
        // Changed from a .siblings() check due to how you've modified your HTML.
        if( $('input.single-checkbox:checked').length > indlimit) {
            this.checked = false;
        }
    });

    const compalimit = 5;
    $('input.compa-single-checkbox').on('change', function(e) {
        // Check how many inputs of class 'single-checkbox' are checked.
        // Changed from a .siblings() check due to how you've modified your HTML.
        if( $('input.compa-single-checkbox:checked').length > compalimit) {
            this.checked = false;
        }
    });

    const compblimit = 5;
    $('input.compb-single-checkbox').on('change', function(e) {
        // Check how many inputs of class 'single-checkbox' are checked.
        // Changed from a .siblings() check due to how you've modified your HTML.
        if( $('input.compb-single-checkbox:checked').length > compblimit) {
            this.checked = false;
        }
    });

})(jQuery); // End of use strict