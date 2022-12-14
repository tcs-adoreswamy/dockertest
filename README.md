[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=the-container-store_reference-python-app&metric=alert_status&token=CHANGE_ME)](https://sonarcloud.io/summary/new_code?id=the-container-store_reference-python-app)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=the-container-store_reference-python-app&metric=bugs&token=CHANGE_ME)](https://sonarcloud.io/summary/new_code?id=the-container-store_reference-python-app)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=the-container-store_reference-python-app&metric=reliability_rating&token=CHANGE_ME)](https://sonarcloud.io/summary/new_code?id=the-container-store_reference-python-app)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=the-container-store_reference-python-app&metric=vulnerabilities&token=CHANGE_ME)](https://sonarcloud.io/summary/new_code?id=the-container-store_reference-python-app)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=the-container-store_reference-python-app&metric=security_rating&token=CHANGE_ME)](https://sonarcloud.io/summary/new_code?id=the-container-store_reference-python-app)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=the-container-store_reference-python-app&metric=code_smells&token=CHANGE_ME)](https://sonarcloud.io/summary/new_code?id=the-container-store_reference-python-app)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=the-container-store_reference-python-app&metric=sqale_rating&token=CHANGE_ME)](https://sonarcloud.io/summary/new_code?id=the-container-store_reference-python-app)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=the-container-store_reference-python-app&metric=coverage&token=CHANGE_ME)](https://sonarcloud.io/summary/new_code?id=the-container-store_reference-python-app)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=the-container-store_reference-python-app&metric=duplicated_lines_density&token=CHANGE_ME)](https://sonarcloud.io/summary/new_code?id=the-container-store_reference-python-app)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=the-container-store_reference-python-app&metric=ncloc&token=CHANGE_ME)](https://sonarcloud.io/summary/new_code?id=the-container-store_reference-python-app)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=the-container-store_reference-python-app&metric=sqale_index&token=CHANGE_ME)](https://sonarcloud.io/summary/new_code?id=the-container-åstore_reference-python-app)

# Reference-Python-App

This project is a starter template designed to help developers create a new
Python application that meets TCS Code Quality & Standards. This reference application can be cloned
and used to scaffold a new service.

## Getting Started

This documentation outlines the steps needed to scaffold a basic Python application.

### Service Now Ticket

Create a Service Now ticket with the necessary information (application name, team, consul/vault usage, databases)
DevOps will need clone and do an initial deployment of the application to devpreview.

### Update your repository

Clone the newly created repository, create a local branch and perform the following changes

- Search for and replace instances of "reference-python-app" with your application name

- Update your `.project-config.yml`. Every project provides a configuration file that provides project-level metadata for use by our CI/CD pipeline

  - [Technology Decision](https://github.com/the-container-store/Technology-Decisions/blob/master/0016-project-config-file.md)
  - [Project Config Schema](https://github.com/the-container-store/Technology-Decisions/blob/master/schema/project-config-yml.md)

- Cleanup the readme to be relevant to the project

- Push the branch and create a pull request

### Secrets and Configuration

If your project will need to access secrets from Vault

1. Coordinate with the DevOps team to have your secrets added to Vault

2. Create application [Vault Policies](https://github.com/the-container-store/Vault-Config/tree/master/policies/app) for _dev_, _tst_, _prd_ and _trn_.

3. Apply the policies via this [TeamCity Build Configuration](https://teamcity.containerstore.com/viewType.html?buildTypeId=DevOps_VaultConfig_ApplyPolicy)

4. Add the Vault and Consul paths to your `config.ctmpl`. See the [entrypoint.ctmpl](https://github.com/the-container-store/docker/blob/master/python/entrypoint.ctmpl) included in the docker image for a reference.

### Running the application

In the project directory, you can run:

### `sh scripts/docker-run.sh`

Starts the express server.\
Open [http://localhost:8080](http://localhost:8080) to view it in your browser.
