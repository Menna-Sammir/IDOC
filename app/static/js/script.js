(function ($) {
<<<<<<< HEAD
  "use strict";
=======
  'use strict';
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97

  // Stick Sidebar

  if ($(window).width() > 767) {
<<<<<<< HEAD
    if ($(".theiaStickySidebar").length > 0) {
      $(".theiaStickySidebar").theiaStickySidebar({
=======
    if ($('.theiaStickySidebar').length > 0) {
      $('.theiaStickySidebar').theiaStickySidebar({
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
        // Settings
        additionalMarginTop: 30,
      });
    }
  }

<<<<<<< HEAD
  $(window).on("load", function () {
    setTimeout(function () {
      $(".loader").fadeOut("slow");
      $(".main-wrapper").css("opacity", "1");
    }, 2500);

    // preview image after upload
    $(".upload").on("change", function (event) {
      var file = event.target.files[0];
      var reader = new FileReader();
      reader.onload = function (event) {
        $("#imagePreview").attr("src", event.target.result);
=======
  $(window).on('load', function () {
    setTimeout(function () {
      $('.loader').fadeOut('slow');
      $('.main-wrapper').css('opacity', '1');
    }, 2500);

    // preview image after upload
    $('.upload').on('change', function (event) {
      var file = event.target.files[0];
      var reader = new FileReader();
      reader.onload = function (event) {
        $('#imagePreview').attr('src', event.target.result);
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      };
      reader.readAsDataURL(file);
    });
  });

  // Sidebar
  if ($(window).width() <= 991) {
    var Sidemenu = function () {
<<<<<<< HEAD
      this.$menuItem = $(".main-nav a");
=======
      this.$menuItem = $('.main-nav a');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    };

    function init() {
      var $this = Sidemenu;
<<<<<<< HEAD
      $(".main-nav a").on("click", function (e) {
        if ($(this).parent().hasClass("has-submenu")) {
          e.preventDefault();
        }
        if (!$(this).hasClass("submenu")) {
          $("ul", $(this).parents("ul:first")).slideUp(350);
          $("a", $(this).parents("ul:first")).removeClass("submenu");
          $(this).next("ul").slideDown(350);
          $(this).addClass("submenu");
        } else if ($(this).hasClass("submenu")) {
          $(this).removeClass("submenu");
          $(this).next("ul").slideUp(350);
=======
      $('.main-nav a').on('click', function (e) {
        if ($(this).parent().hasClass('has-submenu')) {
          e.preventDefault();
        }
        if (!$(this).hasClass('submenu')) {
          $('ul', $(this).parents('ul:first')).slideUp(350);
          $('a', $(this).parents('ul:first')).removeClass('submenu');
          $(this).next('ul').slideDown(350);
          $(this).addClass('submenu');
        } else if ($(this).hasClass('submenu')) {
          $(this).removeClass('submenu');
          $(this).next('ul').slideUp(350);
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
        }
      });
      //$('.main-nav li.has-submenu a.active').parents('li:last').children('a:first').addClass('active').trigger('click');
    }

    // Sidebar Initiate
    init();
  }

  // Textarea Text Count

  var maxLength = 100;
<<<<<<< HEAD
  $("#review_desc").on("keyup change", function () {
    var length = $(this).val().length;
    length = maxLength - length;
    $("#chars").text(length);
=======
  $('#review_desc').on('keyup change', function () {
    var length = $(this).val().length;
    length = maxLength - length;
    $('#chars').text(length);
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
  });

  // Select 2

<<<<<<< HEAD
  if ($(".select").length > 0) {
    $(".select").select2({
      minimumResultsForSearch: -1,
      width: "100%",
=======
  if ($('.select').length > 0) {
    $('.select').select2({
      minimumResultsForSearch: -1,
      width: '100%',
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    });
  }

  // Date Time Picker

<<<<<<< HEAD
  if ($(".datetimepicker").length > 0) {
    $(".datetimepicker").datetimepicker({
      format: "DD/MM/YYYY",
      icons: {
        up: "fas fa-chevron-up",
        down: "fas fa-chevron-down",
        next: "fas fa-chevron-right",
        previous: "fas fa-chevron-left",
=======
  if ($('.datetimepicker').length > 0) {
    $('.datetimepicker').datetimepicker({
      format: 'DD/MM/YYYY',
      icons: {
        up: 'fas fa-chevron-up',
        down: 'fas fa-chevron-down',
        next: 'fas fa-chevron-right',
        previous: 'fas fa-chevron-left',
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      },
    });
  }

  // Fancybox Gallery

<<<<<<< HEAD
  if ($(".clinic-gallery a").length > 0) {
    $(".clinic-gallery a").fancybox({
      buttons: ["thumbs", "close"],
=======
  if ($('.clinic-gallery a').length > 0) {
    $('.clinic-gallery a').fancybox({
      buttons: ['thumbs', 'close'],
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    });
  }

  // Floating Label

<<<<<<< HEAD
  if ($(".floating").length > 0) {
    $(".floating")
      .on("focus blur", function (e) {
        $(this)
          .parents(".form-focus")
          .toggleClass("focused", e.type === "focus" || this.value.length > 0);
      })
      .trigger("blur");
=======
  if ($('.floating').length > 0) {
    $('.floating')
      .on('focus blur', function (e) {
        $(this)
          .parents('.form-focus')
          .toggleClass('focused', e.type === 'focus' || this.value.length > 0);
      })
      .trigger('blur');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
  }

  // Mobile menu sidebar overlay

<<<<<<< HEAD
  $("body").append('<div class="sidebar-overlay"></div>');
  $(document).on("click", "#mobile_btn", function () {
    $("main-wrapper").toggleClass("slide-nav");
    $(".sidebar-overlay").toggleClass("opened");
    $("html").addClass("menu-opened");
    return false;
  });

  $(document).on("click", ".sidebar-overlay", function () {
    $("html").removeClass("menu-opened");
    $(this).removeClass("opened");
    $("main-wrapper").removeClass("slide-nav");
  });

  $(document).on("click", "#menu_close", function () {
    $("html").removeClass("menu-opened");
    $(".sidebar-overlay").removeClass("opened");
    $("main-wrapper").removeClass("slide-nav");
=======
  $('body').append('<div class="sidebar-overlay"></div>');
  $(document).on('click', '#mobile_btn', function () {
    $('main-wrapper').toggleClass('slide-nav');
    $('.sidebar-overlay').toggleClass('opened');
    $('html').addClass('menu-opened');
    return false;
  });

  $(document).on('click', '.sidebar-overlay', function () {
    $('html').removeClass('menu-opened');
    $(this).removeClass('opened');
    $('main-wrapper').removeClass('slide-nav');
  });

  $(document).on('click', '#menu_close', function () {
    $('html').removeClass('menu-opened');
    $('.sidebar-overlay').removeClass('opened');
    $('main-wrapper').removeClass('slide-nav');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
  });

  // Mobile Menu

  /*if($(window).width() <= 991){
		mobileSidebar();
	} else {
		$('html').removeClass('menu-opened');
	}*/

  /*function mobileSidebar() {
		$('.main-nav a').on('click', function(e) {
			$('.dropdown-menu').each(function() {
			  if($(this).hasClass('show')) {
				  $(this).slideUp(350);
			  }
			});
			if(!$(this).next('.dropdown-menu').hasClass('show')) {
				$(this).next('.dropdown-menu').slideDown(350);
			}

		});
	}*/

  // Tooltip

  if ($('[data-toggle="tooltip"]').length > 0) {
    $('[data-toggle="tooltip"]').tooltip();
  }

  // Add More Hours

<<<<<<< HEAD
  $(".hours-info").on("click", ".trash", function () {
    $(this).closest(".hours-cont").remove();
    return false;
  });

  $(".add-hours").on("click", function () {
=======
  $('.hours-info').on('click', '.trash', function () {
    $(this).closest('.hours-cont').remove();
    return false;
  });

  $('.add-hours').on('click', function () {
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    var hourscontent =
      '<div class="row form-row hours-cont">' +
      '<div class="col-12 col-md-10">' +
      '<div class="row form-row">' +
      '<div class="col-12 col-md-6">' +
      '<div class="form-group">' +
<<<<<<< HEAD
      "<label>Start Time</label>" +
      '<select class="form-control">' +
      "<option>-</option>" +
      "<option>12.00 am</option>" +
      "<option>12.30 am</option>" +
      "<option>1.00 am</option>" +
      "<option>1.30 am</option>" +
      "</select>" +
      "</div>" +
      "</div>" +
      '<div class="col-12 col-md-6">' +
      '<div class="form-group">' +
      "<label>End Time</label>" +
      '<select class="form-control">' +
      "<option>-</option>" +
      "<option>12.00 am</option>" +
      "<option>12.30 am</option>" +
      "<option>1.00 am</option>" +
      "<option>1.30 am</option>" +
      "</select>" +
      "</div>" +
      "</div>" +
      "</div>" +
      "</div>" +
      '<div class="col-12 col-md-2"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
      "</div>";

    $(".hours-info").append(hourscontent);
=======
      '<label>Start Time</label>' +
      '<select class="form-control">' +
      '<option>-</option>' +
      '<option>12.00 am</option>' +
      '<option>12.30 am</option>' +
      '<option>1.00 am</option>' +
      '<option>1.30 am</option>' +
      '</select>' +
      '</div>' +
      '</div>' +
      '<div class="col-12 col-md-6">' +
      '<div class="form-group">' +
      '<label>End Time</label>' +
      '<select class="form-control">' +
      '<option>-</option>' +
      '<option>12.00 am</option>' +
      '<option>12.30 am</option>' +
      '<option>1.00 am</option>' +
      '<option>1.30 am</option>' +
      '</select>' +
      '</div>' +
      '</div>' +
      '</div>' +
      '</div>' +
      '<div class="col-12 col-md-2"><label class="d-md-block d-sm-none d-none">&nbsp;</label><a href="#" class="btn btn-danger trash"><i class="far fa-trash-alt"></i></a></div>' +
      '</div>';

    $('.hours-info').append(hourscontent);
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    return false;
  });

  // Content div min height set

  function resizeInnerDiv() {
    var height = $(window).height();
<<<<<<< HEAD
    var header_height = $(".header").height();
    var footer_height = $(".footer").height();
    var setheight = height - header_height;
    var trueheight = setheight - footer_height;
    $(".content").css("min-height", trueheight);
  }

  if ($(".content").length > 0) {
=======
    var header_height = $('.header').height();
    var footer_height = $('.footer').height();
    var setheight = height - header_height;
    var trueheight = setheight - footer_height;
    $('.content').css('min-height', trueheight);
  }

  if ($('.content').length > 0) {
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    resizeInnerDiv();
  }

  $(window).resize(function () {
<<<<<<< HEAD
    if ($(".content").length > 0) {
=======
    if ($('.content').length > 0) {
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      resizeInnerDiv();
    }
    /*if($(window).width() <= 991){
			mobileSidebar();
		} else {
			$('html').removeClass('menu-opened');
		}*/
  });

  // Slick Slider

<<<<<<< HEAD
  if ($(".specialities-slider").length > 0) {
    $(".specialities-slider").slick({
=======
  if ($('.specialities-slider').length > 0) {
    $('.specialities-slider').slick({
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      dots: true,
      autoplay: true,
      infinite: true,
      variableWidth: true,
      prevArrow: false,
      nextArrow: false,
    });
  }

<<<<<<< HEAD
  $(".specialities-slider").on(
    "afterChange",
    function (event, slick, currentSlide) {
      var $dots = $(this).find(".slick-dots li");
=======
  $('.specialities-slider').on(
    'afterChange',
    function (event, slick, currentSlide) {
      var $dots = $(this).find('.slick-dots li');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      // $dots.hide();
      $dots.slice(0, Math.min(currentSlide + 1, 4)).show();
    }
  );

<<<<<<< HEAD
  if ($(".doctor-slider").length > 0) {
    $(".doctor-slider").slick({
      centerMode: true,
      centerPadding: "60px",
=======
  if ($('.doctor-slider').length > 0) {
    $('.doctor-slider').slick({
      centerMode: true,
      centerPadding: '60px',
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      slidesToShow: 4,
      dots: false,
      autoplay: true,
      infinite: true,
      variableWidth: true,
    });
  }
<<<<<<< HEAD
  if ($(".features-slider").length > 0) {
    $(".features-slider").slick({
=======
  if ($('.features-slider').length > 0) {
    $('.features-slider').slick({
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      dots: true,
      infinite: true,
      centerMode: true,
      slidesToShow: 3,
      speed: 500,
      variableWidth: true,
      arrows: false,
      autoplay: false,
      responsive: [
        {
          breakpoint: 992,
          settings: {
            slidesToShow: 1,
          },
        },
      ],
    });
  }

  // Date Time Picker

<<<<<<< HEAD
  if ($(".datepicker").length > 0) {
    $(".datepicker").datetimepicker({
      viewMode: "years",
      showTodayButton: true,
      format: "DD-MM-YYYY",
      // minDate:new Date(),
      widgetPositioning: {
        horizontal: "auto",
        vertical: "bottom",
=======
  if ($('.datepicker').length > 0) {
    $('.datepicker').datetimepicker({
      viewMode: 'years',
      showTodayButton: true,
      format: 'DD-MM-YYYY',
      // minDate:new Date(),
      widgetPositioning: {
        horizontal: 'auto',
        vertical: 'bottom',
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      },
    });
  }

  // Chat

<<<<<<< HEAD
  var chatAppTarget = $(".chat-window");
  (function () {
    if ($(window).width() > 991) chatAppTarget.removeClass("chat-slide");

    $(document).on(
      "click",
      ".chat-window .chat-users-list a.media",
      function () {
        if ($(window).width() <= 991) {
          chatAppTarget.addClass("chat-slide");
=======
  var chatAppTarget = $('.chat-window');
  (function () {
    if ($(window).width() > 991) chatAppTarget.removeClass('chat-slide');

    $(document).on(
      'click',
      '.chat-window .chat-users-list a.media',
      function () {
        if ($(window).width() <= 991) {
          chatAppTarget.addClass('chat-slide');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
        }
        return false;
      }
    );
<<<<<<< HEAD
    $(document).on("click", "#back_user_list", function () {
      if ($(window).width() <= 991) {
        chatAppTarget.removeClass("chat-slide");
=======
    $(document).on('click', '#back_user_list', function () {
      if ($(window).width() <= 991) {
        chatAppTarget.removeClass('chat-slide');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      }
      return false;
    });
  })();

  function changeFont(language) {
<<<<<<< HEAD
    if (language === "en") {
      $("body").css("font-family", "Poppins, sans-serif");
      // $("html").css("direction", "ltr");
    } else if (language === "ar") {
      $("body").css("font-family", "Cairo, sans-serif");
=======
    if (language === 'en') {
      $('body').css('font-family', 'Poppins, sans-serif');
      // $("html").css("direction", "ltr");
    } else if (language === 'ar') {
      $('body').css('font-family', 'Cairo, sans-serif');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      // $("html").css("direction", "rtl");
    }
  }

  function setLanguage(language) {
    $.ajax({
<<<<<<< HEAD
      url: "/set_language",
      type: "GET",
=======
      url: '/set_language',
      type: 'GET',
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      data: { language: language },
      success: function () {
        changeFont(language);
        location.reload();
      },
    });
  }

<<<<<<< HEAD
  var currentLang = $("html").attr("lang");

  changeFont(currentLang);
  $("#language-select .dropdown-item").on("click", function () {
    var language = $(this).data("lang");
    setLanguage(language);
    var dir = language == "ar" ? "rtl" : "ltr";
    $("#calendar").fullCalendar("option", {
=======
  var currentLang = $('html').attr('lang');

  changeFont(currentLang);
  $('#language-select .dropdown-item').on('click', function () {
    var language = $(this).data('lang');
    setLanguage(language);
    var dir = language == 'ar' ? 'rtl' : 'ltr';
    $('#calendar').fullCalendar('option', {
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      locale: language,
      dir: dir,
    });
  });

  $(window).scroll();
  //   $(".alert")
  //     .fadeTo(2000, 500)
  //     .slideUp(1000, function () {
  //       $(".alert").slideUp(1000);
  //     });

  var monthNames = [
<<<<<<< HEAD
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  var dayNames = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
=======
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];
  var dayNames = [
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
  ];

  var newDatecal = new Date();
  newDatecal.setDate(newDatecal.getDate());

  setInterval(function () {
    var hours = new Date().getHours();
<<<<<<< HEAD
    $(".hour").html((hours < 10 ? "0" : "") + hours);
    var seconds = new Date().getSeconds();
    $(".second").html((seconds < 10 ? "0" : "") + seconds);
    var minutes = new Date().getMinutes();
    $(".minute").html((minutes < 10 ? "0" : "") + minutes);

    $(".month span,.month2 span").text(monthNames[newDatecal.getMonth()]);
    $(".date span,.date2 span").text(newDatecal.getDate());
    $(".day span,.day2 span").text(dayNames[newDatecal.getDay()]);
    $(".year span").html(newDatecal.getFullYear());
=======
    $('.hour').html((hours < 10 ? '0' : '') + hours);
    var seconds = new Date().getSeconds();
    $('.second').html((seconds < 10 ? '0' : '') + seconds);
    var minutes = new Date().getMinutes();
    $('.minute').html((minutes < 10 ? '0' : '') + minutes);

    $('.month span,.month2 span').text(monthNames[newDatecal.getMonth()]);
    $('.date span,.date2 span').text(newDatecal.getDate());
    $('.day span,.day2 span').text(dayNames[newDatecal.getDay()]);
    $('.year span').html(newDatecal.getFullYear());
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
  }, 1000);
})(jQuery);

// select2
$(document).ready(function () {
<<<<<<< HEAD
  $(".doctor-select2").select2({
    containerCssClass: "doctor-select",
    width: "100%",
  });
  $(".location-select2").select2({
    containerCssClass: "location-select",
    width: "100%",
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const dateItems = document.querySelectorAll(".date-item");
  const timeslotsContainers = document.querySelectorAll(".timeslots");
  dateItems.forEach((item, index) => {
    item.addEventListener("click", () => {
      dateItems.forEach((i) =>
        i.querySelector("h6").classList.remove("active")
      );
      timeslotsContainers.forEach((c) => c.classList.remove("active"));
      item.querySelector("h6").classList.add("active");
      dateItems.forEach((i) => i.classList.remove("active"));
      timeslotsContainers.forEach((c) => c.classList.remove("active"));
      item.classList.add("active");
      timeslotsContainers[index].classList.add("active");
=======
  $('.doctor-select2').select2({
    containerCssClass: 'doctor-select',
    width: '100%',
  });
  $('.location-select2').select2({
    containerCssClass: 'location-select',
    width: '100%',
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const dateItems = document.querySelectorAll('.date-item');
  const timeslotsContainers = document.querySelectorAll('.timeslots');
  dateItems.forEach((item, index) => {
    item.addEventListener('click', () => {
      dateItems.forEach((i) =>
        i.querySelector('h6').classList.remove('active')
      );
      timeslotsContainers.forEach((c) => c.classList.remove('active'));
      item.querySelector('h6').classList.add('active');
      dateItems.forEach((i) => i.classList.remove('active'));
      timeslotsContainers.forEach((c) => c.classList.remove('active'));
      item.classList.add('active');
      timeslotsContainers[index].classList.add('active');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    });
  });
});

<<<<<<< HEAD
$(document).on("change", ".Specialization", function () {
  if ($(this).is(":checked")) {
    $(this).prop("checked", true);
  } else {
    $(this).prop("checked", false);
=======
$(document).on('change', '.Specialization', function () {
  if ($(this).is(':checked')) {
    $(this).prop('checked', true);
  } else {
    $(this).prop('checked', false);
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
  }
});
$(function () {
  // Cache some selectors

<<<<<<< HEAD
  var clock = $("#clock"),
    ampm = clock.find(".ampm");

  // Map digits to their names (this will be an array)
  var digit_to_name = "zero one two three four five six seven eight nine".split(
    " "
=======
  var clock = $('#clock'),
    ampm = clock.find('.ampm');

  // Map digits to their names (this will be an array)
  var digit_to_name = 'zero one two three four five six seven eight nine'.split(
    ' '
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
  );

  // This object will hold the digit elements
  var digits = {};

  // Positions for the hours, minutes, and seconds
<<<<<<< HEAD
  var positions = ["h1", "h2", ":", "m1", "m2", ":", "s1", "s2"];

  // Generate the digits with the needed markup,
  // and add them to the clock
  var digit_holder = clock.find(".digits");

  $.each(positions, function () {
    if (this == ":") {
      digit_holder.append('<div class="dots">');
    } else {
      var pos = $("<div>");
=======
  var positions = ['h1', 'h2', ':', 'm1', 'm2', ':', 's1', 's2'];

  // Generate the digits with the needed markup,
  // and add them to the clock
  var digit_holder = clock.find('.digits');

  $.each(positions, function () {
    if (this == ':') {
      digit_holder.append('<div class="dots">');
    } else {
      var pos = $('<div>');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      for (var i = 1; i < 8; i++) {
        pos.append('<span class="d' + i + '">');
      }
      // Set the digits as key:value pairs in the digits object
      digits[this] = pos;
      // Add the digit elements to the page
      digit_holder.append(pos);
    }
  });

  // Add the weekday names
<<<<<<< HEAD
  var weekday_names = "SUN MON TUE WED THU FRI SAT".split(" "),
    weekday_holder = clock.find(".weekdays");

  $.each(weekday_names, function () {
    weekday_holder.append("<span>" + this + "</span>");
  });

  var weekdays = clock.find(".weekdays span");
=======
  var weekday_names = 'SUN MON TUE WED THU FRI SAT'.split(' '),
    weekday_holder = clock.find('.weekdays');

  $.each(weekday_names, function () {
    weekday_holder.append('<span>' + this + '</span>');
  });

  var weekdays = clock.find('.weekdays span');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97

  // Run a timer every second and update the clock
  (function update_time() {
    // Use moment.js to output the current time as a string
    // hh is for the hours in 12-hour format,
    // mm - minutes, ss-seconds (all with leading zeroes),
    // d is for day of week and A is for AM/PM
<<<<<<< HEAD
    var now = moment().format("hhmmssdA");

    digits.h1.attr("class", digit_to_name[now[0]]);
    digits.h2.attr("class", digit_to_name[now[1]]);
    digits.m1.attr("class", digit_to_name[now[2]]);
    digits.m2.attr("class", digit_to_name[now[3]]);
    digits.s1.attr("class", digit_to_name[now[4]]);
    digits.s2.attr("class", digit_to_name[now[5]]);
=======
    var now = moment().format('hhmmssdA');

    digits.h1.attr('class', digit_to_name[now[0]]);
    digits.h2.attr('class', digit_to_name[now[1]]);
    digits.m1.attr('class', digit_to_name[now[2]]);
    digits.m2.attr('class', digit_to_name[now[3]]);
    digits.s1.attr('class', digit_to_name[now[4]]);
    digits.s2.attr('class', digit_to_name[now[5]]);
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97

    // Directly use the day of the week from moment.js
    var dow = now[6];

    // Mark the active day of the week
<<<<<<< HEAD
    weekdays.removeClass("active").eq(dow).addClass("active");
=======
    weekdays.removeClass('active').eq(dow).addClass('active');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97

    // Set the am/pm text:
    ampm.text(now[7] + now[8]);

    // Schedule this function to be run again in 1 sec
    setTimeout(update_time, 1000);
  })();
});

<<<<<<< HEAD
const timeslots = document.querySelectorAll(".timeslot");
if (timeslots) {
  timeslots.forEach((slot) => {
    slot.addEventListener("click", () => {
      timeslots.forEach((s) => s.classList.remove("active"));
      slot.classList.add("active");
      slot.querySelector("input[type='radio']").checked = true;
    });
  });
  var continueButton = document.getElementById("continue-button");
  if (continueButton) {
    document
      .getElementById("continue-button")
      .addEventListener("click", function (event) {
=======
const timeslots = document.querySelectorAll('.timeslot');
if (timeslots) {
  timeslots.forEach((slot) => {
    slot.addEventListener('click', () => {
      timeslots.forEach((s) => s.classList.remove('active'));
      slot.classList.add('active');
      slot.querySelector("input[type='radio']").checked = true;
    });
  });
  var continueButton = document.getElementById('continue-button');
  if (continueButton) {
    document
      .getElementById('continue-button')
      .addEventListener('click', function (event) {
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
        var selectedTimeslot = document.querySelector(
          'input[name="timeslot"]:checked'
        );
        if (!selectedTimeslot) {
<<<<<<< HEAD
          document.getElementById("warning-message").style.display = "block";
        } else {
          document.getElementById("warning-message").style.display = "none";
          document.getElementById("appointment-form").submit();
=======
          document.getElementById('warning-message').style.display = 'block';
        } else {
          document.getElementById('warning-message').style.display = 'none';
          document.getElementById('appointment-form').submit();
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
        }
      });
  }
  AOS.init();

  $(window).scroll(function () {
    if ($(this).scrollTop() > 20) {
<<<<<<< HEAD
      $("#backToTop").fadeIn();
    } else {
      $("#backToTop").fadeOut();
=======
      $('#backToTop').fadeIn();
    } else {
      $('#backToTop').fadeOut();
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    }
  });

  // Click event to scroll to top
<<<<<<< HEAD
  $("#backToTop").click(function () {
    $("html, body").animate({ scrollTop: 0 }, "fast");
=======
  $('#backToTop').click(function () {
    $('html, body').animate({ scrollTop: 0 }, 'fast');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    return false;
  });
}

// view all notifications (delete and mark as read) to be continued...
$(document).ready(function () {
<<<<<<< HEAD
  let unreadCount = parseInt($("#notification-count").text(), 10);

  $(".mark-read-btn").on("click", function () {
    const notificationId = $(this).data("id");
    console.log("Notification ID:", notificationId);
    $.ajax({
      type: "POST",
      url: "/mark_as_read",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": $('meta[name="csrf-token"]').attr("content"),
=======
  let unreadCount = parseInt($('#notification-count').text(), 10);

  $('.mark-read-btn').on('click', function () {
    const notificationId = $(this).data('id');
    console.log('Notification ID:', notificationId);
    $.ajax({
      type: 'POST',
      url: '/mark_as_read',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'),
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      },
      data: {
        notification_id: notificationId,
      },
      success: function (data) {
<<<<<<< HEAD
        console.log("AJAX request successful", data);

        if (data.message === "Notification marked as read") {
          const notificationRow = $(this).closest("tr");
          if (notificationRow.length) {
            notificationRow.removeClass("unread-notification");
            $("#read-notifications-body").append(notificationRow);
            notificationRow.find(".mark-read-btn").remove();
            notificationRow
              .find(".delete-btn")
              .removeClass("bg-success-light")
              .addClass("bg-danger-light");
            notificationRow
              .find(".delete-btn i")
              .removeClass("fa-check")
              .addClass("fa-times");
            notificationRow
              .find(".delete-btn")
=======
        console.log('AJAX request successful', data);

        if (data.message === 'Notification marked as read') {
          const notificationRow = $(this).closest('tr');
          if (notificationRow.length) {
            notificationRow.removeClass('unread-notification');
            $('#read-notifications-body').append(notificationRow);
            notificationRow.find('.mark-read-btn').remove();
            notificationRow
              .find('.delete-btn')
              .removeClass('bg-success-light')
              .addClass('bg-danger-light');
            notificationRow
              .find('.delete-btn i')
              .removeClass('fa-check')
              .addClass('fa-times');
            notificationRow
              .find('.delete-btn')
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
              .html('<i class="fas fa-times"></i> Delete');

            unreadCount -= 1;
            updateNotificationCount();
          } else {
<<<<<<< HEAD
            console.error("Notification row not found.");
          }
        } else {
          console.error("Error marking notification as read:", data.message);
        }
      }.bind(this),
      error: function (xhr, status, error) {
        console.error("AJAX request failed with status:", status);
        console.error("Response text:", xhr.responseText);
        console.error("Error:", error);
=======
            console.error('Notification row not found.');
          }
        } else {
          console.error('Error marking notification as read:', data.message);
        }
      }.bind(this),
      error: function (xhr, status, error) {
        console.error('AJAX request failed with status:', status);
        console.error('Response text:', xhr.responseText);
        console.error('Error:', error);
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      },
    });
  });

<<<<<<< HEAD
  $(".delete-btn").on("click", function () {
    const notificationId = $(this).data("id");
    console.log("Notification ID:", notificationId);
    $.ajax({
      type: "POST",
      url: "/delete_notification",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": $('meta[name="csrf-token"]').attr("content"),
=======
  $('.delete-btn').on('click', function () {
    const notificationId = $(this).data('id');
    console.log('Notification ID:', notificationId);
    $.ajax({
      type: 'POST',
      url: '/delete_notification',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'),
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      },
      data: {
        notification_id: notificationId,
      },
      success: function (data) {
<<<<<<< HEAD
        if (data.message === "Notification deleted") {
          const notificationRow = $(this).closest("tr");
          if (notificationRow.hasClass("unread-notification")) {
=======
        if (data.message === 'Notification deleted') {
          const notificationRow = $(this).closest('tr');
          if (notificationRow.hasClass('unread-notification')) {
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
            unreadCount -= 1;
            updateNotificationCount();
          }
          notificationRow.remove();
        } else {
<<<<<<< HEAD
          console.error("Error deleting notification:", data.message);
        }
      }.bind(this),
      error: function (xhr, status, error) {
        console.error("AJAX request failed with status:", status);
        console.error("Response text:", xhr.responseText);
        console.error("Error:", error);
=======
          console.error('Error deleting notification:', data.message);
        }
      }.bind(this),
      error: function (xhr, status, error) {
        console.error('AJAX request failed with status:', status);
        console.error('Response text:', xhr.responseText);
        console.error('Error:', error);
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
      },
    });
  });

  function updateNotificationCount() {
<<<<<<< HEAD
    $("#notification-count").text(unreadCount);
    if (unreadCount === 0) {
      $("#notification-count").css("display", "inline").text("0");
=======
    $('#notification-count').text(unreadCount);
    if (unreadCount === 0) {
      $('#notification-count').css('display', 'inline').text('0');
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    }
  }
});

// update patient profile
<<<<<<< HEAD
$("#patientForm").on("submit", function (event) {
=======
$('#patientForm').on('submit', function (event) {
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
  event.preventDefault();

  let formData = new FormData(this);

  $.ajax({
<<<<<<< HEAD
    url: "/patient_setting",
    type: "PUT",
=======
    url: '/patient_setting',
    type: 'PUT',
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    data: formData,
    processData: false,
    contentType: false,
    headers: {
<<<<<<< HEAD
      "X-CSRFToken": "{{ form.csrf_token._value() }}",
    },
    success: function (data) {
      if (data.status === "success") {
=======
      'X-CSRFToken': '{{ form.csrf_token._value() }}',
    },
    success: function (data) {
      if (data.status === 'success') {
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
        location.reload();
      } else if (data.errors) {
        $.each(data.errors, function (field, error) {
          console.log(`Error in ${field}: ${error}`);
        });
      } else {
        console.log(data.message);
      }
    },
    error: function (xhr, status, error) {
<<<<<<< HEAD
      console.error("Error:", error);
=======
      console.error('Error:', error);
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
    },
  });
});
$(document).ready(function () {
<<<<<<< HEAD
  $("#add-more-item").click(function () {
    // Clone the last row
    var newRow = $("#items-container tr:last").clone();

    // Clear the values of all input elements in the cloned row
    newRow.find("input").val("");

    // Clear the values of any select elements if they exist
    newRow.find("select").val("");

    // Update the names of the input elements in the cloned row
    newRow.find("input, select").each(function () {
      var currentName = $(this).attr("name");
      var newName = currentName.replace(/items-\d+-/g, function (match) {
        var index = parseInt(match.match(/\d+/)) + 1;
        return "items-" + index + "-";
      });
      $(this).attr("name", newName);
    });

    // Append the cloned row to the container
    console.log(newRow)
    $("#items-container").append(newRow);
  });

  // Remove a row when the trash button is clicked
  $("#items-container").on("click", ".trash", function (e) {
    e.preventDefault();
    $(this).closest("tr").remove();
  });
});
=======
  $('#add-more-item').click(function () {
    // Clone the last row
    var newRow = $('#items-container tr:last').clone();

    // Clear the values of all input elements in the cloned row
    newRow.find('input').val('');

    // Clear the values of any select elements if they exist
    newRow.find('select').val('');

    // Update the names of the input elements in the cloned row
    newRow.find('input, select').each(function () {
      var currentName = $(this).attr('name');
      var newName = currentName.replace(/items-\d+-/g, function (match) {
        var index = parseInt(match.match(/\d+/)) + 1;
        return 'items-' + index + '-';
      });
      $(this).attr('name', newName);
    });

    // Append the cloned row to the container
    console.log(newRow);
    $('#items-container').append(newRow);
  });

  // Remove a row when the trash button is clicked
  $('#items-container').on('click', '.trash', function (e) {
    e.preventDefault();
    $(this).closest('tr').remove();
  });
});

// update appointment status
$(document).ready(function () {
  $('.status-dropdown .dropdown-item').click(function () {
    const newStatus = $(this).data('status');
    const dropdownButton = $(this)
      .closest('.status-dropdown')
      .find('.status-badge');
    const appointmentId = dropdownButton.data('appointment-id');
    const csrfToken = $('meta[name="csrf-token"]').attr('content');

    console.log('Sending AJAX request with:', {
      appointment_id: appointmentId,
      new_status: newStatus,
      csrf_token: csrfToken,
    });

    $.ajax({
      url: '/update_appointment_status',
      method: 'POST',
      data: {
        appointment_id: appointmentId,
        new_status: newStatus,
        csrf_token: csrfToken,
      },
      success: function (response) {
        if (response.success) {
          const badge = $(
            `.status-badge[data-appointment-id="${appointmentId}"]`
          );
          badge
            .text(newStatus)
            .removeClass('bg-warning-light bg-success-light bg-danger-light')
            .addClass(`bg-${getStatusColor(newStatus)}-light`);
        } else {
          alert('Failed to update status. Please try again.');
        }
      },
      error: function (xhr, status, error) {
        alert('An error occurred. Please try again.');
        console.error('Error:', status, error);
      },
    });
  });
});

function getStatusColor(status) {
  switch (status) {
    case 'Pending':
      return 'warning';
    case 'Confirmed':
      return 'success';
    case 'Cancelled':
      return 'danger';
    default:
      return 'warning';
  }
}
>>>>>>> b54daea9fe5eb616c0bdbd1a608e3b2206e33a97
