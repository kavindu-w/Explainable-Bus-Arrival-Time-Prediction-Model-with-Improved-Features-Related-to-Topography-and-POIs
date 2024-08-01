import warnings
import requests # for api calls
import osmnx as ox
from tqdm import tqdm # progress bar
warnings.filterwarnings(action="ignore")
import pandas as pd
import numpy as np

# amenity and tourism tags to extract
amenity_tags =[
    "place_of_worship",
    
    "school",
    "college",
    "university",   
    "kindergarten",
    
    "library",
    
    "hospital",
    
    "clinic",
    "doctors",
    "dentist",
    "pharmacy",
    "veterinary",

    "public_building",
    "shopping_center",
    "marketplace",
    
    "bus_station",
    "taxi",
    "charging_station",
    "ferry_terminal",
    "parking",
    "parking_entrance",
    "parking_space",
    "traffic_park",
    "fuel",

    "hotel",
    "motel",
    "hostel",
    
    "camp_site",
    "cinema",
    "theatre",
    "nightclub",
    "restaurant",
    "cafe",
    "fast_food",
    "pub",


    "post_office",
    "bank",
    "atm",
    "social_facility",

    "public_transport",
    "shelter",
    ]

tourism_tags = [
        "attraction",
        "theme_park",
        "museum",
        "artwork",
        "gallery",
        "aquarium",
        
        "viewpoint",
        "camp_site",
        "picnic_site",
        
        "Information Center", 
        "hotel",
    ]

###################################################################
## Location coordinates extraction

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
            all_locations.append({
                'segment': segment_id_start,
                'segment_info': f"{busStops.iloc[i]['stop_id']} - {busStops.iloc[i+1]['stop_id']}",
                'direction': busStops.iloc[i]['direction'],
                'location': {start_route_point,end_route_point}
            })
            k += 1
            segment_id_start += 1
            continue
        else:
            j = 0
            # Check if the end point is the last bus stop, or loop through the route points
            dist_start_route_to_end_stop = ox.distance.euclidean_dist_vec(start_route_point[0], start_route_point[1], end_point[0], end_point[1])
            while dist_start_route_to_end_stop > Threshold:
                # Add all locations to the locations list, with the segment number, segment info, and route segment info
                all_locations.append({
                    'segment':segment_id_start,
                    'segment_info': f"{busStops.iloc[i]['stop_id']} - {busStops.iloc[i+1]['stop_id']}",
                    'route_segment_info': f"{route_points.iloc[k]['point']} - {route_points.iloc[k+1]['point']}",
                    'direction': busStops.iloc[i]['direction'],
                    'location': {start_route_point,end_route_point}
                })
                j += 1
                k += 1
                start_route_point = end_route_point
                # k out of bound check
                if k == len(route_points) - 1:
                    break
                end_route_point = (route_points.iloc[k+1]['latitude'], route_points.iloc[k+1]['longitude'])
                dist_start_route_to_end_stop = ox.distance.euclidean_dist_vec(start_route_point[0], start_route_point[1], end_point[0], end_point[1])
        segment_id_start += 1
    return pd.DataFrame(all_locations)


###################################################################
## POI extraction

