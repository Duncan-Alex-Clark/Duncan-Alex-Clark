#!/usr/bin/python3
#
# Note     The start of the script needs to point to your python 3 installation on Linux
#          and depending on your version this path might be different. Likewise, the script files
#          need to use the Unix EOL ('\n') as opposed to windows EOL ("\r\n").
#          Windows doesn't have an issue with this, but the interpreter on Linux is not able
#          to work with windows EOL.
#
# File      pythonDemo.py
# Brief     Sample Python program for barcode decoding libary (Windows DLL/Linux Shared Library)
#
# Details   This is a simple demonstration program for using the Cognex Moblie Barcode SDK core decoder library
#           (formally the Manatee Works Barcode Scanner Libary, or mwLib). The application takes a single image
#           file as input, loads it into memory, converting it to grayscale, then decodes it using the 
#           specified configuration (barcode types, multicode features, etc.). This is not a comprehensive demo
#           of all of the SDK's features, but rather an example of how to use the library to decode barcodes
#           from an image file.
#           
#           This example is based on Python 3 and relies on the Python Image Library (Pillow) for image handling;
#           it must be installed:
#
#               Windows: python -m pip install --upgrade Pillow
#                        python -m pip install --upgrade pip
#               Visual Studio: (issue commands above in the VS's installed Python directory; this directory
#                        is shown in the Full Path property of the Python Environments of the project)
#               Linux:   sudo apt-get install python3-pil
#                           or
#                        sudo yum install python3-pil
#
# Notes     The barcode scanner library is loaded when BarcodeScanner.py is imported (it can then create all the 
#           libray function definitions). By default, the correct library for the current architecture is loaded 
#           (either 32-bit or 64-bit, Windows or Linux) relative to the current folder and based on the structure
#           of the sample project. This means the Linux shared libraries are assumed to be in ../lib/x86/32bit
#           and ../lib/x86/64bit, while the Windows DLL's are assumed to be in ../DLL/32bit and ../DLL/64bit
#
#           If you have located the library in a different location, modify BarcodeScanner.py
# 
# Notice    Copyright (C) Cognex Corporation 
#
import sys
import time
from ctypes import *
from PIL import Image, ImageDraw
from os import path

import BarcodeScanner as MWB
import MWParser as MWP
import MWResult as MWR

effortLevel = 4
useMultiCode = False
useTiles = False
suppressOutput = False
writeImage = False
tilesX = 6
tilesY = 6
overlap = 6
maxThreads = 4

argc = len(sys.argv)

# Display usage message
if argc < 2:
    print("usage: pythonDemo [-En] [-M] [-S] [-T] [-Xn] [-Yn] [-On] [-Rn] [-W] filename\n\n" +
          "    -En         Effort level (1-5, default "+str(effortLevel)+")\n" +
          "    -M          Enable multi-code\n" +
          "    -S          Suppress barcode results\n" +
          "    -T          Generate tiled regions\n" +
          "    -Xn         Tiles X dimension (default "+str(tilesX)+")\n" +
          "    -Yn         Tiles Y dimension (default "+str(tilesY)+")\n" +
          "    -On         Tiles overlap percentage  (default "+str(overlap)+")\n" +
          "    -Rn         Maximum threads tiles/regions (default "+str(maxThreads)+")\n" +
          "    -W          Write output image\n" +
          "    filename    Image file to scan for barcodes\n\n")
    exit()

# Parse the parameters
#
# There are much more elegant and foolproof ways to process command line arguments; but this 
# is just a simple sample application.  :)
#
for x in range(argc-2):
    arg = sys.argv[x+1]
    
    # Effort level (assume 3rd character is 1-5)
    if arg[0:2].upper() == "-E":
        effortLevel = int(arg[2:])

    # Enable multicode?        
    elif arg[0:2].upper() == "-M":
        useMultiCode = True
    
    # Suppress output?
    elif arg[0:2].upper() == "-S":
        suppressOutput = True
        
    # Enable tiles (and subsequently, multicode)?
    elif arg[0:2].upper() == "-T":
        useTiles = True

    # Set tiles X
    elif arg[0:2].upper() == "-X":
        tilesX = int(arg[2:])

    # Set tiles Y
    elif arg[0:2].upper() == "-Y":
        tilesY = int(arg[2:])

    # Set overlap
    elif arg[0:2].upper() == "-O":
        overlap = int(arg[2:])

    # Set maximum threads
    elif arg[0:2].upper() == "-R":
        maxThreads = int(arg[2:])

    # Write image with located barcodes?
    elif arg[0:2].upper() == "-W":
        writeImage = True
    
# Last argument must be the image file name
fileName = sys.argv[argc-1]

