#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

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
        # menuItem("Time Stamps", tabName = "Time Stamps", icon = icon("clock")),
        # menuItem("Map", tabName = "Map",  icon = icon("map")), 
        # menuSubItem("Current Location",  tabName = "Current Location",  icon = icon("location-dot")), 
        # menuItem("Delayed Locations",  tabName = "Delay",  icon = icon("bridge-circle-exclamation"),  badgeLabel  =  "New",  badgeColor  = 'green')
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
          # ,
          # 
          #  box(width = NULL, status = "primary",
          #                    selectInput("interval", "Refresh interval",
          #                                choices = c(
          #                                  "15 seconds" = 15,
          #                                  "30 seconds" = 30,
          #                                  "1 minute" = 60,
          #                                  "2 minutes" = 120,
          #                                  "5 minutes" = 300,
          #                                  "10 minutes" = 600
          #                                ),
          #                                selected = "60"
          #                    ),
          #                    uiOutput("timeSinceLastUpdate"),
          #                    actionButton("refresh", "Refresh now"),
          #                    p(class = "text-muted",
          #                      br(),
          #                      "Source data updates every 15 seconds.")),

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
                            ))
                        # box(width = NULL, status = "primary",
                        #     uiOutput("routeSelectColumn2"),
                        #     selectInput("routeSelectInput2", h4(strong("Select the Route:"), style = "color:black"),
                        #                 choices = c("Kandy-Digana", "Digana-Kandy"),
                        #                 selected = "Kandy-Digana"),
                        #     selectInput("startingStopInput2", h4(strong("Select the Starting Bus Stop:")),
                        #                 choices = c("Kandy", "Wales-Park", "Mahamaya", "Thennekubura Bridge"),
                        #                 selected = "Thennekubura Bridge")
                        # ),
                        ,
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
                # box(title = "Arrival Time", solidHeader = TRUE, width = NULL, status = "primary",
                    # style = "max-height: 400px; overflow-x: auto; overflow-y: auto;",
                    valueBoxOutput("arrivalTimeOut", width = NULL),
                    valueBoxOutput("usualTimeOut", width = NULL),# h4("Arrived to"),
                    # h2("Thennekubura Bridge"),
                    # h4("at"),
                    # h1("02.15pm")
                # )
                ),
        column(width = 2,
                infoBoxOutput("businfo", width = NULL)
        ),
        column(width = 4,
                # box(title = "Delays", solidHeader = TRUE, width = NULL, status = "primary",
                    # style = "max-height: 400px; overflow-x: auto; overflow-y: auto;",
                  
                    #h3("Delayed Location:"),
                      #h3("Mahamaya"),
                  
                  # HTML(paste0(h2(strong("Delayed Location:"),br(),"Mahamaya"))),
                  # HTML(paste0(h2(strong("Possible reason:"),br(),"Children's Park Nearby and Max elevation along route is 520m"))),
                  
                  #h3("Possible reason: Children's Park Nearby and Max elevation along route is 520m"),
                  valueBoxOutput("Delays", width = NULL),
                # )
                )
        
      ),
      ),

      # 
      #         selectInput("dropdown", "Select the Route:",
      #                     choices  =  c("Kandy-Digana", "Kandy-Katugasthota"),
      #                     selected  =  "Kandy-Digana"),
      #         verbatimTextOutput("selcted_option"),
      #         selectInput("dropdown_map", "Select the Starting Bus Stop:",
      #                     choices  =  c("Kandy", "Wales-Park", "Mahamaya", "Thennekubura Bridge"),
      #                     selected  =  "Thennekubura Bridge"),
      #         verbatimTextOutput("selcted_option"),
      #         h1("Arrival Time"),
      #         h2("Thennekubura Bridge"),
      #         h1("02:15 pm")
      #        )
      # )
    # 
    #       (tabItem(tabName = "Arrival",
    #                selectInput("dropdown", "Select the Route:",
    #                            choices  =  c("Kandy-Digana", "Kandy-Katugasthota"),
    #                            selected  =  "Kandy-Digana"),
    #                verbatimTextOutput("selcted_option"),
    #                selectInput("dropdown_map", "Select the Starting Bus Stop:",
    #                            choices  =  c("Kandy", "Wales-Park", "Mahamaya", "Thennekubura Bridge"),
    #                            selected  =  "Thennekubura Bridge"),
    #                verbatimTextOutput("selcted_option"),
    #                h1("Arrival Time"),
    #                h2("Thennekubura Bridge"),
    #                h1("02:15 pm"))),
    #       (tabItems(
    #         tabItem(tabName  =  "Delay",
    #                 fluidRow(column(width = 10,
    #                                 infoBox("Delayed Location: Mahamaya" ,
    #                                         icon = icon("location-dot"))),
    #                          infoBox("20 mins Delay than usual" ,icon = icon("clock")),
    #                          infoBox("Factors to delay: Childrens' Park nearby,  max elevation 520m" ,
    #                                  icon = icon("person-snowboarding")))),
    # 
    #         tabItem(tabName  =  "Map",
    # 
    #                 titlePanel("Map"),
    #                 tabsetPanel(
    #                   tabItem(tabName = "Map"),
    #                   # leafletOutput("Map")
    #                 )
    # 
    #         ),
    # 
    #         tabItem(tabName  =  "Delay",
    #                 h1("Delay"),
    # 
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