$(document).ready(function () {
  $(".nav-link").each(function () {
    var direction = $("html").attr("lang");
    if (direction === "en") {
      var $link = $(this);
      var text = $link.text();
      $link.empty();

      $.each(text.split(""), function (index, char) {
        var $span = $("<span>")
          .text(char)
          .css("animation-delay", index * 0.1 + "s");
        $link.append($span);
      });
    }
  });

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