def extract_pois_between_terminals(terminal1_lat, terminal1_long, terminal2_lat, terminal2_long, radius=300):
    """
    The function `extract_pois_between_terminals` extracts Points of Interest (POIs) within a specified
    radius between two terminal points.
    
    Args:
        terminal1_lat: The latitude of the first terminal point.
        terminal1_long: The longitude of the first terminal.
        terminal2_lat: The latitude of the second terminal point.
        terminal2_long: The `terminal2_long` parameter represents the longitude coordinate of the second
        terminal point.
        radius: The radius parameter is the distance in meters from the terminals within which you want to
    extract Points of Interest (POIs). Defaults to 300
    
    Returns:
        The function `extract_pois_between_terminals` returns the Points of Interest (POIs) within the
    specified radius and between the two terminal points.
    """
    # Calculate the bounding box coordinates based on the two terminal points
    north = max(terminal1_lat, terminal2_lat) + radius / 111000  # Approximate meters per latitude degrees at the equator
    south = min(terminal1_lat, terminal2_lat) - radius / 111000
    east = max(terminal1_long, terminal2_long) + radius / (111000 * np.cos(np.radians((terminal1_lat + terminal2_lat) / 2)))  # Approximate longitude degrees per meter
    west = min(terminal1_long, terminal2_long) - radius / (111000 * np.cos(np.radians((terminal1_lat + terminal2_lat) / 2)))

    # Download Points of Interest (POIs) within the bounding box
    tags = {'amenity': amenity_tags, 'tourism': tourism_tags}
    # try to get the pois within the bounding box except when InsufficientResponseError, reduce the radius
    try:
        pois_within_radius = ox.features.features_from_bbox(north, south, east, west, tags)
    except ox._errors.InsufficientResponseError:
        north = max(terminal1_lat, terminal2_lat) + (radius*2) / 111000
        south = min(terminal1_lat, terminal2_lat) - (radius*2) / 111000
        east = max(terminal1_long, terminal2_long) + (radius*2) / (111000 * np.cos(np.radians((terminal1_lat + terminal2_lat) / 2)))
        west = min(terminal1_long, terminal2_long) - (radius*2) / (111000 * np.cos(np.radians((terminal1_lat + terminal2_lat) / 2)))
        
        pois_within_radius = ox.features.features_from_bbox(north, south, east, west, tags)
    
    return pois_within_radius


def append_poi_features(df):
    """
    The `append_poi_features` function takes a DataFrame as input, extracts points of interest (POIs)
    within a certain radius of each terminal location, and appends the extracted POI features to the
    DataFrame.
    
    Args:
        df: The parameter `df` is a DataFrame that contains information about terminals. Each row in the
    DataFrame represents a terminal and contains columns such as 'location', 'amenity_attraction',
    'amenity_hotel', 'attraction_count', and 'hotel_count'. The 'location' column contains the
    coordinates
    
    Returns:
        The function `append_poi_features` returns a new DataFrame `new_df` with additional columns that
    contain information about points of interest (POIs) within a certain radius of each terminal.
    """
    new_df = df.copy()  # Create a copy of the DataFrame
    
    for terminal_index, terminal_row in tqdm(df.iterrows(), desc="Extracting POI features", unit="terminal", colour="green", total=len(df)):

        # split {(7.291186017, 80.63766185), (7.292462226, 80.6349778)} into four attributes terminal 1 lat, terminal 1 long, terminal 2 lat, terminal 2 long
        terminal1_lat = list(terminal_row['location'])[0][0]
        terminal1_long = list(terminal_row['location'])[0][1]
        terminal2_lat = list(terminal_row['location'])[1][0]
        terminal2_long = list(terminal_row['location'])[1][1]
        
        pois_within_radius = extract_pois_between_terminals(terminal1_lat, terminal1_long, terminal2_lat, terminal2_long, radius=300)
        for amenity_type in amenity_tags:
            column_name = f'amenity_{amenity_type}'
            locations = []

            for poi_index, poi_row in pois_within_radius.iterrows():
                # check if amenity column exist poi_row
                if "amenity" in poi_row:
                    # print("amenity column exist in poi_row")
                    if not pd.isnull(poi_row['amenity']) and poi_row['amenity'] == amenity_type:
                        geometry = poi_row['geometry']
                        
                        if geometry.geom_type == 'Point':
                            latitude = geometry.y
                            longitude = geometry.x
                            locations.append(f"{latitude},{longitude}")
                        elif geometry.geom_type == 'Polygon':
                            centroid = geometry.centroid
                            latitude = centroid.y
                            longitude = centroid.x
                            locations.append(f"{latitude},{longitude}")
            with warnings.catch_warnings():
                warnings.simplefilter(action='ignore', category=FutureWarning)
                if locations:
                    new_df.loc[terminal_index, column_name] = '|'.join(locations)
                else:
                    new_df.loc[terminal_index, column_name] = None
        
        attraction_count = 0
        hotel_count = 0
        
        for poi_index, poi_row in pois_within_radius.iterrows():
            if "amenity" in poi_row:
                amenity_type = poi_row['amenity']
                if not pd.isnull(amenity_type):
                    if amenity_type == 'attraction':
                        attraction_count += 1
                    elif amenity_type == 'hotel':
                        hotel_count += 1
        
        new_df.loc[terminal_index, 'attraction_count'] = attraction_count
        new_df.loc[terminal_index, 'hotel_count'] = hotel_count
        
    return new_df


