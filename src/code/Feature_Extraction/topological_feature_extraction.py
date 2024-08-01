import numpy as np
import pandas as pd
import warnings
import requests # for api calls
import osmnx as ox
from tqdm import tqdm # progress bar
warnings.filterwarnings(action="ignore")

###################################################################
## Location coordinates extraction

def extract_intermediate_locations_from_route(start_route_point, end_route_point):
    """
    when given a route(terminal to terminal) extract the coordinates of intermediate locations(nodes) along the route
    (the smallest possible location points that can be extracted from the route by using osmnx package)
    
    Args:
        start_route_point: the point where the route starts
        end_route_point: the point where the route ends
    
    Returns:
        list of coordinates of intermediate locations(nodes) along the route [(lat, long), ...]
    """
    # get a graph for the route
    G = ox.graph_from_point(center_point=start_route_point, dist=500, network_type='all_private')

    # Get the nearest network nodes to the start and end points
    start_node = ox.distance.nearest_nodes(G, start_route_point[1], start_route_point[0])
    end_node = ox.distance.nearest_nodes(G, end_route_point[1], end_route_point[0])

    # Calculate the route between the start and end nodes
    route = ox.distance.shortest_path(G, start_node, end_node, weight='length')

    # Extract locations along the route
    locations = []
    for node in route:
        node_data = G.nodes[node]
        latitude = node_data['y']
        longitude = node_data['x']
        locations.append(f"{latitude},{longitude}")
    # add only start point to the locations(as it is affecting up to next terminal)
    # add as the first element
    locations.insert(0, f"{start_route_point[0]},{start_route_point[1]}")
    
    return locations


def location_extraction_pipeline(busStops, route_points, segment_id_start):
    """
    extracts locations from bus stops and route points and groups them based on their segment and direction.
    
    Args:
        busStops: a DataFrame containing information about the bus stops. It
    should have columns for `latitude`, `longitude`, `stop_id`, and `direction`. Each row represents a
    bus stop.
        route_points: a DataFrame that contains the latitude and longitude
    coordinates of the route points along a bus route. Each row in the DataFrame represents a route
    point, and the columns contain the latitude and longitude values.
        segment_id_start: the starting segment ID for the locations.
    It is used to assign a unique identifier to each segment in the output DataFrame.
    
    Returns:
        a pandas DataFrame containing all the locations extracted from the bus stops and route points.
    Each location is associated with a segment number, segment info, direction, and the location
    coordinates.
    """
    # List to store all locations grouped by bus stops and route points in between
    all_locations = []
    k = 0 # this is used to iterate through the route points
    Threshold = 0.001 # in km (1m) # threshold for route points to be considered as bus stops

    # Iterate through the DataFrame to calculate elevations between bus stops
    for i in tqdm(range(len(busStops) - 1), desc="Extracting location coordinates", unit="stop", colour="green"):
        # Get location of two bus stops
        start_point = (busStops.iloc[i]['latitude'], busStops.iloc[i]['longitude'])
        end_point = (busStops.iloc[i+1]['latitude'], busStops.iloc[i+1]['longitude'])

        # Get location from the route points
        start_route_point = (route_points.iloc[k]['latitude'], route_points.iloc[k]['longitude'])
        end_route_point = (route_points.iloc[k+1]['latitude'], route_points.iloc[k+1]['longitude'])

        # Calculate the Euclidean distance between the route end point and the next bus stop
        dist_end_route_to_end_stop = ox.distance.euclidean_dist_vec(end_route_point[0], end_route_point[1], end_point[0], end_point[1])

        if dist_end_route_to_end_stop < Threshold: # if the distance is less than the threshold, then the route point is the next bus stop
            temp_locations = extract_intermediate_locations_from_route(start_route_point, end_route_point)
            # Add all locations to the locations list, with the segment number, segment info, and route segment info
            for location in temp_locations:
                all_locations.append({
                    'segment': segment_id_start,
                    'segment_info': f"{busStops.iloc[i]['stop_id']} - {busStops.iloc[i+1]['stop_id']}",
                    'direction': busStops.iloc[i]['direction'],
                    'location': location
                })
            k += 1
            segment_id_start += 1
            continue
        else:
            j = 0
            # Check if the end point is the last bus stop, or loop through the route points
            dist_start_route_to_end_stop = ox.distance.euclidean_dist_vec(start_route_point[0], start_route_point[1], end_point[0], end_point[1])
            while dist_start_route_to_end_stop > Threshold:
                temp_locations = extract_intermediate_locations_from_route(start_route_point, end_route_point)
                
                # Add all locations to the locations list, with the segment number, segment info, and route segment info
                for location in temp_locations:
                    all_locations.append({
                        'segment':segment_id_start,
                        'segment_info': f"{busStops.iloc[i]['stop_id']} - {busStops.iloc[i+1]['stop_id']}",
                        'route_segment_info': f"{route_points.iloc[k]['point']} - {route_points.iloc[k+1]['point']}",
                        'direction': busStops.iloc[i]['direction'],
                        'location': location
                    })
                j += 1
                k += 1
                # k out of bounds check
                if k == len(route_points) - 1:
                    break
                # update start and end route points
                start_route_point = end_route_point
                end_route_point = (route_points.iloc[k+1]['latitude'], route_points.iloc[k+1]['longitude'])
                dist_start_route_to_end_stop = ox.distance.euclidean_dist_vec(start_route_point[0], start_route_point[1], end_point[0], end_point[1])
        segment_id_start += 1
    
    return pd.DataFrame(all_locations)


