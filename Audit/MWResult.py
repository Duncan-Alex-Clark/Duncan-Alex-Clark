#
# File      MWResult.py
#
# Brief     Wrapper/helper functions for the Cognex Barcode Scanner DLL 
# 
# Details   This class wraps the low-level results returned by the Cognex barcode scanner
#           library providing a much easier way to access the data.
#                 
# Notice    Copyright (C) Cognex Corporation 
#
#

from ctypes import *
import struct
import sys

import BarcodeScanner as MWB
class PointF:
    
    def __init__(self, _x = 0.0, _y = 0.0):
        self.x = float(_x)
        self.y = float(_y)
        
class MWLocation:
    def __init__(self, _points):
        
        self.points = []
        for i in range(4):
            p = PointF(_points[i*2],_points[i*2+1])
            self.points.append(p)
            
        self.p1 = self.points[0]
        self.p2 = self.points[1]
        self.p3 = self.points[2]
        self.p4 = self.points[3]
        
class MWResult:
    
    def __init__(self):
        self.text = None
        self.textEncoding = None
        self.typeName = None
        self.rawBytes = None
        self.bytesLength = int(0)
        self.barcodeType = int(0)
        self.subtype = int(0)
        self.imageWidth = int(0)
        self.imageHeight = int(0)
        self.isGS1 = False
        self.locationPoints = None
        self.parserInput = None
    
        self.modulesCountX = int(0)
        self.modulesCountY = int(0)
        self.moduleSizeX = float(0.0)
        self.moduleSizeY = float(0.0)
        self.skew = float(0.0)
        self.iskanji = False
    
        self.barcodeWidth = float(0.0)
        self.barcodeHeight = float(0.0)
    
        self.pdfRows = int(0)
        self.pdfColumns = int(0)
        self.pdfIsTruncated = int(0)
        self.pdfECLevel = int(0)
        self.pdfCodewords = None
    
        
    def setTypeName(self, barcodeType):
        switcher = {
            MWB.FOUND_25_INTERLEAVED: "Code 25 Interleaved",
            MWB.FOUND_25_STANDARD: "Code 25 Standard",
            MWB.FOUND_128: "Code 128",
            MWB.FOUND_128_GS1: "Code 128 GS1",
            MWB.FOUND_39: "Code 39",
            MWB.FOUND_32: "Code 32",
            MWB.FOUND_93: "Code 93",
            MWB.FOUND_AZTEC: "AZTEC",
            MWB.FOUND_DM: "Datamatrix",
            MWB.FOUND_QR: "QR",
            MWB.FOUND_EAN_13: "EAN 13",
            MWB.FOUND_EAN_8: "EAN 8",
            MWB.FOUND_NONE: "None",
            MWB.FOUND_RSS_14: "Databar 14",
            MWB.FOUND_RSS_14_STACK: "Databar 14 Stacked",
            MWB.FOUND_RSS_EXP: "Databar Expanded",
            MWB.FOUND_RSS_LIM: "Databar Limited",
            MWB.FOUND_UPC_A: "UPC A",
            MWB.FOUND_UPC_E: "UPC E",
            MWB.FOUND_PDF: "PDF417",
            MWB.FOUND_CODABAR: "Codabar",
            MWB.FOUND_DOTCODE: "Dotcode",
            MWB.FOUND_11: "Code 11",
            MWB.FOUND_MSI: "MSI Plessey",
            MWB.FOUND_25_IATA: "IATA Code 25",
            MWB.FOUND_ITF14: "ITF 14",
            MWB.FOUND_25_MATRIX: "Code 2/5 Matrix",
            MWB.FOUND_25_COOP: "Code 2/5 COOP",
            MWB.FOUND_25_INVERTED: "Code 2/5 Inverted",
            MWB.FOUND_MAXICODE: "Maxicode",
            MWB.FOUND_QR_MICRO: "Micro QR",
            MWB.FOUND_POSTNET: "Postnet",
            MWB.FOUND_PLANET: "Planet",
            MWB.FOUND_IMB: "Intelligent mail",
            MWB.FOUND_ROYALMAIL: "Royal mail",
            MWB.FOUND_MICRO_PDF: "Micro PDF417",
            MWB.FOUND_AUSTRALIAN: "Australian",
            MWB.FOUND_TELEPEN: "Telepen"
        }
        self.typeName = switcher.get(barcodeType,"Unknown")
        return
        
        