# Does the image file exist?
if not path.isfile(fileName):
    print("Unable to load image " + fileName)
    exit()

print("Loading image...", end='')
starTime = time.time()

# Load the image, converting to grayscale as we do
grayScale = Image.open(fileName).convert('L')

# Get the image as a bytes object
pixels = grayScale.tobytes()

endTime = time.time()
totalMS = (endTime - starTime) * 1000
print(" (%.2f" % totalMS + " ms)")


# Initialize the SDK with the license key.
#
#   Visit https://cmbdn.cognex.com to obtain a trial license key--without a valid, active license key
#   barcode scan results will be masked with '*' characters and some features, like multi-code, may 
#   not be enabled at all. Replace '<your key here>' below with your license key string.
#
status = MWB.MWBregisterSDK(b'<your key here>')
if status != MWB.MWB_RTREG_OK:
    print("MWBregisterSDK returned " + str(status) + "; scan results will be masked and some features may not be available")
   

# Active codes
#
#  You must specify which symbologies the decoder is to look for; no symbologies are enabled by default. The parameter
#  to MWBsetActiveCodes is an ORed mask of all the symbologies to be enabled.
#
#  For the best performance, only enable symbologies you explicitly need to scan; enabling too many (unnecessary) symbologies
#  can slow the decoder, especially on low-end devices.
#
MWB.MWBsetActiveCodes(  # MWB.MWB_CODE_MASK_QR  |
                        MWB.MWB_CODE_MASK_DM |
                        # MWB.MWB_CODE_MASK_RSS |
                        # MWB.MWB_CODE_MASK_39 |
                        # MWB.MWB_CODE_MASK_EANUPC |
                        # MWB.MWB_CODE_MASK_128  |
                        # MWB.MWB_CODE_MASK_PDF  |
                        # MWB.MWB_CODE_MASK_AZTEC |
                        # MWB.MWB_CODE_MASK_25 |
                        # MWB.MWB_CODE_MASK_93 |
                        # MWB.MWB_CODE_MASK_CODABAR |
                        # MWB.MWB_CODE_MASK_DOTCODE |
                        # MWB.MWB_CODE_MASK_11 |
                        # MWB.MWB_CODE_MASK_MSI |
                        # MWB.MWB_CODE_MASK_MAXICODE |
                        # MWB.MWB_CODE_MASK_POSTAL |
                        # MWB.MWB_CODE_MASK_TELEPEN |
                        0x0)

# 1D Scan direction
#
#  The decoder supports horizontal, vertical, hortizonal & vertical, or omnidirectional scanning for 1D barcodes (2D codes will 
#  scan in any orientation and are not impacted by this setting). In most cases, using just horizontal & vertical is sufficient
#  to locate most 1D codes; omnidirectional can be much slower.
#
MWB.MWBsetDirection(MWB.MWB_SCANDIRECTION_HORIZONTAL | MWB.MWB_SCANDIRECTION_VERTICAL)
# MWB.MWBsetDirection(MWB.MWB_SCANDIRECTION_OMNI)

# Verify 1D location
#
#  Due to the weakness of some 1D symbologies, misreads and short reads are possible in cases of poor print quality, blurry images,
#  extreme skew, etc. To combat this, the decoder provides a verification feature where the decoder works harder to verify the 1D
#  barcode's edges and value. By default, this feature is on for Code 11, Code 25 (all variants), Code 39, Codabar, Code 128, and 
#  MSI Plessey. Be aware that this setting can reduce scanning performance, especially if more than a few symoblogies are enabled.
#
#MWB.MWBsetParam(MWB.MWB_CODE_MASK_EANUPC, MWB.MWB_PAR_ID_VERIFY_LOCATION, MWB.MWB_PAR_VALUE_VERIFY_LOCATION_ON)

# Quiet zones
#
#  Most 1D barcode symbologies define minimum quiet zones for the barcode (whitespace around the barcode's bar/space patterns) to
#  aid in detection and decoding. By default, the decoder only requires that 50% of this requirement be met for Code 11, Code 25,
#  Code 39, Code 128, Codabar, and MSI Plessey (this value is not tunable for other supported symbologies). This quiet zone
#  requirement can be tuned to be more or less strict. Keep in mind though:
#
#     * Less strict quiet zones can lead to misreads and short reads (not recommended)
#     * More strict quiet zones can help reduce misreads and short reads, but may lead to some no reads.
#
#  Below is an example of changing Code 128 to require 100% of the specified quiet zone for the code to be read.
#
#MWB.MWBsetParam(MWB.MWB_CODE_MASK_128, MWB.MWB_PAR_ID_SAFE_ZONE_SCALE, 100)

