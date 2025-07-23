library(ggplot2)
library(dplyr)
library(gridExtra)  
library(grid) 

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
  throughput <- nrow(df) / total_time
  result <- list(Throughput = throughput, Median_latency = median_latency, Q90_latency = q90_latency, Error_rates = error_rates)
  return(result)
}

delta <- 4
total_time <- 5
baseDir <- "C:/Users/pawel/OneDrive/Pulpit/PB/Results/data_grouped_by_language_horizontal/"

g_legend <- function(a.gplot){
  tmp <- ggplot_gtable(ggplot_build(a.gplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend)
}

languageFolders <- list.dirs(baseDir, full.names = TRUE, recursive = FALSE)
plotList <- list()

for (languageFolder in languageFolders) {
  architectureFolders <- list.dirs(languageFolder, full.names = TRUE, recursive = FALSE)
  architectureFolders <- architectureFolders[architectureFolders != languageFolder]
  archPlots <- list()  
  
  for (architectureFolder in architectureFolders) {
    configFolders <- list.dirs(architectureFolder, full.names = TRUE, recursive = FALSE)
    configFolders <- configFolders[configFolders != architectureFolder]
    allStatsDF <- list()
    
    for (configFolder in configFolders) {
      iterationFolders <- list.dirs(configFolder, full.names = TRUE, recursive = FALSE)
      iterationFolders <- iterationFolders[iterationFolders != configFolder]
      statsDF <- data.frame(Users = integer(), Throughput = numeric(), Median_latency = numeric(), Q90_latency = numeric(), Error_rates = numeric())
      
      for (iterationFolder in iterationFolders) {
        csvFiles <- list.files(iterationFolder, pattern = "*.csv", full.names = TRUE)
        
        for (filePath in csvFiles) {
          data <- read.csv(filePath)
          min_timeStamp <- min(data$timeStamp)
          data$timeStamp <- data$timeStamp - min_timeStamp
          df <- getBenchmarkDF(data, delta, total_time)
          stat <- getStat(df, total_time)
          users <- as.integer(gsub("users_|\\.csv", "", basename(filePath)))
          statsDF[nrow(statsDF) + 1,] <- c(users, stat$Throughput, stat$Median_latency, stat$Q90_latency, stat$Error_rates)
        }
      }
      
      aggregatedDF <- aggregate(. ~ Users, data = statsDF, median)
      aggregatedDF$Configuration <- basename(configFolder)
      allStatsDF[[basename(configFolder)]] <- aggregatedDF
    }
    
    combinedData <- do.call(rbind, allStatsDF)
    
    combinedData <- combinedData %>%
      group_by(Configuration) %>%
      mutate(
        Throughput_max = max(Throughput),
        MaxIndex = which.max(Throughput),
        FirstMax = row_number() == MaxIndex,
        FirstBelow95 = {
          below95 <- Throughput < (0.90 * Throughput_max) & row_number() > MaxIndex 
          if (any(below95)) min(which(below95)) else NA_integer_ 
        },
        keepPlotting = ifelse(row_number() <= FirstBelow95, TRUE, FALSE)  
      ) %>%
      ungroup() %>%
      filter(!is.na(keepPlotting) & keepPlotting)
    
    plot_range <- diff(range(combinedData$Throughput))
    
    p <- ggplot(combinedData, aes(x = Users, y = Throughput, colour = Configuration, group = Configuration)) +
      geom_point(size = 2) +
      geom_line(linewidth = 1.5) +
      geom_text(data = combinedData[combinedData$FirstMax, ], aes(label = paste(Throughput), y = Throughput), vjust = -1, color = "black", size = 6) +
      geom_point(data = combinedData[combinedData$FirstMax, ],  aes(x = Users, y = Throughput), colour = "black", size = 3, shape = 17) +
      labs(title = paste(basename(architectureFolder)), x = NULL, y = NULL, color = "Ilość instancji") +
      scale_color_manual(labels = c("horizontal_1" = "1", "horizontal_2" = "2", "horizontal_4" = "4"), values = c("horizontal_1" = "#386cb0", "horizontal_2" = "#fdb462", "horizontal_4" = "#7fc97f")) +
      scale_x_continuous(breaks = scales::pretty_breaks()) +
      theme_Publication() +
      theme(axis.title.x = element_blank(), axis.title.y = element_blank(),
            plot.margin = unit(c(0.5, 0.5, 0.1, 0.5), "cm")) 
    
    archPlots[[basename(architectureFolder)]] <- p
  }
  
  legend <- g_legend(archPlots[[1]])
  
  for (i in seq_along(archPlots)) {
    archPlots[[i]] <- archPlots[[i]] + theme(legend.position = "none", axis.title.x = element_blank(), axis.title.y = element_blank())
  }
  
  combinedPlot <- grid.arrange(
    grobs = archPlots,
    ncol = 1,
    nrow = length(archPlots),
    top = textGrob(paste("Wyniki skalowania horyzontalnego: ", basename(languageFolder)), gp = gpar(fontsize = 16, font = 2)),
    bottom = textGrob("Liczba użytkowników", gp = gpar(fontsize = 12), vjust = -0.5) 
  )
  
  finalPlot <- grid.arrange(
    combinedPlot,
    legend,
    ncol = 1,
    heights = c(length(archPlots), 0.1)
  )
  
  finalPlot <- arrangeGrob(
    finalPlot,
    left = textGrob("Przepustowość", rot = 90, gp = gpar(fontsize = 12))
  )
  
  plotList[[basename(languageFolder)]] <- finalPlot
  
  ggsave(filename = paste0("C:/Users/pawel/OneDrive/Pulpit/PB/Results/result_plots/horizontal_scaling/", basename(languageFolder), "_combined_comparison_plot.png"), plot = finalPlot, width = 16, height = 8 * length(archPlots) + 2, dpi = 600, bg = "white")
}

for (plotName in names(plotList)) {
  grid.draw(plotList[[plotName]])
}