class MWResults:
    
    def __init__(self, buffer):
        self.version = 0
        self.count = 0
        self.results = []
        
        # First 3 characters of the buffer must be 'MWR'
        if buffer.value[0] != ord('M') or buffer.value[1] != ord('W') or buffer.value[2] != ord('R'):
            return
    
        # 4th character is the structure version
        self.version = ord(buffer[3])
        
        # 5th character is the number of results
        self.count = ord(buffer[4])
        
        # The returned fields start at the 6th byte
        pos = 5
        for i in range(self.count):
            result = MWResult()
    
            fieldCount = ord(buffer[pos])
            pos += 1
            for f in range(fieldCount):
                # Each field consists of 5 values:
                #    fieldType - 1 byte
                #    fieldNameLength - 1 byte
                #    fieldName - fieldNameLength bytes
                #    fieldContentLength - 2 bytes
                #    content - fieldContentLenght bytes
                fieldType = ord(buffer[pos])
                fieldNameLength = ord(buffer[pos + 1])
                fieldContentLength = (256 * (ord(buffer[pos + 3 + fieldNameLength]) & 0xFF)) + (ord(buffer[pos + 2 + fieldNameLength]) & 0xFF)
                contentPos = pos + 4 + fieldNameLength
    
                # Not actually used/stored in the results class
                if fieldNameLength > 0:
                    fieldName = buffer[pos+2:pos+2+fieldNameLength].decode("ascii")
                    
                # Barcode contents (as UTF8 string)
                if fieldType == MWB.MWB_RESULT_FT_TEXT:
                    result.text = buffer[contentPos:contentPos+fieldContentLength].decode("utf-8")
            
                # Text Encoding (currenlty only used by QR codes)
                elif fieldType == MWB.MWB_RESULT_FT_TEXT_ENCODING:
                    result.textEncoding = buffer[contentPos:contentPos+fieldContentLength].decode("utf-8")
                    
                # Barcode Type (symbology)
                elif fieldType == MWB.MWB_RESULT_FT_TYPE:
                    result.barcodeType = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)
                    result.setTypeName(result.barcodeType)
            
                # Barcode Subtype (symbology)
                elif fieldType == MWB.MWB_RESULT_FT_SUBTYPE:
                    result.barcodeSubtype = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)
            
                # IsGs1 Code flag
                elif fieldType == MWB.MWB_RESULT_FT_ISGS1:
                    result.isGS1 = (int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder) > 0)

                # Image width (pixels)
                elif fieldType == MWB.MWB_RESULT_FT_IMAGE_WIDTH:
                    result.imageWidth = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)
                
                # Image height (pixels)
                elif fieldType == MWB.MWB_RESULT_FT_IMAGE_HEIGHT:
                    result.imageHeight = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)

                # Barcode location (4 points as floating point percentages)
                elif fieldType == MWB.MWB_RESULT_FT_LOCATION:
                    # Extract 8 floating point numbers
                    locations = []
                    for l in range(8):
                        locations.append(struct.unpack('f', buffer[contentPos + l * 4:contentPos + l * 4 + 4])[0])
                
                    # Now convert to MWLocation points
                    result.locationPoints = MWLocation(locations)
                
                # Barcode contents (raw bytes)
                elif fieldType == MWB.MWB_RESULT_FT_BYTES:
                    result.rawBytes = buffer[contentPos:contentPos+fieldContentLength]
                
                # Parser bytes (hex encoded string)
                elif fieldType == MWB.MWB_RESULT_FT_PARSER_BYTES:
                    result.parserInput = buffer[contentPos:contentPos+fieldContentLength]
                
                # Module count (X axis)
                elif fieldType == MWB.MWB_RESULT_FT_MODULES_COUNT_X:
                    result.modulesCountX = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)
                
                # Module count (y axis)
                elif fieldType == MWB.MWB_RESULT_FT_MODULES_COUNT_Y:
                    result.modulesCount = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)
                
                # Module size in pixels (x axis)
                elif fieldType == MWB.MWB_RESULT_FT_MODULE_SIZE_X:
                    result.moduleSizeX = struct.unpack('f', buffer[contentPos:contentPos+fieldContentLength])[0]
                
                # Module size in pixels (y axis)
                elif fieldType == MWB.MWB_RESULT_FT_MODULE_SIZE_Y:
                    result.moduleSizeY = struct.unpack('f', buffer[contentPos:contentPos+fieldContentLength])[0]

                # Skew
                elif fieldType == MWB.MWB_RESULT_FT_SKEW:
                    result.skew = struct.unpack('f', buffer[contentPos:contentPos+fieldContentLength])[0]
                
                # Is Kanji Encoded flag (QR only)
                elif fieldType == MWB.MWB_RESULT_FT_KANJI:
                    result.kanji = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)
                
                # Barcode width in pixels
                elif fieldType == MWB.MWB_RESULT_FT_BARCODE_WIDTH:
                    result.barcodeWidth = struct.unpack('f', buffer[contentPos:contentPos+fieldContentLength])[0]
                
                # Barcode height in pixels
                elif fieldType == MWB.MWB_RESULT_FT_BARCODE_HEIGHT:
                    result.barcodeHeight = struct.unpack('f', buffer[contentPos:contentPos+fieldContentLength])[0]
                
                # PDF417 only: number of data rows
                elif fieldType == MWB.MWB_RESULT_FT_PDF_ROWS:
                    result.pdfRows = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)
                
                # PDF417 only: number of data columns
                elif fieldType == MWB.MWB_RESULT_FT_PDF_COLUMNS:
                    result.pdfColumns = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)
                
                # PDF417 only: Is Truncated flag
                elif fieldType == MWB.MWB_RESULT_FT_PDF_TRUNCATED:
                    result.pdfTruncated = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)
                
                # PDF417 only: ECC Level
                elif fieldType == MWB.MWB_RESULT_FT_PDF_ECLEVEL:
                    result.pdfECLevel = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)
                
                # PDF417 only: Codewords
                elif fieldType == MWB.MWB_RESULT_FT_PDF_CODEWORDS:
                    listLength = int.from_bytes(buffer[contentPos:contentPos+fieldContentLength],sys.byteorder)
                    result.pdfCodewords = int[listLength+1]
                    result.pdfCodewords[0] = listLength
                
                    for l in range(listLength):
                        result.pdfCodewords[l+1] = int.from_bytes(buffer[contentPos + l * 4:contentPos + l * 4 + 4],sys.byteorder)
                        
                pos += (fieldNameLength + fieldContentLength + 4)
    
            self.results.append(result)
        