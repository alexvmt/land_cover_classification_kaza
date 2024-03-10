// load roi and labeled points
var roi  = ee.FeatureCollection('projects/ee-alexvmt/assets/Mufunta');
var labeled_points = ee.FeatureCollection('projects/ee-alexvmt/assets/Mufunta-sample-data-POL_20240213');

// set start and end date
var start_date = ee.Date('2023-01-01');
var end_date = ee.Date('2023-12-31');

// create Sentinel-2 median composite for roi for specified date range with max 20% cloud cover and for selected bands
var s2_bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12'];
var s2_composite = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
	.filterBounds(roi)
	.filterDate(start_date, end_date)
	.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
	.select(s2_bands)
	.median();

// sample data for labeled points
var sampled_data = s2_composite.sampleRegions({
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
