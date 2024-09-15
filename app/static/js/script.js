(function ($) {
  'use strict';

  // Stick Sidebar

  if ($(window).width() > 767) {
    if ($('.theiaStickySidebar').length > 0) {
      $('.theiaStickySidebar').theiaStickySidebar({
        // Settings
        additionalMarginTop: 30,
      });
    }
  }

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
      };
      reader.readAsDataURL(file);
    });
  });

  // Sidebar
  if ($(window).width() <= 991) {
    var Sidemenu = function () {
      this.$menuItem = $('.main-nav a');
    };

    function init() {
      var $this = Sidemenu;
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
        }
      });
      //$('.main-nav li.has-submenu a.active').parents('li:last').children('a:first').addClass('active').trigger('click');
    }

    // Sidebar Initiate
    init();
  }

  // Textarea Text Count

  var maxLength = 100;
  $('#review_desc').on('keyup change', function () {
    var length = $(this).val().length;
    length = maxLength - length;
    $('#chars').text(length);
  });

  // Select 2

  if ($('.select').length > 0) {
    $('.select').select2({
      minimumResultsForSearch: -1,
      width: '100%',
    });
  }

  // Date Time Picker

  if ($('.datetimepicker').length > 0) {
    $('.datetimepicker').datetimepicker({
      format: 'DD/MM/YYYY',
      icons: {
        up: 'fas fa-chevron-up',
        down: 'fas fa-chevron-down',
        next: 'fas fa-chevron-right',
        previous: 'fas fa-chevron-left',
      },
    });
  }

  // Fancybox Gallery

  if ($('.clinic-gallery a').length > 0) {
    $('.clinic-gallery a').fancybox({
      buttons: ['thumbs', 'close'],
    });
  }

  // Floating Label

  if ($('.floating').length > 0) {
    $('.floating')
      .on('focus blur', function (e) {
        $(this)
          .parents('.form-focus')
          .toggleClass('focused', e.type === 'focus' || this.value.length > 0);
      })
      .trigger('blur');
  }

  // Mobile menu sidebar overlay

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

  $('.hours-info').on('click', '.trash', function () {
    $(this).closest('.hours-cont').remove();
    return false;
  });

  $('.add-hours').on('click', function () {
    var hourscontent =
      '<div class="row form-row hours-cont">' +
      '<div class="col-12 col-md-10">' +
      '<div class="row form-row">' +
      '<div class="col-12 col-md-6">' +
      '<div class="form-group">' +
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
    return false;
  });

  // Content div min height set

  function resizeInnerDiv() {
    var height = $(window).height();
    var header_height = $('.header').height();
    var footer_height = $('.footer').height();
    var setheight = height - header_height;
    var trueheight = setheight - footer_height;
    $('.content').css('min-height', trueheight);
  }

  if ($('.content').length > 0) {
    resizeInnerDiv();
  }

  $(window).resize(function () {
    if ($('.content').length > 0) {
      resizeInnerDiv();
    }
    /*if($(window).width() <= 991){
			mobileSidebar();
		} else {
			$('html').removeClass('menu-opened');
		}*/
  });

  // Slick Slider

  if ($('.specialities-slider').length > 0) {
    $('.specialities-slider').slick({
      dots: true,
      autoplay: true,
      infinite: true,
      variableWidth: true,
      prevArrow: false,
      nextArrow: false,
    });
  }

  $('.specialities-slider').on(
    'afterChange',
    function (event, slick, currentSlide) {
      var $dots = $(this).find('.slick-dots li');
      // $dots.hide();
      $dots.slice(0, Math.min(currentSlide + 1, 4)).show();
    }
  );

  if ($('.doctor-slider').length > 0) {
    $('.doctor-slider').slick({
      centerMode: true,
      centerPadding: '60px',
      slidesToShow: 4,
      dots: false,
      autoplay: true,
      infinite: true,
      variableWidth: true,
    });
  }
  if ($('.features-slider').length > 0) {
    $('.features-slider').slick({
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

  if ($('.datepicker').length > 0) {
    $('.datepicker').datetimepicker({
      viewMode: 'years',
      showTodayButton: true,
      format: 'DD-MM-YYYY',
      // minDate:new Date(),
      widgetPositioning: {
        horizontal: 'auto',
        vertical: 'bottom',
      },
    });
  }

  // Chat

  var chatAppTarget = $('.chat-window');
  (function () {
    if ($(window).width() > 991) chatAppTarget.removeClass('chat-slide');

    $(document).on(
      'click',
      '.chat-window .chat-users-list a.media',
      function () {
        if ($(window).width() <= 991) {
          chatAppTarget.addClass('chat-slide');
        }
        return false;
      }
    );
    $(document).on('click', '#back_user_list', function () {
      if ($(window).width() <= 991) {
        chatAppTarget.removeClass('chat-slide');
      }
      return false;
    });
  })();

  function changeFont(language) {
    if (language === 'en') {
      $('body').css('font-family', 'Poppins, sans-serif');
      // $("html").css("direction", "ltr");
    } else if (language === 'ar') {
      $('body').css('font-family', 'Cairo, sans-serif');
      // $("html").css("direction", "rtl");
    }
  }

  function setLanguage(language) {
    $.ajax({
      url: '/set_language',
      type: 'GET',
      data: { language: language },
      success: function () {
        changeFont(language);
        location.reload();
      },
    });
  }

  var currentLang = $('html').attr('lang');

  changeFont(currentLang);
  $('#language-select .dropdown-item').on('click', function () {
    var language = $(this).data('lang');
    setLanguage(language);
    var dir = language == 'ar' ? 'rtl' : 'ltr';
    $('#calendar').fullCalendar('option', {
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
  ];

  var newDatecal = new Date();
  newDatecal.setDate(newDatecal.getDate());

  setInterval(function () {
    var hours = new Date().getHours();
    $('.hour').html((hours < 10 ? '0' : '') + hours);
    var seconds = new Date().getSeconds();
    $('.second').html((seconds < 10 ? '0' : '') + seconds);
    var minutes = new Date().getMinutes();
    $('.minute').html((minutes < 10 ? '0' : '') + minutes);

    $('.month span,.month2 span').text(monthNames[newDatecal.getMonth()]);
    $('.date span,.date2 span').text(newDatecal.getDate());
    $('.day span,.day2 span').text(dayNames[newDatecal.getDay()]);
    $('.year span').html(newDatecal.getFullYear());
  }, 1000);
})(jQuery);

// select2
$(document).ready(function () {
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
    });
  });
});

