# Tobias Mods

Various modifications to Tobias' files as seen in guidance videos.

## Chapter 7 - Case 1

**Python Scripts**
- `azure-ml-inference-arrdel15.py` - modified to work effectively as per video demonstration
- `azure-ml-inference-arrdel15-modified-for-csv.py` - skips any processing from within PowerBI (my preference)

**JSON Files**
Preparations for testing the endpoint (see the swagger file for your endpoint)

**CSV**
Unchanged training and test files from Tobias

**PBI**
Modified PBI files

NOTE: The number of parameters for an endpoint are defined when the AutoML job data inputs are set, as a result, each script would need to be adjusted for the model used.