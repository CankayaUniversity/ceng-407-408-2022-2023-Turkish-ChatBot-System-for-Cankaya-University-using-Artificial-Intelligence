$(document).ready(function () {
    $(".megamenu").on("click", function (e) {
        e.stopPropagation();
    });
});


var Dropdowns = function () {
    var t = $(".dropup, .dropright, .dropdown, .dropleft")
        , e = $(".dropdown-menu")
        , r = $(".dropdown-menu .dropdown-menu");
    $(".dropdown-menu .dropdown-toggle").on("click", function () {
        var a;
        return (a = $(this)).closest(t).siblings(t).find(e).removeClass("show"),
            a.next(r).toggleClass("show"),
            !1
    }),
        t.on("hide.bs.dropdown", function () {
            var a, t;
            a = $(this),
                (t = a.find(r)).length && t.removeClass("show")
        })
}()


$(document).ready(function () {
    // executes when HTML-Document is loaded and DOM is ready

    // breakpoint and up  
    $(window).resize(function () {
        if ($(window).width() >= 980) {

            // when you hover a toggle show its dropdown menu
            $(".navbar .dropdown-toggle").hover(function () {
                $(this).parent().toggleClass("show");
                $(this).parent().find(".dropdown-menu").toggleClass("show");
            });

            // hide the menu when the mouse leaves the dropdown
            $(".navbar .dropdown-menu").mouseleave(function () {
                $(this).removeClass("show");
            });

            // do something here
        }
    });
    // document ready  
});



$(document).ready(function() {

});