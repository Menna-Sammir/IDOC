const months = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
];

const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

let date = new Date();

function getCurrentDate(element, asString) {
  if (element) {
      if (asString) {
          return element.textContent = weekdays[date.getDay()] + ', ' + date.getDate() + " " + months[date.getMonth()] + " " + date.getFullYear();
      }
      return element.value = date.toISOString().substr(0, 10);
  }
  return date;
}

function generateWeekCalendar() {
  const calendar = document.getElementById('calendar');
  if (calendar) {
      calendar.remove();
  }

  const table = document.createElement("table");
  table.id = "calendar";

  const trHeader = document.createElement('tr');
  trHeader.className = 'weekends';

  weekdays.map(week => {
      const th = document.createElement('th');
      const w = document.createTextNode(week.substring(0, 3));
      th.appendChild(w);
      trHeader.appendChild(th);
  });

  table.appendChild(trHeader);

  const startOfWeek = getStartOfWeek(date);

  let tr = document.createElement("tr");
  for (let i = 0; i < 7; i++) {
      let td = document.createElement('td');
      const day = new Date(startOfWeek);
      day.setDate(startOfWeek.getDate() + i);

      let btn = document.createElement('button');
      btn.className = "btn-day";
      btn.addEventListener('click', function () { changeDate(this, day) });

      const text = document.createTextNode(day.getDate());
      btn.appendChild(text);
      td.appendChild(btn);

      if (day.getDate() === date.getDate()) {
          btn.classList.add('active');
      }

      tr.appendChild(td);
  }

  table.appendChild(tr);

  const content = document.getElementById('table');
  content.appendChild(table);

  changeHeader(date);
  getCurrentDate(document.getElementById("currentDate"), true);
}

function getStartOfWeek(d) {
  const start = new Date(d);
  const day = start.getDay(); // Get current day of the week
  const diff = start.getDate() - day + (day === 0 ? -6 : 1); // Adjust to the start of the week (Monday)
  return new Date(start.setDate(diff));
}

function changeHeader(dateHeader) {
  const month = document.getElementById("month-header");
  if (month.childNodes[0]) {
      month.removeChild(month.childNodes[0]);
  }
  const headerMonth = document.createElement("h4");
  const textMonth = document.createTextNode(months[dateHeader.getMonth()].substring(0, 3) + " " + dateHeader.getFullYear());
  headerMonth.appendChild(textMonth);
  month.appendChild(headerMonth);
}

function changeDate(button, newDate) {
  date = newDate;
  generateWeekCalendar();
}

// Navigate to the next week
function nextWeek() {
  date.setDate(date.getDate() + 7);
  generateWeekCalendar();
}

// Navigate to the previous week
function prevWeek() {
  date.setDate(date.getDate() - 7);
  generateWeekCalendar();
}

document.onload = generateWeekCalendar(date);