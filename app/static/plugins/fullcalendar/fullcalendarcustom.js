if ($("#calendar-appointment").length) {
  var currentLang = $("html").attr("lang");
  var dir = currentLang == "ar" ? "rtl" : "ltr";
  var CalendarApp = function () {
    this.$body = $("body");
    (this.$calendar = $("#calendar-appointment")),
      (this.$event = "#calendar-events div.calendar-events"),
      (this.$categoryForm = $("#add_new_event form")),
      (this.$extEvents = $("#calendar-events")),
      (this.$modal = $("#clinicMeet")),
      (this.$saveCategoryBtn = $(".save-category")),
      (this.$calendarObj = null);
  };

  function fetchAndUpdateCalendar(calendarApp) {
    $.ajax({
      url: "/getcaldata",
      method: "GET",
      success: function (data) {
        calendarApp.$calendarObj.fullCalendar("removeEvents");
        calendarApp.$calendarObj.fullCalendar(
          "addEventSource",
          data.appointment_events
        );
        calendarApp.$calendarObj.fullCalendar("refetchEvents");
      },
      error: function (error) {
        console.error("Error fetching data:", error);
      },
    });
  }

  (CalendarApp.prototype.enableDrag = function () {
    //init events
    $(this.$event).each(function () {
      // it doesn't need to have a start or end
      var eventObject = {
        title: $.trim($(this).text()), // use the element's text as the event title
      };
      // store the Event Object in the DOM element so we can get to it later
      $(this).data("eventObject", eventObject);
      // make the event draggable using jQuery UI
      $(this).draggable({
        zIndex: 999,
        revert: true, // will cause the event to go back to its
        revertDuration: 0, //  original position after the drag
      });
    });
  }),
    (CalendarApp.prototype.onEventClick = function (calEvent, jsEvent, view) {
      this.$modal.find(".modal-title").text("Edit Event");
      this.$modal.find(".modal-body").html(`
      <div class="card card-table px-4 py-2 mb-0">
        <div class="card-body text-left">
          <div class="p-1">
            <img class="img-fluid" src="${
              calEvent.img
            }" alt="User Image" width="80" style="border: 3px groove #85d8ff; border-radius: 50%;" />
          </div>
          <div class="p-1">
            <h5 class="mb-0">Doctor: Dr. ${calEvent.doctor}</h5>
          </div>
          <div class="p-1">
            <h5 class="mb-0">Patient: ${calEvent.patient}</h5>
          </div>
          <div class="p-1">
            <h5 class="mb-0">Time: ${calEvent.start.format("hh:mm A")}</h5>
          </div>
          <div class="p-1">
            <h5 class="mb-0">Cost: ${calEvent.cost}$</h5>
          </div>
        </div>
      </div>
    `);
      this.$modal.modal("show");
    }),
    /* Initializing */
    (CalendarApp.prototype.init = function () {
      var $this = this;
      this.enableDrag();
      $this.$calendarObj = $this.$calendar.fullCalendar({
        defaultView: "month",
        handleWindowResize: true,
        header: {
          left: "prev,next today",
          center: "title",
          right: "month,agendaDay",
        },
        slotDuration: "00:45:00",
        minTime: "08:00:00",
        maxTime: "19:00:00",
        eventLimit: true,
        views: {
          month: {
            eventLimit: 2,
          },
        },
        selectable: true,
        events: [],
        locale: currentLang,
        dir: dir,
        eventRender: function (event, element) {
          element.find(".fc-title").html(event.doctor);

          var html = '<img src="' + event.img + '" class="event-image">';

          html +=
            '<div class="ml-1 mt-2"><div class="fc-event-title d-block text-left"> Dr.' +
            event.doctor +
            '</div><p class="fc-event-title d-block text-muted m-0 text-left">' +
            event.patient +
            "</p></div>";
          element.find(".fc-content").append(html);
        },
        eventClick: function (calEvent, jsEvent, view) {
          $this.onEventClick(calEvent, jsEvent, view);
        },
      });
      fetchAndUpdateCalendar($this);
    }),
    ($.CalendarApp = new CalendarApp());
  $.CalendarApp.init();
}
// function changelocale(language){
