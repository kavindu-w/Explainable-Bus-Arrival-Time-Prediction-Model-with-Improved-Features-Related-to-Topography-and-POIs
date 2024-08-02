
source('db.R')
source('ui.R')
source('global.R')
library(shiny)
library(shinydashboard)
library(dplyr)
library(leaflet)

shinyServer(function(input,output, session){
  output$map <- renderLeaflet({
    leaflet() %>%
      addTiles() %>%
      setView(lng = 80.6349778, 
              lat = 7.292462226
              , zoom = 6)  # Adjust the initial view coordinates and zoom level
  })
  
  output$busStops <- renderTable({
    only_busStops 
  })
  
  # Update the choices of bus stops
  updateSelectInput(session, "startingStopInput1", choices = busStops) 

  # Update the choices of the selectInput with the unique device_ids
  updateSelectInput(session, "device_id_select", choices = device_ids)
  
  observeEvent(c(input$device_id_select, input$startingStopInput1), {
    selected_device_id <- input$device_id_select
    selected_bus_stop <- input$startingStopInput1
    selected_bus_stop_id <- lookupBusStopId(selected_bus_stop)
    
    print(selected_device_id)
    print(selected_bus_stop_id)
    
    usualTime <- 6 # get historical data
    
    # Call the function to get arrival time based on selected_device_id and selected_bus_stop
    arrival_time <- getArrivalTime(selected_device_id, selected_bus_stop_id)
    if (arrival_time == -1) {
      output$arrivalTimeOut <- renderInfoBox({
        valueBox(
          tags$p("Arrival Time", style = "font-size: 80%;"),
          tags$p(paste0("In ", arrival_time, " mins"), style = "font-size: 150%;"),
          icon = icon("hourglass-half"),
          color = "gray"  # Set a neutral color initially
        )
      })

      output$usualTimeOut <- renderValueBox({
        valueBox(
          value = tags$p("No data", style = "font-size: 45%;"),  # Set a placeholder message
          NULL, icon = tags$i(class = "question-circle", style = "font-size: 100%"),
          color = "gray"  # Set a neutral color initially
        )
      })
      
      output$Delays <- renderValueBox({
        valueBox(
          value = tags$p("No data", style = "font-size: 45%;"),  # Set a placeholder message
          NULL, icon = tags$i(class = "question-circle", style = "font-size: 100%"),
          color = "gray"  # Set a neutral color initially
        )
      })
    }
    arrival_time <- round(arrival_time/60)
    output$arrivalTimeOut <- renderInfoBox({
      color <- if (arrival_time < 8) {
        "green"
      } else if (arrival_time >= 8 && arrival_time <= 10) {
        "yellow"
      } else {
        "red"
      }
      valueBox(
        tags$p("Arrival Time", style = "font-size: 80%;"), 
        tags$p(HTML(paste0("At ", selected_bus_stop, br()," In ", arrival_time, " mins")), style = "font-size: 150%;"), 
        icon = icon("hourglass-half"),
        color = color
      )
    })
    
    output$usualTimeOut <- renderValueBox({
      if (usualTime < arrival_time) {
        str <- paste0(arrival_time - usualTime, " mins later than usual")
        color <- "red"
        icon <- "arrow-up"
      } else if (usualTime > arrival_time) {
        str <- paste0(usualTime - arrival_time, " mins earlier than usual")
        color <- "green"
        icon <- "circle-chevron-up"
      } else {
        str <- paste0("Bus is on time as usual")
        color <- "green"
        icon <- "arrow-up"
      } 
      valueBox(
        value = tags$p(str, style = "font-size: 45%;"),
        NULL, icon = tags$i(class = icon, style = "font-size: 100%"),
        color = color
      )
    })
    output$businfo <- renderInfoBox({
      infoBox(
        tags$p(strong("Bus ID"), style = "font-size: 110%;"), paste0(selected_device_id), icon = icon("bus"),
        color = "blue"
      )
    })
    output$Delays <- renderInfoBox({
      if (arrival_time < 8) {
        valueBox(
          tags$p(HTML(paste0(h2(strong("Delays")),h4("No delays")))),
          icon = icon("thumbs-up"),
          color = "green",
          subtitle = ""
          )
      
      } else if (arrival_time >= 8 && arrival_time <= 10) {
        valueBox(
          tags$p(HTML(paste0(
            h2(strong("Delayed Location:")),
            h4("Mahamaya"),
            h4(strong("Possible reasons:")),
            "<ul>",
            "<li>", h4("Children's Park Nearby"), "</li>",
            "<li>", h4("Max elevation along route is 520m"), "</li>",
            "</ul>"
          ))),
          icon = icon("stopwatch"),
          color = "yellow",
          subtitle = ""
        )
      } else {
        valueBox(
          tags$p(HTML(paste0(
            h2(strong("Delayed Location:")),
            h4("Mahamaya"),
            h4(strong("Possible reasons:")),
            "<ul>",
            "<li>", h4("Hospital Nearby"), "</li>",
            "<li>", h4("Max elevation along route is 490m"), "</li>",
            "</ul>"
          ))),
          icon = icon("triangle-exclamation"),
          color = "red",
          subtitle = ""
        )
      }
      

    })
  
    output$graphOutput <- renderPlot({
    # Create your plot here, for example:
    #x <- dataG$segment
    #y <- dataG$avg_elevation
    x <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
    y <- c(511.65,529.50,529.10,515.71,480.33,450.00,472.56,481.83,487.83,489.33,488.56,457.71,473.67,464.71,516.60)
    #data <- data.frame(x = 1:10, y = rnorm(10))
    plot(x, y, type = "l", col = "blue",main="avg_elevation from Kandy to Digana",xlab="segment",ylab="elevation")
  })
  
  output$graphOutput2 <- renderPlot({
    # Create your plot here, for example:
    #x <- dataG$segment
    #y <- dataG$max_elevation
    x <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
    y <- c(532.00,532.00,544.00,527.00,488.00,468.00,480.00,485.00,494.00,494.00,494.00,467.00,475.00,473.00,525.00)
    #data <- data.frame(x = 1:10, y = rnorm(10))
    plot(x, y, type = "l", col = "purple",main="avg_elevation from Kandy to Digana",xlab="segment",ylab="elevation")
  })
})
})