def group_by_segment(df):
    """
    The function `group_by_segment` takes a DataFrame `df` and groups it by the 'segment' column, then
    aggregates the data for each segment by calculating the center location and joining the unique
    values of columns starting with 'amenity_' with '|', and returns the aggregated data as a new
    DataFrame.
    
    Args:
      df: The parameter `df` is a pandas DataFrame that contains the data to be grouped and aggregated.
    It is assumed that the DataFrame has the following columns:
    
    Returns:
      a pandas DataFrame containing aggregated data for each segment in the input DataFrame. The
    aggregated data includes the segment name, segment info, direction, center location, and the set of
    locations for each amenity column starting with 'amenity_'.
    """
    grouped = df.groupby('segment')

    # Initialize a list to store aggregated results
    aggregated_data = []

    # Iterate through groups
    for segment, group_data in grouped:
        # Initialize the dictionary to store aggregated data for this segment
        segment_aggregated = {'segment': segment, 'segment_info': group_data['segment_info'].iloc[0], 'direction': group_data['direction'].iloc[0]}
        
        # Get the set of all locations
        all_locations = set()
        for index, row in group_data.iterrows():
            if pd.notnull(row['location']):
                all_locations.update(row['location'])
        
        # Convert the set to a list
        all_locations_list = list(all_locations)
        
        # Store the first and last locations
        if all_locations_list:
            segment_aggregated['center_location'] = ((all_locations_list[0][0] + all_locations_list[-1][0])/2 , (all_locations_list[0][1] + all_locations_list[-1][1])/2)
        else:
            segment_aggregated['center_location'] = None
        
        # Iterate through columns starting with 'amenity_'
        for col in group_data.columns:
            if col.startswith('amenity_'):
                locations = set()  # Use a set to avoid duplicates
                
                # Iterate through rows in the group
                for index, row in group_data.iterrows():
                    # Check if the cell value is not None
                    if pd.notnull(row[col]):
                        locations.update(row[col].split('|'))
                
                # Join the set of locations with '|'
                segment_aggregated[col] = '|'.join(locations) if locations else None
        
        aggregated_data.append(segment_aggregated)

    return pd.DataFrame(aggregated_data)


###################################################################
## Avg POI distancs and total POI count extraction

def avg_dist_poi_count_extraction(df):
    """
    The function `avg_dist_poi_count_extraction` calculates the average distance between a center
    location and points of interest (POI) in a DataFrame, and also counts the total number of POIs in
    each row.
    
    Args:
      df: The parameter `df` is a DataFrame that contains data related to points of interest (POIs).
    
    Returns:
      a new DataFrame with additional columns 'total_poi_count', 'average_poi_distance', and columns for
    each amenity type in the 'amenity_tags' list.
    """
    new_df = df.copy()  # Create a copy of the DataFrame
    poi_columns = new_df.filter(like='amenity_')
    new_df['total_poi_count'] = poi_columns.count(axis=1)

    def calculate_average_distance(row):
        poi_columns = [col for col in row.index if col.startswith('amenity_') and not pd.isnull(row[col])]
        distances = []
        for col in poi_columns:
            locations = row[col].split('|')
            for location in locations:
                lat, lon = map(float, location.split(','))
                distance = ox.distance.euclidean_dist_vec(row['center_location'][0], row['center_location'][1], lat, lon)
                distances.append(distance)
        if len(distances) > 0:
            return np.mean(distances)
        else:
            return np.nan

    new_df['average_poi_distance'] = new_df.apply(calculate_average_distance, axis=1)

    for amenity_type in amenity_tags:
        column_name = f'amenity_{amenity_type}'
        new_df[column_name] = new_df[column_name].apply(lambda x: (x.count('|') + 1) if isinstance(x, str) else 0)

    return new_df


