# Use the official Gradle image as a build image
FROM gradle:8.4-jdk21 AS build

# Set the working directory
WORKDIR /home/gradle/project

# Copy the entire project into the container
COPY . .

# Run the Gradle build
RUN gradle clean build --no-daemon

# Use the official OpenJDK base image for the final image
FROM eclipse-temurin:21-jre

# Set the working directory inside the container
WORKDIR /app

# Copy only the built JAR file from the build image into the final image
COPY --from=build /home/gradle/project/build/libs/*.jar app.jar

# Specify the command to run on container start
CMD ["java", "-jar", "app.jar"]
