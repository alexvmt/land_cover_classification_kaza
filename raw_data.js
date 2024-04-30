// load roi and labeled points
var roi  = ee.FeatureCollection('projects/ee-alexvmt/assets/Mufunta');
var labeled_points = ee.FeatureCollection('projects/ee-alexvmt/assets/Mufunta-sample-data-POL_20240213');

// set start and end date
var start_date = '2023-01-01';
var end_date = '2024-01-01';

// define relevant bands
var s2_bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12'];

// get Sentinel-2 imagery for roi for specified date range with max 20% cloud cover and for selected bands
var s2_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
	.filterBounds(roi)
	.filterDate(start_date, end_date)
	.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
	.select(s2_bands);

// Q1
var s2_composite_q1 = s2_collection
	.filterDate('2023-01-01', '2023-04-01')
	.median()
	.rename(['B2_Q1', 'B3_Q1', 'B4_Q1', 'B5_Q1', 'B6_Q1', 'B7_Q1', 'B8_Q1', 'B8A_Q1', 'B11_Q1', 'B12_Q1']);

print(s2_composite_q1.bandNames());

// Q2
var s2_composite_q2 = s2_collection
	.filterDate('2023-04-01', '2023-07-01')
	.median()
	.rename(['B2_Q2', 'B3_Q2', 'B4_Q2', 'B5_Q2', 'B6_Q2', 'B7_Q2', 'B8_Q2', 'B8A_Q2', 'B11_Q2', 'B12_Q2']);

print(s2_composite_q2.bandNames());

// Q3
var s2_composite_q3 = s2_collection
	.filterDate('2023-07-01', '2023-10-01')
	.median()
	.rename(['B2_Q3', 'B3_Q3', 'B4_Q3', 'B5_Q3', 'B6_Q3', 'B7_Q3', 'B8_Q3', 'B8A_Q3', 'B11_Q3', 'B12_Q3']);

print(s2_composite_q3.bandNames());

// Q4
var s2_composite_q4 = s2_collection
	.filterDate('2023-10-01', '2024-01-01')
	.median()
	.rename(['B2_Q4', 'B3_Q4', 'B4_Q4', 'B5_Q4', 'B6_Q4', 'B7_Q4', 'B8_Q4', 'B8A_Q4', 'B11_Q4', 'B12_Q4']);

print(s2_composite_q4.bandNames());

// combine data
var combined_data = s2_composite_q1
	.addBands([s2_composite_q2])
	.addBands([s2_composite_q3])
	.addBands([s2_composite_q4]);

print(combined_data.bandNames());

// sample data for labeled points
var sampled_data = combined_data.sampleRegions({
	collection: labeled_points,
	properties: ['Landcover', 'LC_Out', 'LC_Nr'],
	tileScale: 16,
	scale: 10,
	geometries: true
});

// export sampled data to drive as csv
Export.table.toDrive({
	collection: sampled_data,
	description: 'raw_data',
	fileFormat: 'CSV'
});