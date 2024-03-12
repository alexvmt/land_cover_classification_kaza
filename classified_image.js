// load roi
var roi  = ee.FeatureCollection('projects/ee-alexvmt/assets/Mufunta');

// Sentinel-2 median composite 2023
var bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12'];
var s2_image = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
	// Set date range according to selected year below
	.filterDate('2023-01-01', '2023-12-31')
	// Pre-filter to get less cloudy granules
	.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
	// Select bands
	.select(bands)
	// Compute median
	.median()
	// Clip roi
	.clip(roi);

var vis_params = {
	min: 0,
	max: 3000,
	bands: ['B4', 'B3', 'B2']
	};

// Prediction
var pred = ee.Image('projects/ee-alexvmt/assets/classified_image');
var palette = [
  '419bdf', // water
  'a59b8f', // bare
  'c4281b', // built up
  'e49635', // cropland
  '88b053', // grass
  'dfc35a', // shrub
  '397d49', // forest
  '7a87c6' // wetland
];

// Mapping
Map.centerObject(roi, 8);
Map.addLayer(s2_image, vis_params, 'Sentinel-2 RGB median composite 2023');
Map.addLayer(pred, {min: 1, max: 8, palette: palette}, 'Land cover map');