library(ggplot2)
library(dplyr)
library(tidyr)
library(grid)
library(ggthemes)
library(scales)

theme_Publication <- function(base_size=14, base_family="sans") {
  (theme_foundation(base_size=base_size, base_family=base_family)
   + theme(plot.title = element_text(face = "bold",
                                     size = rel(1.2), hjust = 0.5),
           text = element_text(),
           panel.background = element_rect(colour = NA),
           plot.background = element_rect(colour = NA),
           panel.border = element_rect(colour = NA),
           axis.title = element_text(face = "bold", size = rel(1)),
           axis.title.y = element_text(angle = 90, vjust = 2),
           axis.title.x = element_text(vjust = -0.2),
           axis.text = element_text(),
           axis.line.x = element_line(colour = "black"),
           axis.line.y = element_line(colour = "black"),
           axis.ticks = element_line(),
           panel.grid.major = element_line(colour = "#f0f0f0"),
           panel.grid.minor = element_blank(),
           legend.key = element_rect(colour = NA),
           legend.position = "bottom",
           legend.key.size = unit(0.4, "cm"),
           legend.margin = unit(0, "cm"),
           legend.title = element_text(face = "italic"),
           plot.margin = unit(c(10, 5, 5, 5), "mm"),
           strip.background = element_rect(colour = "#f0f0f0", fill = "#f0f0f0"),
           strip.text = element_text(face = "bold")
   ))
}

custom_palette <- c(
  "Wertykalne" = "#1E90FF",  # niebieski
  "Horyzontalne" = "#FF4500"  # czerwony
)

scaling_data <- data.frame(
  Language = c("C#", "C#", "C#", "Go", "Go", "Go", "Python", "Python", "Python", "Java", "Java", "Java"),
  Architecture = c("monolityczna", "mikroserwisowa", "mikroserwisowa", "monolityczna", "mikroserwisowa", "mikroserwisowa", "monolityczna", "mikroserwisowa", "mikroserwisowa", "monolityczna", "mikroserwisowa", "mikroserwisowa"),
  Technology = c("Monolit", "REST API", "gRPC", "Monolit", "REST API", "gRPC", "Monolit", "REST API", "gRPC", "Monolit", "REST API", "gRPC"),
  c2d_standard_4 = c(3069.2, 524.8, 1363.4, 1803.8, 393, 863.6, 206.4, 56, 70, 2693, 580, 1400.6),
  c2d_standard_8 = c(6110.2, 1042.2, 2678.6, 3435.4, 722.8, 1651, 287.4, 59.6, 79, 5473, 1178.8, 2878),
  replicas_2 = c(2788.8, 429.4, 977, 1736.2, 402.4, 879.4, 188.6, 81.4, 68.2, 2502, 559.6, 1125.4),
  replicas_4 = c(5551.4, 814.4, 1921.6, 3409.8, 773, 1585, 378.4, 145.6, 72.8, 4915.8, 1056.8, 1555.4)
)

long_data <- scaling_data %>%
  pivot_longer(cols = c(c2d_standard_4, c2d_standard_8, replicas_2, replicas_4), 
               names_to = "Metric", 
               values_to = "Value") %>%
  mutate(Comparison = case_when(
    Metric %in% c("c2d_standard_4", "c2d_standard_8") ~ "Wertykalne",
    Metric %in% c("replicas_2", "replicas_4") ~ "Horyzontalne"
  ))

long_data <- long_data %>%
  mutate(ComparisonType = factor(case_when(
    Metric %in% c("c2d_standard_4", "replicas_2") ~ "Dwukrotne zwiększenie zasobów",
    Metric %in% c("c2d_standard_8", "replicas_4") ~ "Czterokrotne zwiększenie zasobów"
  ), levels = c("Dwukrotne zwiększenie zasobów",
                "Czterokrotne zwiększenie zasobów")))

long_data <- long_data %>%
  mutate(TechArch = case_when(
    Technology == "Monolit" ~ "Monolit",
    Technology == "gRPC" & Architecture == "mikroserwisowa" ~ "Mikroserwisy gRPC",
    Technology == "REST API" & Architecture == "mikroserwisowa" ~ "Mikroserwisy REST"
  ))

generate_plot <- function(data, language) {
  ggplot(data %>% filter(Language == language), aes(x = TechArch, y = Value, fill = Comparison)) +
    geom_bar(stat = "identity", position = "dodge") +
    geom_text(aes(label = round(Value, 1)), vjust = -0.5, position = position_dodge(width = 0.9)) +
    labs(title = paste("Porównanie mechanizmów skalowania dla języka", language),
         x = "Implementacja aplikacji",
         y = "Przepustowość",
         fill = "Mechanizm skalowania") +
    theme_Publication() +
    scale_fill_manual(values = custom_palette) +
    facet_grid(. ~ ComparisonType, scales = "free_x") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          legend.position = "bottom") +
    guides(fill = guide_legend(direction = "horizontal"))
}

outputFolder <- "C:/Users/pawel/OneDrive/Pulpit/PB/Results/Result_plots/ind"

languages <- unique(long_data$Language)

for (lang in languages) {
  plot <- generate_plot(long_data, lang)
  ggsave(filename = paste0(outputFolder, "/plot_", lang, ".png"), plot = plot, width = 16, height = 8, units = "cm")
  print(plot)
}
