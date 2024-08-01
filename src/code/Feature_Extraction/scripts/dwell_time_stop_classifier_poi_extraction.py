import numpy as np
import pandas as pd
import warnings
import requests # for api calls
import osmnx as ox
from tqdm import tqdm # progress bar
warnings.filterwarnings(action="ignore")
# Suppress DeprecationWarning related to 'strict' parameter
from requests.exceptions import RequestsDependencyWarning
warnings.simplefilter("ignore", RequestsDependencyWarning)

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


def extract_pois(curr_lat, curr_long, radius=10):
    """
    The function extracts Points of Interest (POIs) within a given radius from a specified latitude and
    longitude.
    
    Args:
      curr_lat: The current latitude of the location you want to extract points of interest from.
      curr_long: The `curr_long` parameter represents the current longitude of the location you want to
    extract Points of Interest (POIs) from.
      radius: The radius parameter is the distance in meters from the current latitude and longitude
    coordinates within which you want to extract points of interest (POIs). Defaults to 10
    
    Returns:
      a list of Points of Interest (POIs) within a specified radius from the given latitude and
    longitude coordinates.
    """
    center_point = (curr_lat, curr_long)
    # Download Points of Interest (POIs) within the bounding box
    tags = {'amenity': amenity_tags, 'tourism': tourism_tags}
    pois_within_radius = ox.features.features_from_point(center_point, tags, dist=radius)

    return pois_within_radius


def append_poi_features(df):
    """
    The function `append_poi_features` takes a DataFrame containing latitude and longitude coordinates,
    extracts points of interest (POIs) within a specified radius of each coordinate, and appends the POI
    locations to the DataFrame as new columns.
    
    Args:
      df: The parameter `df` is a pandas DataFrame that contains information about terminals. It is
    assumed that the DataFrame has columns named 'latitude' and 'longitude' which represent the latitude
    and longitude coordinates of each terminal.
    
    Returns:
      a new DataFrame with additional columns that contain the locations of points of interest (POIs)
    within a certain radius of each terminal.
    """
    new_df = df.copy()  # Create a copy of the DataFrame

    for terminal_index, terminal_row in tqdm(df.iterrows(), desc="Extracting POI features", unit="terminal", colour="green", total=len(df)):
        curr_lat = terminal_row['latitude']
        curr_long = terminal_row['longitude']
        
        pois_within_radius = extract_pois(curr_lat, curr_long, radius=300)
        
        for amenity_type in amenity_tags:
            column_name = f'amenity_{amenity_type}'
            locations = []

            for poi_index, poi_row in pois_within_radius.iterrows():
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

    return new_df


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
                distance = ox.distance.euclidean_dist_vec(row['latitude'], row['longitude'], lat, lon)
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
        "healthcare": ["amenity_hospital", "amenity_clinic", "amenity_doctors", "amenity_dentist", "amenity_pharmacy", "amenity_veterinary"],
        "tourist_attractions": ["amenity_camp_site", "amenity_cinema", "amenity_theatre", "amenity_nightclub", "amenity_restaurant", "amenity_cafe", "amenity_fast_food", "amenity_pub"],
        "commercial_places": ["amenity_public_building", "amenity_shopping_center", "amenity_marketplace"],
        "public_places": ["amenity_bus_station", "amenity_taxi", "amenity_charging_station", "amenity_ferry_terminal", "amenity_parking", "amenity_parking_entrance", "amenity_parking_space", "amenity_traffic_park", "amenity_fuel", "amenity_hotel", "amenity_motel", "amenity_hostel"]
    }
    # Iterate through the amenity groups
    for group_name, amenity_list in amenity_groups.items():
        # Sum the counts for the specified amenity types in the group
        df[group_name] = df[amenity_list].sum(axis=1)

    # drop the columns starting with amenity_
    df = df.drop(df.filter(like='amenity_'), axis=1)

    return df


###################################################################

def complete_extraction_pipeline(busStops):
    direction = busStops['direction'].iloc[1]
    poi_df = append_poi_features(busStops)
    poi_df.to_csv(f'..\data\\processed\\poi_dwell\dwell_times_poi_with_locations_names_{direction}.csv', index=False)
    print("### Step 4/5 ###: POI features extraction completed successfully")
    
    poi_transformed_df = avg_dist_poi_count_extraction(poi_df)
    print("### Step 5/5 ###: Avg POI distancs and Total POI count extraction completed")
    
    poi_features_grouped_df = group_features(poi_transformed_df)
    poi_features_grouped_df.to_csv(f'..\data\\processed\\poi_dwell\dwell_times_poi_final_{direction}.csv', index=False)
    print("### Step 5/5 ###: Grouping POI features completed")
    
    print(f"####### POI extraction for {direction} completed #######")
    print("-------------------------------------------------------")


if __name__ == '__main__':
    print("####### Dwell time stop classifier POI feature extraction pipeline #######")
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
    
    print("### Step 2/5 ###: Data split into up and down route completed")
    
    ####### Kandy to Digana
    complete_extraction_pipeline(KDbusStops)
    
    ######## Digana to Kandy
    complete_extraction_pipeline(DKbusStops)