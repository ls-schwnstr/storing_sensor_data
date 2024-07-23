# Sensor Data InfluxDB

## Overview

This project sets up an InfluxDB instance with sample sensor data using Docker. It includes a Docker container that will automatically load sample data into your InfluxDB instance.
The dataset can also be downloaded here: [dataset](https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k?resource=download).

## Prerequisites

- **Docker**: Make sure Docker is installed on your machine. You can download and install Docker from [Docker's official website](https://www.docker.com/products/docker-desktop).
- **InfluxDB**: You need to have an InfluxDB instance running. You can use the InfluxDB cloud service or run it locally using Docker.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository

2. **Build the Docker Image**:
   ```bash
   docker build -t sensor-data-influxdb .
   
4. **Create a '.env' File**:
   - Create a file named .env in the root directory of the project.
   - Add your InfluxDB credentials and any other necessary environment variables. Here’s an example .env file:

   INFLUXDB_TOKEN=your_influxdb_token  
   INFLUXDB_URL=https://your-influxdb-url.com  
   INFLUXDB_ORG=your_organization  
   INFLUXDB_BUCKET=your_bucket  

   
5. **Run the Docker Container**:
   ```bash
   docker run --env-file .env sensor-data-influxdb