def group_features(df):
    """
    The function `group_features` takes a DataFrame `df` and groups the counts of different amenity
    types into specific categories, dropping the original amenity columns in the process.
    
    Args:
      df: The parameter `df` is a pandas DataFrame that contains data related to amenities in a certain
    area. It is assumed that the DataFrame has columns starting with "amenity_" followed by the specific
    amenity type. Each row represents a different location or point of interest, and the values in the
    columns indicate
    
    Returns:
      the modified dataframe `df` with additional columns representing the grouped features.
    """
    # Define the list of amenity types for grouping
    amenity_groups = {
        "place_of_worship": ["amenity_place_of_worship"],
        "place_of_education": ["amenity_school", "amenity_college", "amenity_university", "amenity_kindergarten"],
        "hospital" : ["amenity_hospital"],
        "healthcare": ["amenity_hospital", "amenity_clinic", "amenity_doctors", "amenity_dentist", "amenity_pharmacy", "amenity_veterinary"],
        "tourist_attractions": ["amenity_camp_site", "amenity_cinema", "amenity_theatre", "amenity_nightclub", "amenity_restaurant", "amenity_cafe", "amenity_fast_food", "amenity_pub"],
        "commercial_places": [ "amenity_shopping_center", "amenity_marketplace"],
        "nearby_bus_stops": ["amenity_bus_station"],
        "public_places": ["amenity_public_building","amenity_taxi", "amenity_charging_station", "amenity_ferry_terminal", "amenity_parking", "amenity_parking_entrance", "amenity_parking_space", "amenity_traffic_park"],
        "fuel_station": ["amenity_fuel"],   
        "place_of_accommodation": ["amenity_hotel", "amenity_motel", "amenity_hostel"],
    }
    # Iterate through the amenity groups
    for group_name, amenity_list in amenity_groups.items():
        # Sum the counts for the specified amenity types in the group
        df[group_name] = df[amenity_list].sum(axis=1)

    # drop the columns starting with amenity_
    df = df.drop(df.filter(like='amenity_'), axis=1)

    return df




def complete_extraction_pipeline(busStops, route_points, segment_id_start):
    direction = busStops['direction'].iloc[1]
    locations_df = location_extraction_pipeline(busStops, route_points, segment_id_start)
    print("### Step 3/5 ###: Location coordinates extraction completed successfully")
    poi_df = append_poi_features(locations_df)
    
    poi_grouped_df = group_by_segment(poi_df)
    poi_grouped_df.to_csv(f'..\data\\processed\\poi_running\\running_times_poi_with_locations_names_{direction}.csv', index=False)
    
    poi_transformed_df = avg_dist_poi_count_extraction(poi_grouped_df)
    print("### Step 4/5 ###: Avg POI distancs and Total POI count extraction completed")
    
    poi_features_grouped_df = group_features(poi_transformed_df)
    poi_features_grouped_df.to_csv(f'..\data\\processed\\poi_running\\running_times_poi_final_{direction}.csv', index=False)
    print("### Step 5/5 ###: Grouping POI features completed")
    
    print(f"####### POI extraction for {direction} completed #######")
    print("-------------------------------------------------------")


if __name__ == '__main__':
    print("####### Running time POI feature extraction pipeline #######")
    print("-------------------------------------------------------")
    # read data
    busStops = pd.read_csv('..\data\\raw\\bus_stops_and_terminals_654.csv')
    route_points = pd.read_csv('..\data\\raw\\route points.csv')
    
    print("### Step 1/5 ###: Data read completed")
    
    # split into up and down route
    split_index = busStops[busStops['stop_id'] == 'BT02'].index[0] 
    KDbusStops = busStops.iloc[:split_index + 1] # Kandy to Digana
    DKbusStops = busStops.iloc[split_index + 1:] # Digana to Kandy

    # split into up and down route
    split_index = route_points[route_points['point'] == 'Digana'].index[0] 
    KDroute_points = route_points.iloc[:split_index + 1] # Kandy to Digana
    DKroute_points = route_points.iloc[split_index + 1:] # Digana to Kandy
    
    print("### Step 2/6 ###: Data split into up and down route completed")
    
    ####### Kandy to Digana
    complete_extraction_pipeline(KDbusStops, KDroute_points, 1)
    
    ######## Digana to Kandy
    complete_extraction_pipeline(DKbusStops, DKroute_points, 21)