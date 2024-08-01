# Explainable Bus Arrival Time Prediction Model with Improved Features Related to Topography and Points of Interest

## Usage

Step 1: Install the library
```bash
pip install gps2topo-poi
```

Step 2: Import the library
```python
import gps2topo_poi as g2p

# dwell time POIs extraction
g2p.dwell_time_stop_classifier_poi_extraction.complete_extraction_pipelinecomplete_extraction_pipeline(bus_stops_path, segment_id_start=1)

# running time POIs extraction
g2p.running_time_poi_extraction.complete_extraction_pipeline(bus_stops_path, route_points_path, segment_id_start=1)

# Topographical feature extraction
g2p.topological_feature_extraction.complete_extraction_pipeline(bus_stops_path, route_points_path, segment_id_start=1)
```

## Abstract
Accurate and reliable prediction of bus arrival times enhances passenger mobility experience. This study addresses a significant research gap by focusing on the complexities of predicting bus arrival times in heterogeneous
traffic conditions. Unlike conventional prediction models, this research identifies hidden features related to topographical and Points of Interest (POIs) data, recognizing their critical role
in reasoning. The methodology involves a two-fold approach, segmenting predictions into running time within a segment and dwell time at bus halts, using the multi-model ensemble
technique. The results indicate that incorporating the new features (5 topographical and 10 POIs-related) has improved model performance by a reduction in MAE of 1.37 seconds
(dwell time) and a decrease in MAPE by 0.7% (running time). While the enhancements in accuracy may appear modest, our focus lies on examining the influence of new features, offering
valuable insights into the factors that cause delays. Moreover, we developed a dashboard showcasing real-time bus arrival times and highlighting delay reasoning using explainable AI
techniques.


## Results
<div id="results" style= ""padding:15pt"> 
  <h3>  Performance of Running Time Prediction with and without Topographical and POIs Data </h3>
  <table>
    <tr>
      <th>XGBoost Model</th>
      <th>RMSE (s)</th>
      <th>MAE (s)</th>
      <th>MAPE (%)</th>
      <th>R2</th>
    </tr>
    <tr>
      <td>Without topographical & POIs features</td>
      <td>57.55</td>
      <td>37.19</td>
      <td>23.11</td>
      <td>0.76</td>
    </tr>
    <tr>
      <td>With topographical & POIs (total 25 features)</td>
      <td>57.14</td>
      <td>36.64</td>
      <td><b>22.06</b></td>
      <td>0.76</td>
    </tr>
    <tr>
      <td>With topographical & POIs (total 19 features)</td>
      <td><b>56.99</b></td>
      <td><b>36.56</b></td>
      <td>22.12</td>
      <td>0.76</td>
    </tr>
  </table> 

  <h3>  Performance of Dwell Time Prediction with and without POIs Data </h3>
  <table>
    <tr>
      <th>XGBoost Model</th>
      <th>RMSE (s)</th>
      <th>MAE (s)</th>
      <th>R2</th>
    </tr>
    <tr>
      <td>Without POIs features</td>
      <td><b>38.13</b></td>
      <td>19.77</td>
      <td>0.14</td>
    </tr>
    <tr>
      <td>Original features with total_poi_count</td>
      <td>38.2</td>
      <td><b>19.6</b></td>
      <td>0.14</td>
    </tr>
    
  </table> 
</div>

## Authors

- A.K. Warnakulasuriya - Department of Computer Science and Engineering, University of Moratuwa, Sri Lanka
- C.D.R.M. Weerasinghe - Department of Computer Science and Engineering, University of Moratuwa, Sri Lanka
- H.K.G.V.L. Wickramarathna - Department of Computer Science and Engineering, University of Moratuwa, Sri Lanka
- Shiveswarran Ratneswaran - Department of Computer Science and Engineering, University of Moratuwa, Sri Lanka
- Dr. Uthayasanker Thayasivam - Department of Computer Science and Engineering, University of Moratuwa, Sri Lanka