# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 10:39:59 2017
@author: Phani Atmakur

PyBarcode - Python Barcode Labels Printing.
"""
import sys, os, win32print, cx_Oracle, re


printer_name = win32print.GetDefaultPrinter ()
db_con = cx_Oracle.connect('username', 'password', 'server address - (IP) or hostname')
cursor = db_con.cursor()

print ">_________________________________________________________<"
print "| PYBARCODE VER.1.1. {Py2.7}                              |"
print "| PyBarcode reads user input, fetches data from database  |"
print "| and prints a barcode with respective identifiers on it. |"
print "|_________________________________________________________|" 
print "\n"



#Reads input from user.
#----------------------
def read_scannerdata():
    #keyboard_input = str(raw_input())
    print "*********************************************************"
    print "Enter ID or scan a barcode:"
    print "*********************************************************"
    keyboard_input = str(raw_input())
    print "---------"
    print "ID: " + keyboard_input.upper()
    feedto_printer(get_data(keyboard_input.upper()), keyboard_input)


#Retrieves data from Oracle database.
#------------------------------------
def get_data(data):
    ids = []
    query = "SELECT * \
             FROM   ITEMS \
             WHERE  INVENTORY_ID =:sub_query"

    sub_query = "SELECT * FROM DELIVERIES WHERE REQUEST_NUMBER=:REQUEST_NUMBER"

    cursor.execute(sub_query, {'REQUEST_NUMBER':data})
    for row in cursor:
        ids.append(row[0])
        

    cursor.execute(query, {'sub_query':ids[0]})
    for item in cursor:
        ids.append(item[0]) 
    
    return ids


#Prints data to a barcode along with identifiers.
#------------------------------------------------
def feedto_printer(req_data, keyboard_input):
    print "DATA    : %r " % req_data
    if req_data == [None]:
        print "INVALID INPUT (OR) BARCODE SCANNED.\nPLEASE TRY AGAIN."
        #print "*********************************************************"
        print "\n"
        read_scannerdata()

    else:
        print "NHI     : " + req_data[0], "\nNAME    : " + req_data[1]
        print "\n"
        #print "*********************************************************"

        barcode = str(req_data[0])
        name = str(req_data[1])
    
        # Barcode printer data feed format
        code128_format = 'N' + '\n' \
        + 'MD25' + '\n' \
        + 'B300,60,0,1,2,2,50,B,"' + name[:12] + '"' + '\n' \
        + 'A310,01,0,3,2,2,N,"' + inventory_id + '"' + '\n' \
        + 'P1' + '\n'

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


        double_label = '^XA' + '\n' \
        + '^MMT' + '\n' \
        + '^PW783' + '\n' \
        + '^LL0216' + '\n' \
        + '^LS0' + '\n' \
        + '^FT438,44^A0N,28,28^FB181,1,0^FH\^FN2^FD' + keyboard_input.upper() + '^FS' + '\n' \
        + '^FT33,46^A0N,28,28^FB180,1,0^FH\^FN2^FD' + keyboard_input.upper() + '^FS' + '\n' \
        + '^BY2,3,59^FT52,120^BCN,,N,N,N,A' + '\n' \
        + '^FN8^FD' + keyboard_input.upper() + '^FS' + '\n' \
        + '^BY2,3,59^FT450,118^BCN,,N,N,N,A' + '\n' \
        + '^FN8^FD' + keyboard_input.upper() + '^FS'  + '\n' \
        + '^FT32,151^A0N,17,16^FB173,1,0^FH\^FN6^FDSURN  : ' + name[6:12] + '^FS' + '\n' \
        + '^FT31,180^A0N,17,16^FB149,1,0^FH\^FN7^FDNAME: ' + name[:6] + '^FS' + '\n' \
        + '^FT438,149^A0N,17,16^FB173,1,0^FH\^FN7^FDSURN  : ' + name[6:12] + '^FS' + '\n' \
        + '^FT437,178^A0N,17,19^FB172,1,0^FH\^FN7^FDNAME: ' + name[:6] + '^FS'  + '\n' \
        + '^FT212,152^A0N,17,26^FB130,1,0^FH\^FN9^FD' + inventory_id + '^FS' + '\n' \
        + '^FT618,180^A0N,17,24^FB137,1,0^FH\^FN10^FD' + '^FS' + '\n' \
        + '^FT207,180^A0N,17,24^FB137,1,0^FH\^FN10^FD' + '^FS' + '\n' \
        + '^FT617,150^A0N,17,28^FB143,1,0^FH\^FN9^FD' + inventory_id + '^FS' + '\n' \
        + '^XZ'
        
        datamatrix = '~SD' + str(32) + '\n' \
        + '^XA' + '\n' \
        + '^FO370,70^A0N,30,25^FD' + name + '^FS' + '\n' \
        + '^FO370,100^ADN,9,5^FD' + inventory_id[:12] + '^FS' + '\n' \
        + '^FO390,10^BQN,2,2,Q,7^FDQA,' + name + '^FS' + '\n' \
        + '^XZ'

        
        if sys.version_info >= (3,):
            raw_data = bytes (single_label, "utf-8")
        else:
            raw_data = DATA
    
        hPrinter = win32print.OpenPrinter (printer_name)
        try:
            hJob = win32print.StartDocPrinter (hPrinter, 1, (DATA, None, "RAW"))
            try:
                win32print.StartPagePrinter (hPrinter)
                win32print.WritePrinter (hPrinter, raw_data)
                win32print.EndPagePrinter (hPrinter)
            finally:
                win32print.EndDocPrinter (hPrinter)
        finally:
            win32print.ClosePrinter (hPrinter)
            read_scannerdata()
     
read_scannerdata()
