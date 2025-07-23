# Use the official Gradle image as a build image
FROM gradle:8.4-jdk20 AS build

# Set the working directory
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Install unzip utility
RUN apt-get update && apt-get install -y unzip

# Unzip the file into the specified folder
RUN unzip /app/src/main/resources/data/inventory.zip -d /app/src/main/resources/data
RUN unzip /app/src/main/resources/data/geo.zip -d /app/src/main/resources/data
RUN unzip /app/src/main/resources/data/hotels.zip -d /app/src/main/resources/data

# Run the Gradle build
RUN gradle clean build --no-daemon -x test

# Use the official OpenJDK base image for the final image
FROM openjdk:20-jdk-slim


# Set the working directory inside the container
WORKDIR /app

# Copy only the built JAR file from the build image into the final image
COPY --from=build /app/build/libs/*.jar app.jar

# Specify the command to run on container start using the environment variable for JVM options
CMD java -jar app.jar
