---
applyTo: "**/*.postman_collection.json,output/**,context/**,context/*.py,context/*.csv"
---

# Test Data Generation Instructions

## Generation of shipments with alta-preenvios-api-apiode
- Each time shipments are generated with the mentioned API, prompt for the following variables:
  - Contract to use (show available contracts)
  - Number of packages
  - Whether to include optional data (boolean)
  If the data is not provided, use default values from the sample request in context/Envios.postman_collection.json