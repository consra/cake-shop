# Cake Shop
Cake Shop Online App

# Architectural Diagram

# Services
- MySQL Database
    - Consists of a series of tables that hold customer data, orders, products, list with the main ingredients of each product, as well as a table in which the customer login session is saved and a table where the messages are logged.
    - Database Diagram
- Business Logic Server
    - Exposes numerous endpoints used by the Web application. For each table there are two main endpoints - one for GET requests that select the elements from database and sends them in JSON format to the Web and one for POST requests that add the data received from the Web to the MySQL database. The server also exposes two endpoints one for login and one for logout.
    - Written in Python 3 with Flask.
- Frontend Server
    - Apache HTTP Server, Vanilla JavaScript, HTML, CSS.
    - The web application consists of following pages:
    - PRODUCTS - the page that displays the available products from the cake shop. 
    - INGREDIENTS - the page that shows the main ingredients contained in the exposed products. 
    - ORDERS - the page that displays the orders placed - an admin user can see all the orders made by all users in the system.
    - REPORTS - the page contains the application reports.
    - GRAPHICS - the page contains the application graphics.
    - ABOUT - the page that displays the application documentation.
- Monitoring Service - Grafana
    - The service will retrieve the information from the InfluxDB database and create statistics that will present general information about the processed orders.
    - In the below image the service monitors the number of orders processed within 12 hours.
- InfluxDB Database
    - The primary key will be a timestamp to be able to perform statistics for certain periods of time.
    - A record in the database has the following structure:
- Adapter
    - The purpose of the adapter is to retrieve the data from the MySQL database, process and store them in the InfluxDB database. The inserted data will be used by the monitoring service.
    - Written in Python 3.
