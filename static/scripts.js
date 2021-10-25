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
    
    // Custom Validation Code

    // Index Checkbox Limit

    const indlimit = 10;
    $('input.single-checkbox').on('change', function() {
        // Check how many inputs of class 'single-checkbox' are checked.
        if( $('input.single-checkbox:checked').length > indlimit) {
            this.checked = false;
        }
    });

    // Compare Team A Checkbox Limit

    const compalimit = 5;
    $('input.compa-single-checkbox').on('change', function() {
        // Check how many inputs of class 'single-checkbox' are checked.
        if( $('input.compa-single-checkbox:checked').length > compalimit) {
            this.checked = false;
        }
    });

    // Compare Team B Checkbox Limit

    const compblimit = 5;
    $('input.compb-single-checkbox').on('change', function() {
        // Check how many inputs of class 'single-checkbox' are checked.
        if( $('input.compb-single-checkbox:checked').length > compblimit) {
            this.checked = false;
        }
    });

    // Count Index Checkboxes that are checked

    $('input.single-checkbox').on('change', function() {
        var indexnumber = $('input.single-checkbox:checked').length;
        $('.indextotalchecked').html(10 - indexnumber);
    });

    // Count Compare A Checkboxes that are checked

    $('input.compa-single-checkbox').on('change', function() {
        var companumber = $('input.compa-single-checkbox:checked').length;
        $('.compatotalchecked').html(5 - companumber);
    });

    // Count Compare B Checkboxes that are checked

    $('input.compb-single-checkbox').on('change', function() {
        var compbnumber = $('input.compb-single-checkbox:checked').length;
        $('.compbtotalchecked').html(5 - compbnumber);
    });

    // Change Image with dropdown

    $('#changeImageA').change(function(){
        $('#imageA')[0].src = "/static/"+this.value+".png";
    });

    // Change Image with dropdown

    $('#changeImageB').change(function(){
        $('#imageB')[0].src = "/static/"+this.value+".png";
    });

})(jQuery); // End of use strict