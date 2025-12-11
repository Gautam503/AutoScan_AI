TCP Barcode Scanner → SAP Integration (Python)

This project is a lightweight TCP server written in Python that listens for barcode/engine-number data sent from a barcode scanner or Cognex vision system.
Once the data is received, the script adds a prefix & suffix, processes the value, and then sends it to an SAP endpoint using a POST API request.

This can be used in manufacturing/assembly lines where engine/chassis numbers must be validated or uploaded to SAP.
