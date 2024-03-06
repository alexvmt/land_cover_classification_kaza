// load data
var study_aoi  = ee.FeatureCollection('projects/ee-alexvmt/assets/Mufunta');
var sample_shp = ee.FeatureCollection('projects/ee-alexvmt/assets/Mufunta-sample-data-POL_20240213');

// center on area of interest
Map.centerObject(study_aoi, 8);

// set start and end dates
var startDate = '2023-01-01';
var endDate = '2023-12-31';

var date_start = ee.Date(startDate);
var date_end= ee.Date(endDate);

// select S2 bands by AOI, for the year 2023 and filtering only images with max 20% cloud cover
var s2_bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12'];
var s2_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
	.filterBounds(study_aoi)
	.filterDate(startDate,endDate)
	.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))
	.select(s2_bands)
	.median();

// generate training pixels data
var sampling_data = s2_collection.sampleRegions({
	collection: sample_shp,
	properties: ['Landcover',' LC_Out', 'LC_Nr'],
	tileScale: 16,
	scale: 10,
	geometries: true
});

// split data into training and validation groups. Set at 70% training/30% validation
var splitData = function(data){
	
	var dict = {};
	var randomTpixels = data.randomColumn(); 
	var trainingData = randomTpixels.filter(ee.Filter.lt('random', 0.7));
	var valiData = randomTpixels.filter(ee.Filter.gte('random', 0.7));

	
	dict.training = trainingData;
	dict.validation = valiData;
	
	return dict;
	
};

var ValTestData = splitData(sampling_data);

// export data
Export.table.toDrive({
	collection: ValTestData.training,
	description: 'ClassPrototype_Mafunta_Training',
	folder: 'TestFolder',
	fileFormat: 'CSV'
});

Export.table.toDrive({
	collection: ValTestData.validation,
	description: 'ClassPrototype_Mafunta_Validation',
	folder: 'TestFolder',
	fileFormat: 'CSV'
});