#
# Decoder effort level (1 - 5)
#
#  When scanning from a live video stream, typically use level 2 (use level 1 for very pristine codes), or level 3  
#  for difficult or dense codes (PDF417). Levels 4 and 5 are intended for offline/batch scanning of an image where
#  extended decode times are not an issue.
#
MWB.MWBsetLevel(effortLevel)

# Scanning rectangle
#
#  You can limit the portion of the image that the SDK will search when locating a barcode. This is useful when working
#  with large images and the general location of the barcode is known (when scanning with a mobile phone, this scenario
#  is common as the user interface typically leads the user to center the barcode and even within a virtual bounding area
#  on screen). This may not be the case with offline image processing (that is, the barcode may appear anywhere within
#  the image).
#
#  While a different scanning rectangle can be defined for each symbology, the SDK will use a union of all defined 
#  scanning rectangles for 1D symbologies when searching for 1D barcodes (including PDF417) and a union of all 
#  defined scanning rectangles for 2D symbologies when searching for 2D barcodes.
#
#  Keep in mind that for 1D codes, a portion of the barocode that is at least the entire width of the barcode (including
#  quiet zones) must be within the scanning rectangle for it to be decoded (the entire height of the 1D code is not 
#  required to be within the scanning rectangle), while for 2D codes the entire code including quiet zones, must be
#  within the scanning rectangle for it to be decoded.
#
#  A scanning rectangle for PDF417 is treated as a 1D symbology; however, due to PDF417's error correction capabiliies,
#  this means that the entire width of a PDF417 may not have to be within the scanning rectangle to be decoded (since 
#  the error correction can recover erasures). Generally this is only likely to occur when a high ECC level has been
#  employed: otherwise expect that the entire PDF417 must be within the scanning rectangle for reliable decoding.
#
#  NOTE: do not use a scanning rectangle in conjunction with multi-code and regions as the results may be 
#        unpredictable.
#
# MWB.MWBsetScanningRect(MWB.MWB_CODE_MASK_PDF, 0, 25, 100, 50);

# Multi-code
#
#  Multi-code can detect as many as 150 barcodes in a single image, though doing so may require significant resources. If the
#  image(s) being decoded have specific, known regions or very dense codes, consider using tiles or defining custom regions.
#  Multi-code requires a license key that has this feature enabled (NOTE: a trial license includes multi-code).
#
#  Note that when setting global decoder options (code mask == 0), OR the new flag with any existing settings.
#
if useMultiCode:
    MWB.MWBsetFlags(0, MWB.MWBgetFlags(0) | MWB.MWB_CFG_GLOBAL_ENABLE_MULTI)

# Scan results
#
#  Use MWResults for all meta data as well as the scanned barcode data
#
MWB.MWBsetResultType(MWB.MWB_RESULT_TYPE_MW)

# Parsers
#
#  Industry standard parsers for a variety of formats are provided for easier processing of common structured data formats. The 
#  parsed results can either be a JSON document or formated text (see the use of the parser below). The SDK provides the following
#  parsers:
#      GS1 - standard data format for the exchange of global trade information
#      IUID - Item Unique Identification marking (or UID), mandated by the US Department of Defense
#      ISBT - global standard for the identification, labeling, and information transfer of medical products of human origin
#      AAMVA - format used for North American driver's licenses and IDs (PDF417 barcode)
#      HIBC - similar to IUID/UID, the Health Industry Bar Code addresse the specific safety and security needs of the 
#             healcare industry
#      SCM - Structured Carrier message; most commonly used in MaxiCode barcodes for shipping inforamtion 
#
#  See mwParser.cs for more details.
#
#  Use of the parsers requires a license key that has this feature enabled (NOTE: a trial license includes all parsers).
#
parserMask = MWP.MWP_PARSER_MASK_NONE
#parserMask = MWP.MWP_PARSER_MASK_GS1
parserMask = MWP.MWP_PARSER_MASK_AAMVA

# Gets SDK version as a string
sdkVersion = MWB.MWBgetLibVersionText()

print("Starting decoder - SDK Version " + str(sdkVersion))
print("  Image " + fileName + " (" + str(grayScale.height) + " X " + str(grayScale.width) + " pixels)")
print("  Effort level: " + str(effortLevel))
if useMultiCode:
    print("  Multi-code enabled")
if useTiles:
    print("  Using tiles (" + str(tilesX) + " x " + str(tilesY) + ") overlap " + str(overlap) + "%, " + str(maxThreads) + " threads");

resultLen = int(0)
regionData = []
regionCount = int(0)

starTime = time.time()

