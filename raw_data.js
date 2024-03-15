// load roi and labeled points
var roi  = ee.FeatureCollection('projects/ee-alexvmt/assets/Mufunta');
var labeled_points = ee.FeatureCollection('projects/ee-alexvmt/assets/Mufunta-sample-data-POL_20240213');

// set start and end date
var start_date = '2023-01-01';
var end_date = '2023-12-31';

// define relevant bands
var s2_bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12'];

// get Sentinel-2 imagery for roi for specified date range with max 20% cloud cover and for selected bands
var s2_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
	.filterBounds(roi)
	.filterDate(start_date, end_date)
	.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
	.select(s2_bands);

// rainy season
var s2_composite_rainy_season_part_1 = s2_collection
  .filterDate('2023-01-01', '2023-04-01');

var s2_composite_rainy_season_part_2 = s2_collection
  .filterDate('2023-11-15', '2024-01-01');
	
var s2_composite_rainy_season = s2_composite_rainy_season_part_1.merge(s2_composite_rainy_season_part_2)
  .median()
	.rename(['B2_rainy', 'B3_rainy', 'B4_rainy', 'B5_rainy', 'B6_rainy', 'B7_rainy', 'B8_rainy', 'B8A_rainy', 'B11_rainy', 'B12_rainy']);

print(s2_composite_rainy_season.bandNames());

// dry season
var s2_composite_dry_season = s2_collection
  .filterDate('2023-04-01', '2023-11-15')
	.median()
	.rename(['B2_dry', 'B3_dry', 'B4_dry', 'B5_dry', 'B6_dry', 'B7_dry', 'B8_dry', 'B8A_dry', 'B11_dry', 'B12_dry']);

print(s2_composite_dry_season.bandNames());

// combine data
var combined_data = s2_composite_rainy_season.addBands([s2_composite_dry_season]);

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