$(document).on('change', '.Specialization', function () {
  if ($(this).is(':checked')) {
    $(this).prop('checked', true);
  } else {
    $(this).prop('checked', false);
  }
});
$(function () {
  // Cache some selectors

  var clock = $('#clock'),
    ampm = clock.find('.ampm');

  // Map digits to their names (this will be an array)
  var digit_to_name = 'zero one two three four five six seven eight nine'.split(
    ' '
  );

  // This object will hold the digit elements
  var digits = {};

  // Positions for the hours, minutes, and seconds
  var positions = ['h1', 'h2', ':', 'm1', 'm2', ':', 's1', 's2'];

  // Generate the digits with the needed markup,
  // and add them to the clock
  var digit_holder = clock.find('.digits');

  $.each(positions, function () {
    if (this == ':') {
      digit_holder.append('<div class="dots">');
    } else {
      var pos = $('<div>');
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
  var weekday_names = 'SUN MON TUE WED THU FRI SAT'.split(' '),
    weekday_holder = clock.find('.weekdays');

  $.each(weekday_names, function () {
    weekday_holder.append('<span>' + this + '</span>');
  });

  var weekdays = clock.find('.weekdays span');

  // Run a timer every second and update the clock
  (function update_time() {
    // Use moment.js to output the current time as a string
    // hh is for the hours in 12-hour format,
    // mm - minutes, ss-seconds (all with leading zeroes),
    // d is for day of week and A is for AM/PM
    var now = moment().format('hhmmssdA');

    digits.h1.attr('class', digit_to_name[now[0]]);
    digits.h2.attr('class', digit_to_name[now[1]]);
    digits.m1.attr('class', digit_to_name[now[2]]);
    digits.m2.attr('class', digit_to_name[now[3]]);
    digits.s1.attr('class', digit_to_name[now[4]]);
    digits.s2.attr('class', digit_to_name[now[5]]);

    // Directly use the day of the week from moment.js
    var dow = now[6];

    // Mark the active day of the week
    weekdays.removeClass('active').eq(dow).addClass('active');

    // Set the am/pm text:
    ampm.text(now[7] + now[8]);

    // Schedule this function to be run again in 1 sec
    setTimeout(update_time, 1000);
  })();
});

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
        var selectedTimeslot = document.querySelector(
          'input[name="timeslot"]:checked'
        );
        if (!selectedTimeslot) {
          document.getElementById('warning-message').style.display = 'block';
        } else {
          document.getElementById('warning-message').style.display = 'none';
          document.getElementById('appointment-form').submit();
        }
      });
  }
  AOS.init();

  $(window).scroll(function () {
    if ($(this).scrollTop() > 20) {
      $('#backToTop').fadeIn();
    } else {
      $('#backToTop').fadeOut();
    }
  });

  // Click event to scroll to top
  $('#backToTop').click(function () {
    $('html, body').animate({ scrollTop: 0 }, 'fast');
    return false;
  });
}

