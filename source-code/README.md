# Performance and Scalability Analysis of Monolithic and Microservice Architectures

This repository contains the codebase and benchmarking tools for a comprehensive comparative analysis of monolithic and microservice architectures.

## Overview

The aim of this project is to evaluate and compare the performance and scalability of monolithic versus microservice architectures. The study explores various programming technologies by implementing a benchmarking application in three architectural variants:

- **Monolithic Architecture**
- **Microservice Architecture using REST API**
- **Microservice Architecture using gRPC**

Each architectural variant has been implemented using four programming languages: Java, Python, GoLang, and C#. The performance tests were conducted in a cloud environment on Google Cloud Platform using tools like Docker, Docker Swarm, Terraform, and GitHub Actions.

## Tools and Technologies

- **Programming Languages:** Java, Python, GoLang, C#
- **Cloud Platform:** Google Cloud Platform (GCP)
- **Containerization and Orchestration:** Docker, Docker Swarm
- **Infrastructure as Code:** Terraform
- **CI/CD:** GitHub Actions
- **Benchmarking Tools:** JMeter
- **Postprocessing:** R programming language

## Repository Structure

In the Repositories folder, there are all prepared implementations. 
They were implemented a part of the "Projekt Badawczy" program performed by students of Computer Science master degree studies at GUT. All code implemented as part of it can be found here - https://github.com/orgs/Microservices-Benchmarking-11-KIOP-2023/repositories
Each subfolder represents different programing language, and inside each there are 3 other subfolders:

- `/monolith`: Contains the monolithic architecture implementation.
- `/microservices-rest`: Contains the microservice implementation using REST API.
- `/microservices-grpc`: Contains the microservice implementation using gRPC.

## Key Findings

The microservice architecture consists of five components. Below is an image that represents microservices architecture on cloud environemnt.
Presented scenario represents architecture for the environment when 2 replicas of each services were created - as a part of horizontal scaling benchmarking tests.

<p align="center">
    <img width="100%" height="100%" src="results-pkrac/diag_micr_hor.png">
</p>


## Key Findings

<p align="center">
    <img width="100%" height="100%" src="results-pkrac/base/Monolit_plot.png">
</p>

<p align="center">
    <img width="100%" height="100%" src="results-pkrac/base/Mikroserwisy%20REST_plot.png">
</p>

<p align="center">
    <img width="100%" height="100%" src="results-pkrac/base/Mikroserwisy%20GRPC_plot.png">
</p>

The rest of achieved results can be found in the results folder of this repository.
