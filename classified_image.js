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
var pred = ee.Image('projects/ee-alexvmt/assets/classified_image').clip(roi);
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
Map.centerObject(roi, 9);
Map.addLayer(s2_image, vis_params, 'Sentinel-2 RGB median composite 2023');
Map.addLayer(pred, {min: 1, max: 8, palette: palette}, 'Land cover map');



// set position of panel
var legend = ui.Panel({
  style: {
    position: 'bottom-left',
    padding: '8px 15px'
  }
});

// Create legend title
var legendTitle = ui.Label({
  value: 'Legend',
  style: {
    fontWeight: 'bold',
    fontSize: '18px',
    margin: '0 0 4px 0',
    padding: '0'
    }
});

// Add the title to the panel
legend.add(legendTitle);
    
// Creates and styles 1 row of the legend.
var makeRow = function(color, name) {
      
      // Create the label that is actually the colored box.
      var colorBox = ui.Label({
        style: {
          backgroundColor: '#' + color,
          // Use padding to give the box height and width.
          padding: '8px',
          margin: '0 0 4px 0'
        }
      });
      
      // Create the label filled with the description text.
      var description = ui.Label({
        value: name,
        style: {margin: '0 0 4px 6px'}
      });
      
      // return the panel
      return ui.Panel({
        widgets: [colorBox, description],
        layout: ui.Panel.Layout.Flow('horizontal')
      });
};

// name of the legend
var names = ['Water', 'Bare', 'Built up', 'Cropland', 'Grass', 'Shrub', 'Forest', 'Wetland'];

// Add color and and names
for (var i = 1; i < 8; i++) {
  legend.add(makeRow(palette[i], names[i]));
  }  

// add legend to map (alternatively you can also print the legend to the console)  
Map.add(legend);