// view all notifications (delete and mark as read) to be continued...
$(document).ready(function () {
  let unreadCount = parseInt($('#notification-count').text(), 10);

  $('.mark-read-btn').on('click', function (event) {
    event.preventDefault();

    const notificationId = $(this).data('id');
    console.log('Notification ID:', notificationId);

    const button = $(this);

    $.ajax({
      type: 'POST',
      url: `/mark_as_read/${notificationId}`,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'),
      },
      success: function (data) {
        console.log('AJAX request successful', data);

        if (data.success) {
          const notificationRow = button.closest('tr');
          if (notificationRow.length) {
            notificationRow.removeClass('unread-notification');
            $('#read-notifications-body').append(notificationRow);
            notificationRow.find('.mark-read-btn').remove();
            notificationRow
              .find('.delete-btn')
              .removeClass('bg-success-light')
              .addClass('bg-danger-light')
              .html('<i class="fas fa-times"></i> Delete');

            unreadCount -= 1;
            updateNotificationCount();
          } else {
            console.error('Notification row not found.');
          }
        } else {
          console.error('Error marking notification as read:', data.message);
        }
      },
      error: function (xhr, status, error) {
        console.error('AJAX request failed with status:', status);
        console.error('Response text:', xhr.responseText);
        console.error('Error:', error);
      },
    });
  });

  function updateNotificationCount() {
    $('#notification-count').text(unreadCount);
    if (unreadCount === 0) {
      $('#notification-count').css('display', 'inline').text('0');
    }
  }
});

// update patient profile
$('#patientForm').on('submit', function (event) {
  event.preventDefault();

  let formData = new FormData(this);

  $.ajax({
    url: '/patient_setting',
    type: 'PUT',
    data: formData,
    processData: false,
    contentType: false,
    headers: {
      'X-CSRFToken': '{{ form.csrf_token._value() }}',
    },
    success: function (data) {
      if (data.status === 'success') {
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
      console.error('Error:', error);
    },
  });
});

$(document).ready(function () {
  $('#add-more-item').click(function (e) {
    e.preventDefault();

    // Get the number of existing items
    var count = $('#items-container tr').length;

    // Clone the last item row
    var newItem = $('#items-container tr:last').clone();

    // Clear input values in the cloned row
    newItem.find('input:not([type="checkbox"])').val('');

    newItem.find('input[type="checkbox"]').prop('checked', false);

    // Update the name and id attributes for each form element in the new item row
    newItem.find('input, select, label').each(function () {
      var name = $(this).attr('name');
      if (name) {
        var newName = name.replace(/\d+/, count);
        $(this).attr('name', newName);
      }

      var id = $(this).attr('id');
      if (id) {
        var newId = id.replace(/\d+/, count);
        $(this).attr('id', newId);
      }

      var forAttr = $(this).attr('for');
      if (forAttr) {
        var newFor = forAttr.replace(/\d+/, count);
        $(this).attr('for', newFor);
      }
    });

    // Append the new item row to the items container
    $('#items-container').append(newItem);
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
    case 'Completed':
      return 'primary';
    default:
      return 'warning';
  }
}

document.addEventListener('DOMContentLoaded', function () {
  $('#add_medical_reports').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var appointmentId = button.data('appointment-id');
    var patientId = button.data('patient-id');
    var diagnosis = button.data('diagnosis');

    var modal = $(this);
    modal.find('#appointment_id').val(appointmentId);
    modal.find('#patient_id').val(patientId);
    modal.find('#modal_diagnosis').val(diagnosis);
  });
});

$(document).ready(function () {
  $('.print-btn').on('click', function () {
    var reportUrl = $(this).data('report-url');
    if (reportUrl) {
      var printWindow = window.open(reportUrl, '_blank');
      printWindow.onload = function () {
        printWindow.print();
      };
    } else {
      alert('No report available to print.');
    }
  });
});