###################################################################
## Features max_elevation and avg_elevation extraction

def elevation_from_coordinates(locations):
    """
    return elevation data for given locations formatted as a list of dictionaries using opentopodata API
    
    Args:
        locations: list of coordinates(nodes) along the route [(lat, long), ...]
    
    Returns:
        a list of elevations for the given locations
    """
    # check if the length of locations is greater than 100, if so split into 100 locations and join by |
    locations = [locations[i:i+100] for i in range(0, len(locations), 100)]
    locations = ['|'.join(location) for location in locations]
    
    # for each location in locations, make a request and get the elevation
    elevations = []
    for location in tqdm(locations, desc="Extracting elevation data", colour="green"):
        # API endpoint URL
        url = "https://api.opentopodata.org/v1/srtm90m"

        # JSON payload for POST request
        payload = {
            "locations": location
        }

        # Set headers for POST request
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        # POST request
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if data['results'] != None:
            # Extract elevation data from the response and add it to the DataFrame
            elevations.extend([result['elevation'] for result in data['results']])
        else:
            print("No elevation data found for the given location")
    
    return elevations


def max_avg_elevation(locations_df):
    """
    takes a DataFrame of location data that has 'elevation' column with elevation data
    and calculates the maximum and average elevation for each segment, along with the corresponding latitude and longitude.
    
    Args:
        locations_df: DataFrame that contains information about
        locations, segments, elevations, and route segment information. It should have elevation data as a column.
    
    Returns:
        a DataFrame containing the maximum and average elevation data for each segment in the input
    locations_df DataFrame.
    """
    df = locations_df.copy()
    elevation_out = [] # to store aggregated elevation data

    # Iterate through each unique segment
    for segment_id, segment_data in tqdm(df.groupby('segment'), desc="Extracting max and average elevation", unit="segment", colour="green"):
        segment_info = segment_data['segment_info'].iloc[0]  # Taking the first entry since it's the same for the segment

        if segment_data['route_segment_info'].isnull().all():
            # If all route_segment_info entries are NaN, calculate max elevation for the segment
            max_elevation = segment_data['elevation'].max()
            avg_elevation = segment_data['elevation'].mean()
            max_elevation_index = segment_data['elevation'].idxmax()
            location = segment_data.loc[max_elevation_index, 'location']

            elevation_out.append({
                'segment': segment_id, 
                'segment_info': segment_info, 
                'direction': segment_data['direction'].iloc[0],  # Taking the first entry since it's the same for the segment
                'latitude': location.split(',')[0],
                'longitude': location.split(',')[1],
                'max_elevation': max_elevation,
                'avg_elevation': avg_elevation})
        else:
            # Calculate max elevation for each route_segment_info group within the segment
            route_groups = segment_data.groupby('route_segment_info')
            max_elevations_per_route = route_groups['elevation'].max()
            max_elevation_route_segment = max_elevations_per_route.idxmax()

            max_elevation_data = segment_data[segment_data['route_segment_info'] == max_elevation_route_segment]
            max_elevation = max_elevation_data['elevation'].max()
            avg_elevation = max_elevation_data['elevation'].mean()
            max_elevation_index = max_elevation_data['elevation'].idxmax()
            location = max_elevation_data.loc[max_elevation_index, 'location']
            max_elevation_route_segment = max_elevation_data.loc[max_elevation_index, 'route_segment_info']

            elevation_out.append({
                'segment': segment_id, 
                'segment_info': segment_info, 
                'route_segment_info': max_elevation_route_segment,  # This is the route segment with the max elevation
                'direction': segment_data['direction'].iloc[0],  # Taking the first entry since it's the same for the segment
                'latitude': location.split(',')[0],
                'longitude': location.split(',')[1],
                'max_elevation': max_elevation,
                'avg_elevation': avg_elevation})
    
    return pd.DataFrame(elevation_out)


