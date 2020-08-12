// Prepare data
var AOI =  ee.FeatureCollection("users/kolesovdm/AreasOfInterest/habAOI");
var collection = ee.ImageCollection("COPERNICUS/S2");
collection = collection.filter(ee.Filter.date('2019-01-20', '2019-01-30'));
collection = collection.filterBounds(AOI);

var composite = collection.median();
Export.image.toCloudStorage({
  image: composite, 
  description: 'composite_2019_01_25', 
  bucket: 'gee4avral', 
  fileNamePrefix: 'Source/composite_2019_01_25', 
  region: AOI.geometry().bounds(), 
  scale: 10, 
  maxPixels: 1e13
});
