# Tobias Mods

Various modifications to Tobias' files as seen in guidance videos.

## Chapter 7 - Case 1

**Python Scripts**
- `azure-ml-inference-arrdel15.py` - modified to work effectively as per video demonstration
- `azure-ml-inference-arrdel15-updated.py` - modified to work effectively as per video demonstration with SDK V2
- `azure-ml-inference-arrdel15-modified-for-csv.py` - skips any processing from within PowerBI (my preference)
- `azure-ml-inference-arrdel15-modified-for-csv-updated` - Uses SDK V2 techniques (FAVOR THIS ONE!!!)

**JSON Files**
Preparations for testing the endpoint (see the swagger file for your endpoint). These are all just guides and examples, none of the scripts reads these.

**Swagger**
These JSON files describe the service endpoints and are useful for developing the endpoint script properly.

**CSV**
Unchanged training and test files from Tobias

**PBI**
Modified PBI files.  I have not adjusted these so that they actually work, I've focused my time in supporting your ability to use the Azure connection scripts.

NOTE: The number of parameters for an endpoint are defined when the AutoML job data inputs are set, as a result, each script would need to be adjusted for the model used.