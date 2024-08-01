# %% [markdown]
# #### CS3501 - Data Science and Engineering Project 💻
# 
# ##### Bus Arrival Time Prediction 🚌
# 
# #### How we predict?

# %%
import pandas as pd 
from datetime import time,timedelta
import time as t
import xgboost as xgb
from joblib import load
import emoji

# %%
running_df=pd.read_csv('src//data//demo_trip_running.csv')
dwell_df = pd.read_csv('src//data//demo_trip_dwell.csv')

# %% [markdown]
# #### Load already trained models
# 
# ##### 🚏 bus Stop n-1 =============Segement n================== 🚏 bus stop n                            
# 

# %%
running_model = xgb.XGBRegressor()
dwell_model = xgb.XGBRegressor()
running_model.load_model('src//models//run_time_model_improved.json')
dwell_model.load_model('src//models//dwell_time_model_improved.json')
dwell_scaler = load('src//models//dwell_scaler.bin')
running_scaler = load('src//models//running_scaler.bin')
pca = load('src//models//pca.bin')

# %%
busses = dict()
busses_pred = dict()


for bus in running_df['deviceid'].unique():
    bus_trip = dict()
    pred_bus_trip = dict()

    start_time = running_df.loc[(running_df['segment']==1) & (running_df['deviceid']==bus),"start_time"].values[0]
    bus_trip[100] = start_time
    pred_bus_trip[100] = start_time
    for stop in dwell_df['bus_stop'].unique():
        bus_trip[stop] = None
        pred_bus_trip[stop] = None
    busses[bus] = bus_trip
    busses_pred[bus] = pred_bus_trip




# %%
def is_arrived_last(bus_stop,bus):
    if busses[bus][bus_stop-1]==None:
        return False
    return True

def predict_dwell_time(bus_stop,bus):
    input_features = ['deviceid','day_of_week','time_of_day','Sunday/holiday','weekday/end','bus_stop','precip','temp',
            'dt(n-1)','dt(n-2)', 'dt(n-3)','dt(t-1)', 'dt(t-2)', 'dt(w-1)', 'dt(w-2)', 'dt(w-3)', 'rt(n-1)','total_poi_count']
    feature_values = dwell_df.loc[(dwell_df['bus_stop']==bus_stop) & (dwell_df['deviceid']==bus),input_features]
    dwell_time = dwell_model.predict(dwell_scaler.transform(feature_values))
    return dwell_time[0]

def predict_running_time(bus_stop,bus):
    # 100===1===101===2===102===3===103===4===104===
    segment  = (bus_stop+1)%100
    input_features = ['deviceid','segment','length',
            'rt(n-1)','rt(n-2)', 'rt(n-3)','rt(t-1)', 'rt(t-2)', 'rt(w-1)', 'rt(w-2)', 'rt(w-3)', 'dt(n-1)','max_elevation','avg_elevation',
'total_poi_count', 'average_poi_distance','segment_gradient_average', 'stop_to_stop_gradient','significant_bend_count']
    feature_values = running_df.loc[(running_df['segment']==segment) & (running_df['deviceid']==bus),input_features]
    run_time = running_model.predict(pca.transform(running_scaler.transform(feature_values)))
    return run_time[0]

def predict_arrival_time(bus_stop,bus):
    if (is_arrived_last(bus_stop,bus)):
        if (bus_stop==101):
            dt = 0
        else:
            dt = predict_dwell_time(bus_stop-1,bus)
        rt = predict_running_time(bus_stop-1,bus)
        busses_pred[bus][bus_stop] = dt+rt
        return (round((dt+rt),2))
    else:
        return "Bus has not arrived to the last stop"
def get_real_arrival_time(bus_stop,bus):
    arrival_time = (dwell_df.loc[(dwell_df['bus_stop']==bus_stop) & (dwell_df['deviceid']==bus),'arrival_time']).values[0]
    
    return arrival_time


# %%
def get_minutes(seconds):
    mins = [seconds//60, seconds%60]
    return mins

# %%
def demo(bus):
    bus_stop = 101
    print("==============================================")
    print(f"Bus Arrival time Prediction - Device ID {bus}")

    print (emoji.emojize(":bus: Journey Start time: "), busses[bus][100])

    while (busses[bus][114]==None):

        at = predict_arrival_time(bus_stop,bus)

        at_min = get_minutes(at)

        print("_____________________________________________")

        print(emoji.emojize(":stop_sign: Bus Stop: %d \n :hourglass_not_done: Bus will arrive in %d minutes and %d seconds") %(bus_stop,at_min[0],at_min[1]))
        busses[bus][bus_stop] = get_real_arrival_time(bus_stop,bus)

        t.sleep(at/50) # demo waiting time

        print(emoji.emojize(":check_mark_button: Bus Arrived at: "),busses[bus][bus_stop])
        
        bus_stop+=1



# %%
demo(505)