# Decode the image
if useTiles:
    # Tiles/regions
    #
    #  This feature is primarily intended for use with multicode when there exists relatively small codes within a large image, or when 
    #  the layout/locations of the barcodes is known. By dividing the image into smaller "regions", the decoder can process them much
    #  more efficiently, including using multiple threads, if desired. After processing all the regions, the SDK merges the results, 
    #  eliminating duplicates (due to overlapping regions) and retursn the results as a single MWResults list.
    # 
    #  When using tiles, the SDK divides the image into equally sized regions based on the number of columns (tilesX) and rows (tilesY)
    #  specified, with some overlap. Note that the overlap (expressed as a percentage of the image size) needs to be at least as large as
    #  the largest barcode to be scanned--otherwise the possibility exists that a code could be split across adjacent tiles and then
    #  not be detected.
    #
    #  Regions are defined as two pairs of X,Y coordinates as the upper left and lower right corners, in percentages of the image size.
    #
    #  An application can also construct its own region data, explicitly defining the coordinates of each region versus using the tiles
    #  feature. This application only demonstrates using tiles.
    #
    
    # Create the region data
    regionCount, regionData = MWB.MWBcreateRegionsFromTiles(tilesX, tilesY, overlap)
    
    # Decode using the defined regions (multithreaded)
    resultLen, scanResults = MWB.MWBscanGrayscaleRegions(pixels, grayScale.width, grayScale.height, regionData, regionCount, maxThreads)
   
else:
    # Decode using the entire image (and any defined scanning rectangle)
    resultLen, scanResults = MWB.MWBscanGrayscaleImage(pixels, grayScale.width, grayScale.height)

endTime = time.time()

# Make sure the results did not overrun our buffer (very bad)
if resultLen > sizeof(scanResults):
    print("Critical error: scanResults buffer is too small")
    exit()

# The length returned is for the raw results buffer; we will create an MWResults object from this since
# it's much easier to work with!
#
if resultLen > 0:
    # Display MWResults
    results = MWR.MWResults(scanResults)
    if results.count > 0:
        print("Total barcodes detected: ", results.count)

        if not(suppressOutput):
            for i in range(results.count):
                result = results.results[i]
                print(str(i+1) + ": (" + result.typeName+ ") " + str(result.text))
                if parserMask != MWP.MWP_PARSER_MASK_NONE:
                    
                    parsedData = create_string_buffer(10000)
                    
                    # Envoke the parser
                    #
                    #  The SDK provides two parsers, each returning different results:
                    #    JSON - parsed results are returned as a JSON document
                    #    Text - parsed results are returned as key/value pairs (primarily for demonstration/readability purposes)
                    #
                    #pLen, parsedData = MWB.MWPgetJSON(parserMask, result.parserInput, len(result.parserInput))
                    pLen, parsedData = MWB.MWPgetFormattedText(parserMask, result.parserInput, len(result.parserInput))
                    if pLen > sizeof(parsedData):
                        print("Critical error: parsedData buffer is too small")
                        exit()
    
                    if pLen > 0:
                        print("  Parsed Result: " + parsedData.raw[0:int(pLen)].decode("utf-8"))

                        
        # Write image with overlays?
        if writeImage:
            # Reload the orignal image
            im = Image.open(fileName)
            draw = ImageDraw.Draw(im)
            
            # Draw a red box around each barcode found
            for i in range(results.count):
                result = results.results[i]
                draw.line([(result.locationPoints.p1.x,result.locationPoints.p1.y),
                           (result.locationPoints.p2.x,result.locationPoints.p2.y),
                           (result.locationPoints.p3.x,result.locationPoints.p3.y),
                           (result.locationPoints.p4.x,result.locationPoints.p4.y),
                           (result.locationPoints.p1.x,result.locationPoints.p1.y)],fill=(255,0,0),width=4)
            im.show()
            
            # If we defined regions, draw them in yellow    
            if regionCount > 0:
                for i in range(regionCount):
                    # Regions are defined as percentages X, Y, W, H
                    x1 = (regionData[i*4] / 100 ) * grayScale.width
                    y1 = (regionData[i*4+1] / 100 ) * grayScale.height
                    x2 = x1 + (regionData[i*4+2] / 100 ) * grayScale.width
                    y2 = y1 + (regionData[i*4+3] / 100 ) * grayScale.height

                    # Bah; draw the rectangle using lines as older versions of Pillow do not support width= for .rectangle
                    draw.line([(x1,y1),(x2,y1),(x2,y2),(x1,y2),(x1,y1)],fill=(255,255,0),width=4)

            # Save as a new image with _out appended to the file name
            split = path.splitext(fileName)
            im.save(split[0]+"_out"+split[1])

    else:
        print("Failed to decode MWResults")
else:
    print("No barcodes found: decoder returned " + str(resultLen))
    
    
totalMS = (endTime - starTime) * 1000
print("Total decoder time %.2f" % totalMS + " ms")
