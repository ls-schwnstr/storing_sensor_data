# Sensor Data InfluxDB

## Overview

This project sets up an InfluxDB instance with sample sensor data using Docker. It includes a Docker container that will automatically load sample data into your InfluxDB instance.

## Prerequisites

- **Docker**: Make sure Docker is installed on your machine. You can download and install Docker from [Docker's official website](https://www.docker.com/products/docker-desktop).
- **InfluxDB**: You need to have an InfluxDB instance running. You can use the InfluxDB cloud service or run it locally using Docker.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/yourusername/your-repository-name.git](https://github.com/ls-schwnstr/storing_sensor_data.git)
   cd storing_sensor_data

2. **Build the Docker Image**:
   docker build -t sensor-data-influxdb .
   
4. **Create a '.env' File**:
   - Create a file named .env in the root directory of the project.
   - Add your InfluxDB credentials and any other necessary environment variables. Here’s an example .env file:

   INFLUXDB_TOKEN=your_influxdb_token
   INFLUXDB_URL=https://your-influxdb-url.com
   INFLUXDB_ORG=your_organization
   INFLUXDB_BUCKET=your_bucket

   
5. **Run the Docker Container**:
   docker run --env-file .env sensor-data-influxdb

