$(document).ready(function () {
  var navbar = $(".navbar");

  function toggleNavbarBackground() {
    if (navbar.hasClass("scrollednav")) {
      navbar.css("background-color", "#0096c78c");
    } else {
      navbar.css("background-color", "transparent");
    }
  }
  $(window).on("scroll", function () {
    if ($(this).scrollTop() > 50) {
      navbar.addClass("scrollednav").removeClass("topnavbar");
    } else {
      navbar.addClass("topnavbar").removeClass("scrollednav");
    }
    toggleNavbarBackground();
  });

  $(".navbar-toggler").click(function () {
    navbar.toggleClass("scrollednav");
    toggleNavbarBackground();
  });
});
