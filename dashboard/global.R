source('db.R')
library(dplyr)

bus_stops_data <- getbusStops()
only_busStops <- bus_stops_data %>%
  select(stop_id, address) %>%
  rename(`Bus Stop` = address) %>%
  rename(`Bus Stop ID` = stop_id)
# print(only_busStops)
busStops <- unique(bus_stops_data$address)
# print(busStops)

##lat long markers
# print(bus_stops_data)
busstopMarkers <- bus_stops_data %>%
  select(stop_id, address, latitude, longitude)
# print(busstopMarkers)

##
arrival_predict <- function(pythonScriptPath) {
  # Run the Python script using system() and capture the output
  pythonOutput <-
    system(paste("python", pythonScriptPath), intern = TRUE)
  
  # Convert the output into a character vector
  pythonOutput <- as.character(pythonOutput)
  
  # Return the captured output
  return(pythonOutput)
}


# pythonScriptPath <- "scripts_py\src\script\arrival_time_prediction.py"
# arrivalTime <- arrival_predict(pythonScriptPath)


# predictions
predictions <- read.csv("example_arrival_times.data.csv")
print("example data:")
print(predictions)

# Extract unique device_id values from the predictions dataset
device_ids <- unique(predictions$device_id)


getArrivalTime <- function(dev_id, bus_stop_id) {
  print(paste0("inside getarrival time"))
  subset_data <-
    subset(predictions, device_id == dev_id &
             Bus.Stop == bus_stop_id)
  print(subset_data)
  
  if (nrow(subset_data) == 0) {
    return(-1)
  }
  arrival_time <-
    subset_data$arrival.time[1]  # Assuming there's only one arrival time per device_id and bus_stop
  print(paste0("arrival time: ",arrival_time))
  return(arrival_time)
}
lookupBusStopId <- function(busStop) {
  stop_info <-
    bus_stops_data$stop_id[bus_stops_data$address == busStop]
  return(stop_info)
}


# device_id <- 117  # Replace with the desired device_id
# bus_stop <- 102  # Replace with the desired bus_stop
# arrival_time <- getArrivalTime(device_id, bus_stop)
# print(paste("Arrival time for device_id", device_id, "at bus_stop", bus_stop, "is", arrival_time))
#
