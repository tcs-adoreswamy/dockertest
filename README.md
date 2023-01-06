# Price-Simulation app

Streamlit based python application that generates pricing reports

## Getting Started

This documentation outlines the steps needed to sun the application over a container

### Service Now Ticket

Create a Service Now ticket with the necessary information (application name, team, consul/vault usage, databases)
DevOps will need clone and do an initial deployment of the application to devpreview.

### Running the application

In the project directory, you can run:

### `scripts/docker-run.sh "database username" "database password"`
Example : `scripts/docker-run.sh "myusername" "mypassword"`

Starts the streamlit server.\
Open [http://localhost:8080](http://localhost:8080) to view it in your browser.
