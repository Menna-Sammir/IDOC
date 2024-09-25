# IDOC - Intelligent Clinic Organizer and Controller

IDOC is an intelligent application designed to facilitate appointment scheduling with doctors and clinics. This project aims to provide users with a user-friendly interface for managing appointments and accessing healthcare services efficiently.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **User Authentication**: Secure login and registration for patients and healthcare providers.
- **Appointment Scheduling**: Easily book, reschedule, or cancel appointments with doctors and clinics.
- **Doctor and Clinic Search**: Search for doctors and clinics based on specialty, location, and availability.
- **Patient Dashboard**: View upcoming appointments, medical history, and manage personal information.
- **Notifications**: Receive reminders and notifications for upcoming appointments.

## Technologies Used

- **Frontend**: Jinja - A templating engine for Python to create dynamic web pages.
- **Backend**: Flask - A micro web framework for Python.
- **Database**: MySQL - A popular open-source relational database for storing appointment and user data.
- **ORM**: SQLAlchemy - A Python SQL toolkit and Object-Relational Mapping (ORM) system.
- **Styling**: Bootstrap - A front-end framework for developing responsive web applications.

## Installation

To set up the IDOC project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Menna-Sammir/IDOC.git
   ```
   
2- Navigate to the project directory

```bash
cd idoc

```

3- Create a virtual environment

```bash
python3 -m venv venv

```

4- Activate the virtual environment

```bash
source venv/bin/activate

```

5- Install the dependencies

```bash
pip install -r requirements.txt

```

6- Set up the database
```bash
flask db init
flask db migrate
flask db upgrade

```

7- Run the application
```bash
python3 app.py

```
# Usage
Search for Doctors:

Use the search functionality to find doctors based on specialization, location, and availability.
Book appointments directly through the platform.

Clinic Dashboard:

Clinics can view and manage their appointments.
Real-time notifications for new appointments.



@Contributing
Contributions are welcome! If you'd like to contribute to IDOC, please follow these steps:

1- Fork the repository.
2- Create a new branch (git checkout -b feature/YourFeature).
3- Make your changes and commit them (git commit -m 'Add some feature').
4- Push to the branch (git push origin feature/YourFeature).
5- Open a pull request.




## Authors

- [@Menna-Sammir](https://github.com/Menna-Sammir)

- [@fatmasoly](https://github.com/fatmasoly)

- [@adhamelsayed2000](https://github.com/adhamelsayed2000)


![Home Page](https://github.com/manonaSamir/IDOC/blob/main/app/static/images/screencapture-localhost-5000-2024-06-12-14_02_53.png)
