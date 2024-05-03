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

// M1
var s2_composite_m1 = s2_collection
	.filterDate('2023-01-01', '2023-02-01')
	.median()
	.rename(['B2_M1', 'B3_M1', 'B4_M1', 'B5_M1', 'B6_M1', 'B7_M1', 'B8_M1', 'B8A_M1', 'B11_M1', 'B12_M1']);

print(s2_composite_m1.bandNames());

// M2
var s2_composite_m2 = s2_collection
	.filterDate('2023-02-01', '2023-03-01')
	.median()
	.rename(['B2_M2', 'B3_M2', 'B4_M2', 'B5_M2', 'B6_M2', 'B7_M2', 'B8_M2', 'B8A_M2', 'B11_M2', 'B12_M2']);

print(s2_composite_m2.bandNames());

// M3
var s2_composite_m3 = s2_collection
	.filterDate('2023-03-01', '2023-04-01')
	.median()
	.rename(['B2_M3', 'B3_M3', 'B4_M3', 'B5_M3', 'B6_M3', 'B7_M3', 'B8_M3', 'B8A_M3', 'B11_M3', 'B12_M3']);

print(s2_composite_m3.bandNames());

// M4
var s2_composite_m4 = s2_collection
	.filterDate('2023-04-01', '2023-05-01')
	.median()
	.rename(['B2_M4', 'B3_M4', 'B4_M4', 'B5_M4', 'B6_M4', 'B7_M4', 'B8_M4', 'B8A_M4', 'B11_M4', 'B12_M4']);

print(s2_composite_m4.bandNames());

// M5
var s2_composite_m5 = s2_collection
	.filterDate('2023-05-01', '2023-06-01')
	.median()
	.rename(['B2_M5', 'B3_M5', 'B4_M5', 'B5_M5', 'B6_M5', 'B7_M5', 'B8_M5', 'B8A_M5', 'B11_M5', 'B12_M5']);

print(s2_composite_m5.bandNames());

// M6
var s2_composite_m6 = s2_collection
	.filterDate('2023-06-01', '2023-07-01')
	.median()
	.rename(['B2_M6', 'B3_M6', 'B4_M6', 'B5_M6', 'B6_M6', 'B7_M6', 'B8_M6', 'B8A_M6', 'B11_M6', 'B12_M6']);

print(s2_composite_m6.bandNames());

// M7
var s2_composite_m7 = s2_collection
	.filterDate('2023-07-01', '2023-08-01')
	.median()
	.rename(['B2_M7', 'B3_M7', 'B4_M7', 'B5_M7', 'B6_M7', 'B7_M7', 'B8_M7', 'B8A_M7', 'B11_M7', 'B12_M7']);

print(s2_composite_m7.bandNames());

// M8
var s2_composite_m8 = s2_collection
	.filterDate('2023-08-01', '2023-09-01')
	.median()
	.rename(['B2_M8', 'B3_M8', 'B4_M8', 'B5_M8', 'B6_M8', 'B7_M8', 'B8_M8', 'B8A_M8', 'B11_M8', 'B12_M8']);

print(s2_composite_m8.bandNames());

// M9
var s2_composite_m9 = s2_collection
	.filterDate('2023-09-01', '2023-10-01')
	.median()
	.rename(['B2_M9', 'B3_M9', 'B4_M9', 'B5_M9', 'B6_M9', 'B7_M9', 'B8_M9', 'B8A_M9', 'B11_M9', 'B12_M9']);

print(s2_composite_m9.bandNames());

// M10
var s2_composite_m10 = s2_collection
	.filterDate('2023-10-01', '2023-11-01')
	.median()
	.rename(['B2_M10', 'B3_M10', 'B4_M10', 'B5_M10', 'B6_M10', 'B7_M10', 'B8_M10', 'B8A_M10', 'B11_M10', 'B12_M10']);

print(s2_composite_m10.bandNames());

// M11
var s2_composite_m11 = s2_collection
	.filterDate('2023-11-01', '2023-12-01')
	.median()
	.rename(['B2_M11', 'B3_M11', 'B4_M11', 'B5_M11', 'B6_M11', 'B7_M11', 'B8_M11', 'B8A_M11', 'B11_M11', 'B12_M11']);

print(s2_composite_m11.bandNames());

// M12
var s2_composite_m12 = s2_collection
	.filterDate('2023-12-01', '2024-01-01')
	.median()
	.rename(['B2_M12', 'B3_M12', 'B4_M12', 'B5_M12', 'B6_M12', 'B7_M12', 'B8_M12', 'B8A_M12', 'B11_M12', 'B12_M12']);

print(s2_composite_m12.bandNames());

// combine data
var combined_data = s2_composite_m1
	.addBands([s2_composite_m2])
	.addBands([s2_composite_m3])
	.addBands([s2_composite_m4])
	.addBands([s2_composite_m5])
	.addBands([s2_composite_m6])
	.addBands([s2_composite_m7])
	.addBands([s2_composite_m8])
	.addBands([s2_composite_m9])
	.addBands([s2_composite_m10])
	.addBands([s2_composite_m11])
	.addBands([s2_composite_m12]);

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