###################################################################
## Feature segment_gradient_average extraction

def segment_gradient_average(locations_df):
    """
    Calculates the average gradient for each segment in a given dataframe of locations(with elevation data as a column).
    
    Args:
        locations_df: DataFrame that contains information about
        locations, segments, elevations, and route segment information. It should have elevation data as a column.
    
    Returns:
        a DataFrame that contains the segment and the average gradient for each segment.
    """
    df = locations_df.copy()
    
    # Split the "location" column into "latitude" and "longitude" columns
    df[["latitude", "longitude"]] = df["location"].str.split(",", expand=True).astype(float)
    
    # Calculate the vertical difference in elevation (elevation_diff)
    df["elevation_diff"] = df["elevation"].diff().fillna(0)
    
    # used harversine formula to accurately capture earths curvature
    df["distance_diff"] = ox.distance.great_circle_vec(df["latitude"], df["longitude"], df["latitude"].shift(1), df["longitude"].shift(1)).fillna(0)
    
    # Calculate the gradient as vertical difference in elevation divided by horizontal distance
    df["segment_gradient_average"] = df["elevation_diff"] / df["distance_diff"]
    
    # Group by the "segment" column and calculate the mean gradient for each segment
    segment_gradients = df.groupby("segment")["segment_gradient_average"].mean().reset_index()
    
    return segment_gradients


###################################################################
## Feature stop_to_stop_gradient extraction

def stop_to_stop_gradient(locations_df):
    """
    takes a DataFrame of locations and calculates the gradient
    between each stop based on the vertical difference in elevation and horizontal distance.
    
    Args:
        locations_df: DataFrame that contains information about
        locations, segments, elevations, and route segment information. It should have elevation data as a column.
    
    Returns:
        a DataFrame containing the last row of each segment in the input DataFrame, with additional
    columns for latitude, longitude, elevation difference, distance difference, and stop-to-stop
    gradient.
    """
    df = locations_df.copy()
    
    # keep only the first and last rows of each segment
    # Initialize variables to keep track of the first and last rows
    first_row = None
    last_row = None

    # Create a list to store the selected rows
    selected_rows = []

    # Iterate through the DataFrame
    for index, row in df.iterrows():
        # Check if it's the first row of a new segment
        if first_row is None:
            first_row = row
        elif row['segment'] != first_row['segment']:
            # If it's the first row of a new segment, save the last row of the previous segment
            selected_rows.append(first_row)
            selected_rows.append(last_row)
            first_row = row
        last_row = row

    # Append the last row of the last segment
    if first_row is not None:
        selected_rows.append(first_row)
        selected_rows.append(last_row)

    # Create a new DataFrame with the selected rows
    df = pd.DataFrame(selected_rows)    
    
    # Split the "location" column into "latitude" and "longitude" columns
    df[["latitude", "longitude"]] = df["location"].str.split(",", expand=True).astype(float)
    # Calculate the vertical difference in elevation (elevation_diff)
    df["elevation_diff"] = df["elevation"].diff().fillna(0)
    # used harversine formula to accurately capture earths curvature
    df["distance_diff"] = ox.distance.great_circle_vec(df["latitude"], df["longitude"], df["latitude"].shift(1), df["longitude"].shift(1)).fillna(0)
    # Calculate the gradient as vertical difference in elevation divided by horizontal distance
    df["stop_to_stop_gradient"] = df["elevation_diff"] / df["distance_diff"]

    # Group by the "segment" column and get the last row of each group
    stop_to_stop_gradients = df.groupby("segment").tail(1)
    
    return stop_to_stop_gradients


###################################################################
## Feature significant_bend_count extraction

def significant_bend_count(segment_data, threshold):
    """
    calculates the number of significant direction changes in
    a given segment of data based on a threshold value.
    
    Args:
        segment_data: DataFrame containing the latitude and longitude values of consecutive points in a segment. 
    Each row of the DataFrame represents a point, and the columns should include "latitude" and "longitude" to store the
    corresponding coordinates.
        threshold: maximum change in direction between consecutive points that is considered significant. 
    If the change in direction between two consecutive points exceeds this threshold, it is considered a significant bend.
    
    Returns:
        the count of significant bends in the segment data.
    """
    significant_bend_count = 0
    seg_bearings = []
    
    for i in range(len(segment_data) - 1):
        lat1, lon1 = segment_data.iloc[i]["latitude"], segment_data.iloc[i]["longitude"]
        lat2, lon2 = segment_data.iloc[i + 1]["latitude"], segment_data.iloc[i + 1]["longitude"]
        
        # Calculate the bearing between consecutive points and add it to the list
        bearing = ox.bearing.calculate_bearing(lat1, lon1, lat2, lon2)
        seg_bearings.append(bearing)
    for i in range(len(seg_bearings) - 1):
        # Calculate the change in direction between consecutive points
        direction_change = abs((seg_bearings[i] - seg_bearings[i + 1] + 180) % 360 - 180)
        # Check if the change in direction exceeds the threshold
        if direction_change > threshold:
            significant_bend_count += 1
            current_start = i + 1  # Reset the starting point to the next location

    return significant_bend_count


