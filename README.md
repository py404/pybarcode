# pybarcode
PyBarcode - a barcode labels printing application written in Python

This is a python script (written in Python 2.7) to print barcode labels (tested and works on Zebra label printers). 

I developed this script to print barcodes for laboratory sample tubes where I worked in the past. 

cx_Oracle package is used to connect to Oracle database and win32print package is used to connect to the printers in Windows ecosystem. 

You can connect to any database to fetch the data and print. All your script needs is a proper connection to an existing database that you can connect to. 

Please be wary that since this is Python script, your password and connection string details are exposed (hard coded in this instance). So please follow security measures or find another way to encrypt them. 


## ZPL Code breakdown
I have use Zebra's ZPL language to print the barcodes.

### Code 128 breakdown
Example:
```raw
single_label = '^XA' + '\n' \
+ '^MMT' + '\n' \
+ '^PW783' + '\n' \
+ '^LL0216' + '\n' \
+ '^LS0' + '\n' \
+ '^FT238,44^A0N,28,28^FB181,1,0^FH\^FN2^FD' + keyboard_input.upper() + '^FS' + '\n' \
+ '^FT13,46^A0N,28,28^FB180,1,0^FH\^FN2^FD' + inventory_id + '^FS' + '\n' \
+ '^BY2,3,59^FT250,118^BCN,,N,N,N,A' + '\n' \
+ '^FN8^FD' + keyboard_input.upper() + '^FS'  + '\n' \
+ '^FT238,149^A0N,17,16^FB173,1,0^FH\^FN7^FDSURN  : ' + name[6:12] + '^FS' + '\n' \
+ '^FT238,178^A0N,17,19^FB172,1,0^FH\^FN7^FDNAME: ' + name[:6] + '^FS'  + '\n' \
+ '^FT418,180^A0N,17,24^FB137,1,0^FH\^FN10^FD' + '^FS' + '\n' \
+ '^FT418,150^A0N,17,28^FB143,1,0^FH\^FN9^FD' + inventory_id + '^FS' + '\n' \
+ '^XZ'
```

- MM = print mode, combine with T (^MMT) => Printer mode + Tear off
- PW783
  - PW = Print Width, combine with 783 => (^PW783) => printer label width set to 783 dots (dots are Zebra specific, please refere Zebra ZPL programming guide)
- LL0216
  - LL = Label Length, combine with desired value => (^LL0216) => set label label (Y-axis position)
- LS0 = Label Shift, combine with a value => if 0, starts label from Y=0
- FT = Field Position
and so on...

For reference, please have a look here: https://www.zebra.com/content/dam/zebra/manuals/printers/common/programming/zpl-zbi2-pm-en.pdf

You will find a best example on page 48. 

I tinkered around a lot with a lot of spare label ribbons and figured out the best suitable configuration for me. 
