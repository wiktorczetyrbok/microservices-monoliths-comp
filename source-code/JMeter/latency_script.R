library(ggplot2)
library(dplyr)
library(svglite)
source('C:/Users/pawel/OneDrive/Pulpit/PB/Microservices-and-Monolith-comparison-benchmarking/JMeter/ggplot_theme_Publication.R')

getBenchmarkDF <- function(df, delta, total_time) {
  df$response_end_timeStamp <- df$timeStamp + df$elapsed
  estimated_benchmark_start <- min(df$timeStamp) + delta * 1000
  tmp <- df[df$response_end_timeStamp > estimated_benchmark_start, 'response_end_timeStamp']
  benchmark_start <- min(tmp)
  benchmark_end <- benchmark_start + total_time * 1000
  return(df[df$response_end_timeStamp >= benchmark_start & df$response_end_timeStamp <= benchmark_end,])
}

getStat <- function(df, total_time, max_latency = 200, drop_unsuccessful = TRUE) {
  all_requests <- nrow(df)
  if (drop_unsuccessful) df <- df[df$responseCode == 200,]
  successful_requests <- nrow(df)
  error_rates <- (all_requests - successful_requests) / all_requests
  median_latency <- median(df$Latency)
  q90_latency <- quantile(df$Latency, probs = c(0.9))
  if (max_latency > 0) df <- df[df$Latency <= max_latency,]
  result <- list(Median_latency = median_latency, Q90_latency = q90_latency, Error_rates = error_rates)
  return(result)
}

delta <- 4
total_time <- 5
baseDir <- "C:/Users/pawel/OneDrive/Pulpit/PB/Results/data_grouped_architecture/"
languageMap <- list('Java-' = 'Java', 'C#-' = 'C#', 'Python-' = 'Python', 'Go-' = 'GoLang')

mainFolders <- list.dirs(baseDir, full.names = TRUE, recursive = FALSE)
plotList <- list()
allData <- list()

for (mainFolder in mainFolders) {
  subFolders <- list.dirs(mainFolder, full.names = TRUE, recursive = FALSE)
  subFolders <- subFolders[subFolders != mainFolder]
  
  for (subFolder in subFolders) {
    subFolderName <- basename(subFolder)
    iterationDirectories <- list.dirs(subFolder, full.names = FALSE)
    iterationDirectories <- iterationDirectories[iterationDirectories != "."]
    statsDF <- data.frame(Users = integer(), Median_latency = numeric(), Q90_latency = numeric(), Error_rates = numeric())
    
    for (iteration in iterationDirectories) {
      csvFiles <- list.files(file.path(subFolder, iteration), pattern = "*.csv", full.names = TRUE)
      for (filePath in csvFiles) {
        fileName <- basename(filePath)
        users <- as.integer(sub("users_", "", substr(fileName, 1, nchar(fileName) - 4)))
        data <- read.csv(filePath)
        min_timeStamp <- min(data$timeStamp)
        data$timeStamp <- data$timeStamp - min_timeStamp
        df <- getBenchmarkDF(data, delta, total_time)
        stat <- getStat(df, total_time)
        statsDF[nrow(statsDF) + 1,] <- c(users, stat$Median_latency, stat$Q90_latency, stat$Error_rates)
      }
    }
    
    aggregatedDF <- aggregate(. ~ Users, data = statsDF, median)
    prefix <- sapply(names(languageMap), function(x) ifelse(startsWith(subFolderName, x), languageMap[[x]], NA))
    prefix <- na.omit(prefix)
    if (length(prefix) > 0) {
      subFolderName <- prefix[1]
    }
    aggregatedDF$SubFolder <- subFolderName
    allData[[subFolderName]] <- aggregatedDF
  }
  
  combinedData <- do.call(rbind, allData)
  
  p <- ggplot(combinedData, aes(x = Users, y = Median_latency, colour = SubFolder, group = SubFolder)) +
    geom_point(size = 2) +
    geom_line(linewidth = 1.5) +
    labs(title = basename(mainFolder), x = "Liczba użytkowników", y = "Mediana latencji (ms)", color = "Implementacja") +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5),
      axis.title.x = element_text(margin = margin(t = 20)),
      axis.title.y = element_text(margin = margin(r = 30))
    ) +
    scale_colour_Publication() +
    theme_Publication()
  
  plotList[[paste(basename(mainFolder))]] <- p
  
  svg_filename <- paste0("C:/Users/pawel/OneDrive/Pulpit/PB/Results/result_plots/grouped/latency/", basename(mainFolder), "_plot.png")
  
  ggsave(filename = svg_filename, plot = p, width = 12, height = 8, bg = "gray")
}

for (plot in plotList) {
  print(plot)
}