def significant_bend_count_pipeline(locations_df):
    """
    takes a DataFrame of locations, splits the "location"
    column into latitude and longitude columns, groups the data by segment, and calculates the number of
    significant bends in each segment based on a given threshold.
    
    Args:
        locations_df: DataFrame that contains information about
    locations. It should have at least two columns: "location" and "segment". The "location" column
    contains the coordinates of each location in the format "latitude,longitude"
    
    Returns:
        a DataFrame called "segment_bend_counts" which contains two columns: "segment" and
    "significant_bend_count".
    """
    df = locations_df.copy()
    threshold = 90  # degrees
    # Split the "location" column into "latitude" and "longitude" columns
    df[["latitude", "longitude"]] = df["location"].str.split(",", expand=True).astype(float)
    segment_bend_counts = df.groupby("segment").apply(lambda x: significant_bend_count(x, threshold)).reset_index()
    segment_bend_counts.columns = ["segment", "significant_bend_count"]

    return segment_bend_counts


###################################################################

def complete_extraction_pipeline(busStops, route_points, segment_id_start):
    direction = busStops['direction'].iloc[1]
    locations_df = location_extraction_pipeline(busStops, route_points, segment_id_start)
    print("### Step 3/7 ###: Location coordinates extraction completed successfully")
    locations_df['elevation'] = elevation_from_coordinates(locations_df['location'].to_list())
    print("### Step 4/7 ###: Elevation extraction completed successfully")
    #save locations_df to csv
    locations_df.to_csv(f'..\data\\processed\\topological_features\\locations_grouped_by_routes_{direction}.csv', index=False)
    max_avg_elevation_df = max_avg_elevation(locations_df)
    print("### Step 5/7 ###: Max and average elevation extraction completed")
    segment_gradient_average_df = segment_gradient_average(locations_df)
    stop_to_stop_gradient_df = stop_to_stop_gradient(locations_df)
    print("### Step 6/7 ###: Segment gradient average and stop to stop gradient extraction completed")
    significant_bend_count_df = significant_bend_count_pipeline(locations_df)
    print("### Step 7/7 ###: Significant bend count extraction completed")
    # add segment_gradient_average and stop_to_stop_gradient columns to max_avg_elevation_df
    final_elevations_from_locations = max_avg_elevation_df.copy()
    final_elevations_from_locations['segment_gradient_average'] = segment_gradient_average_df['segment_gradient_average'].values
    final_elevations_from_locations['stop_to_stop_gradient'] = stop_to_stop_gradient_df['stop_to_stop_gradient'].values
    final_elevations_from_locations['significant_bend_count'] = significant_bend_count_df['significant_bend_count'].values
    # save elevation_out_df to csv
    final_elevations_from_locations.to_csv(f'..\data\\processed\\topological_features\\topological_features_{direction}.csv', index=False)
    print(f"####### Topological feature extraction for {direction} completed #######")
    print("-------------------------------------------------------")


if __name__ == "__main__":
    print("####### Topological feature extraction pipeline #######")
    print("-------------------------------------------------------")
    # read data
    busStops = pd.read_csv('..\data\\raw\\bus_stops_and_terminals_654.csv')
    route_points = pd.read_csv('..\data\\raw\\route points.csv')
    
    print("### Step 1/7 ###: Data read completed")
    
    # split into up and down route
    split_index = busStops[busStops['stop_id'] == 'BT02'].index[0] 
    KDbusStops = busStops.iloc[:split_index + 1] # Kandy to Digana
    DKbusStops = busStops.iloc[split_index + 1:] # Digana to Kandy

    # split into up and down route
    split_index = route_points[route_points['point'] == 'Digana'].index[0] 
    KDroute_points = route_points.iloc[:split_index + 1] # Kandy to Digana
    DKroute_points = route_points.iloc[split_index + 1:] # Digana to Kandy
    
    print("### Step 2/7 ###: Data split into up and down route completed")
    
    ############ Kandy to Digana direction elevation extraction
    complete_extraction_pipeline(KDbusStops, KDroute_points, 1)

    ############# Digana to Kandy direction elevation extraction
    complete_extraction_pipeline(DKbusStops, DKroute_points, 21)
    