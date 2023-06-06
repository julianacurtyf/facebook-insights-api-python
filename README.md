# facebook-api-master

This repository provides access to the Facebook Insights API. The Facebook Insights API allows developers to retrieve valuable data and metrics related to Facebook Campaigns, Adsets, and Ads, including user engagement, reach, impressions, and more. The code retrieves the data from the API and loads it into a MySQL database, allowing users to analyze and visualize the data as needed.


## Setup

To use this repository, please follow the steps below:

__1. Clone the repository to your local machine:__

```sh
$ git clone https://github.com/julianacurtyf/facebook-insights-api-python.git
$ cd facebook-insights-api-python
```

__2. Create a virtual environment to install the dependencies:__

```sh
$ pip install virtualenv
$ virtualenv2 --no-site-packages env
```

__3. Activate the virtual environment:__

- MacOS or Linux
```
$ source env/bin/activate
```
- Windows
```
$ .\env\Scripts\activate
```

__4. Install the required dependencies:__

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

__5. Configure the MySQL database settings:__

Open the database.py file in the root directory.
Update the following variables with your MySQL database information:
- DB_HOST: the host of your MySQL server (e.g., localhost)
- DB_PORT: the port number of your MySQL server (e.g., 3306)
- DB_USER: the username to connect to your MySQL server
- DB_PASSWORD: the password to connect to your MySQL server
- DB_NAME: the name of the MySQL database where you want to store the Facebook Insights data

__6. Obtain the necessary Facebook API credentials:__

Create a new Facebook app on the Facebook Developers platform.
Obtain the following credentials:
- APP_ID: the ID of your Facebook app (account id)
- APP_SECRET: the secret key of your Facebook app (Token)

__7. Run the main.py.__

With those informations in hand, it is now possible to r
