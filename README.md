# pybarcode
PyBarcode - a barcode labels printing application written in Python

This is a python script (written in Python 2.7) to print barcode labels. 

I developed this script to print barcodes for laboratory sample tubes where I worked in the past. 

cx_Oracle package is used to connect to Oracle database and win32print package is used to connect to the printers in Windows ecosystem. 

You can connect to any database to fetch the data and print. All your script needs is a proper connection to an existing database that you can connect to. 

Please be wary that since this is Python script, your password and connection string details are exposed (hard coded in this instance). So please follow security measures or find another way to encrypt them. 
