library(shiny)
library(shinydashboard)
library(leaflet)

# Define UI for application that draws a histogram
shinyUI(
  dashboardPage(skin = "purple",
    dashboardHeader(title = "Bus Arrival Time Dashboard", titleWidth = 350,
      dropdownMenu(type = "message",
                  messageItem(from = "AD-9789",
                              message = "Arrived to Lewella Junction  ",
                              icon = icon("bus"), time = "14:15"
                              )
                  ), 
      dropdownMenu(type = "notifications", 
        notificationItem(
          text = "RDA: Construction at Thalwatta ", 
          icon = icon("person-digging"), status = "success",
        )
      )
    ), 
    dashboardSidebar(width = 350,
      sidebarMenu(
        (sidebarSearchForm("searchText", "buttonSearch", "Search"))), 
        menuItem("Arrival Time", tabName = "Arrival", icon = icon("calendar-week")),
        menuItem("Visualizations", tabName = "Visualizations",icon=icon("chart-area"))
    ), 
    dashboardBody(
      tags$head(
        tags$link(rel = "stylesheet", type = "text/css", href = "custom.css")
      ),
      # tabItems(
      tabItem(tabName = "Arrival",
      fluidRow(
        column(width = 3,
          box(width = NULL, status = "primary",
              uiOutput("routeSelectColumn1"),
              selectInput("routeSelectInput1", h4(strong("Select the Route:"), style = "color:black"),
                          choices = c("Kandy-Digana", "Digana-Kandy"),
                                      selected = "Kandy-Digana"),
              selectInput("startingStopInput1", 
                          h4(strong("Select the Starting Bus Stop:")),
                          choices = NULL),
              selectInput("device_id_select", 
                            HTML(paste0(h4(strong("Select an Available Bus:"),
                            br(),"(Fastest bus will appear first)"))), 
                            choices = NULL)
                          )

          ),
                  column(width = 9,
                        box(title = "Map", solidHeader = TRUE, width = NULL, status = "primary",
                            style = "max-height: 800px; overflow-x: auto; overflow-y: auto;",
                            #plotOutput("elevationPlot")
                            div(style = "width: 100%; height: 300px;",  # Adjust the width and height as needed
                                # leafletOutput("map")
                                leaflet(data = busstopMarkers) %>% 
                                  addTiles() %>%
                                  addMarkers(
                                    ~longitude, ~latitude,
                                    popup = ~address,
                                    label = ~address
                                  )
                            )),
                  )
                ),

      fluidRow(
        column(width = 3,
                box(title = "Bus Stops", solidHeader = TRUE, width = NULL, status = "primary",
                    style = "max-height: 400px; overflow-x: auto; overflow-y: auto;",
                    tableOutput("busStops")
                )
        ),
        column(width = 3,
                    valueBoxOutput("arrivalTimeOut", width = NULL),
                    valueBoxOutput("usualTimeOut", width = NULL),# h4("Arrived to"),
                ),
        column(width = 2,
                infoBoxOutput("businfo", width = NULL)
        ),
        column(width = 4,
                  valueBoxOutput("Delays", width = NULL),
                )
        
      ),
      ),

    tabItem(tabName = "Visualizations",
              fluidRow(
                box(title = "avg_elevation", solidHeader = TRUE, width = NULL, status = "primary",
                    plotOutput("graphOutput")
                ) ,
                box(title = "max_elevation", solidHeader = TRUE, width = NULL, status = "primary",
                    plotOutput("graphOutput2")
                ))
    )
    ) # dashboard body
  ) # dashbpard page
) # all
