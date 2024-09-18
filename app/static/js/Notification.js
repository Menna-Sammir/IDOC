document.addEventListener("DOMContentLoaded", (event) => {
  if (clinic_id) {
    console.log("Rendered clinic_id:", clinic_id);
    if (!clinic_id) {
      console.error(
        "Clinic ID is missing. Cannot establish WebSocket connection."
      );
      return;
    }
    console.log("Connecting with clinic_id:", clinic_id);

    var socket = io.connect("http://localhost:5000", {
      query: "clinic_id=" + clinic_id,
      transports: ["websocket", "polling"],
    });

    socket.on("connected", function (msg) {
      console.log(msg.message);
    });

    socket.on("appointment_notification", function (data) {
      console.log("Appointment notification:", data);
      addNotification(data, true);
    });

    socket.on("disconnected", function (msg) {
      console.log(msg.message);
    });

    function addNotification(data, store = false) {
      var notificationList = document.getElementById("notification-list");
      var notificationCount = document.getElementById("notification-count");

      var newNotification = document.createElement("li");
      newNotification.classList.add("notification-message");

      var currentTime = new Date();
      var formattedTime = currentTime.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
      var notificationContent = `
        <a href="#">
          <div class="media">
            <span class="avatar avatar-sm">
              <img class="avatar-img rounded-circle" alt="User Image" src="assets/img/doctors/doctor-thumb-01.jpg">
            </span>
            <div class="media-body">
              <p class="noti-details">
                <span class="noti-title">Dr. ${data.doctor}</span> has a new appointment on
                <span class="noti-title">${data.date} at ${data.time}</span>
              </p>
              <p class="noti-time">
                <span class="notification-time">${formattedTime}</span>
              </p>
            </div>
          </div>
        </a>
      `;

      newNotification.innerHTML = notificationContent;
      notificationList.prepend(newNotification);

      var currentCount = parseInt(notificationCount.textContent);
      notificationCount.textContent = currentCount + 1;

      playNotificationSound();
      if (store) {
        storeNotification(data);
      }
    }

    function playNotificationSound() {
      var audio = document.getElementById("notification-sound");
      if (audio) {
        audio.play().catch((error) => {
          console.error("Error playing audio:", error);
        });
      } else {
        console.error("Audio element not found");
      }
    }

    function storeNotification(data) {
      var notifications =
        JSON.parse(localStorage.getItem("notifications")) || [];
      notifications.unshift(data);
      localStorage.setItem("notifications", JSON.stringify(notifications));
    }

    function loadNotifications() {
      var notifications =
        JSON.parse(localStorage.getItem("notifications")) || [];
      notifications.forEach((notification) => {
        addNotification(notification, true);
      });
    }

    document
      .getElementById("clear-all-notifications")
      .addEventListener("click", function () {
        clearAllNotifications();
      });

    //  function fetchNotifications() {
    //   fetch(`/notifications?clinic_id=${clinic_id}`)
    //     .then((response) => {
    //       if (!response.ok) {
    //         throw new Error('Network response was not ok');
    //       }
    //       return response.json();
    //     })
    //     .then((data) => {
    //       data.forEach((notification) =>
    //         addNotification(notification, false)
    //        );
    //     })
    //     .catch((error) =>
    //       console.error('Error fetching notifications:', error)
    //     );
    // }

    function clearAllNotifications() {
      var notificationList = document.getElementById("notification-list");
      var notificationCount = document.getElementById("notification-count");
      if (notificationList && notificationCount) {
        notificationList.innerHTML = "";
        notificationCount.textContent = "0";
        localStorage.removeItem("notifications");
      }
    }
    socket.on("notification_update", function (data) {
      updateNotificationCount(data.count);
    });

    loadNotifications();
    //fetchNotifications();
  }
});
