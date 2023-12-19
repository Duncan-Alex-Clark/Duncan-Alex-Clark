#
# File     BarcodeScanner.py
#
# Brief    Wrapper/helper functions for the Cognex Barcode Scanner library (Windows/Linux)
# 
# Details  This is the python interface to the Cognex barcode scanner library (originally
#          named the Manatee Works Barcode Scanners Libary).
#         
#          ctypes is used to load and wrap the library's function, with MWResult.py provided to
#          convert the library's barcode scan data to an easy to use object, while MWParser.py 
#          has the definitions for the SDK's data parser functions.
#
# Notice   Copyright (C) Cognex Corporation 
#

import struct
import ctypes
from ctypes.util import find_library
import platform

# Windows
if platform.system() == 'Windows':
    libc = None

    # Load either the 32-bit or 64-bit shared library
    if (8 * struct.calcsize("P")) == 32:
        mwdll = ctypes.cdll.LoadLibrary('../lib/dll/32bit/BarcodeScanner.dll')
    else:
        mwdll = ctypes.cdll.LoadLibrary('../lib/dll/64bit/BarcodeScanner64.dll')
    
    MWBgetLibVersion = mwdll.MWBgetLibVersion
    MWBgetLibVersionText = mwdll.MWBgetLibVersionText
    MWBsetScanningRect = mwdll.MWBsetScanningRect
    MWBgetScanningRect = mwdll.MWBgetScanningRect
    MWBregisterSDK = mwdll.MWBregisterSDK_pchar
    MWBregisterSDKCustom = mwdll.MWBregisterSDKCustom
    MWBgetDeviceID = mwdll.MWBgetDeviceID
    MWBgetLicenseString = mwdll.MWBgetLicenseString
    MWBsetTargetRect = mwdll.MWBsetTargetRect
    MWBgetTargetRect = mwdll.MWBgetTargetRect
    MWBsetActiveCodes = mwdll.MWBsetActiveCodes
    MWBgetActiveCodes = mwdll.MWBgetActiveCodes
    MWBgetSupportedCodes = mwdll.MWBgetSupportedCodes
    MWBenableCode = mwdll.MWBenableCode
    MWBdisableCode = mwdll.MWBdisableCode
    MWBsetActiveSubcodes = mwdll.MWBsetActiveSubcodes
    MWBgetActiveSubcodes = mwdll.MWBgetActiveSubcodes
    MWBenableSubcode = mwdll.MWBenableSubcode
    MWBdisableSubcode = mwdll.MWBdisableSubcode
    MWBsetCodePriority = mwdll.MWBsetCodePriority
    MWBcleanupLib = mwdll.MWBcleanupLib
    MWBgetLastType = mwdll.MWBgetLastType
    MWBsetFlags = mwdll.MWBsetFlags
    MWBenableFlag = mwdll.MWBenableFlag
    MWBdisableFlag = mwdll.MWBdisableFlag
    MWBgetFlags = mwdll.MWBgetFlags
    MWBsetLevel = mwdll.MWBsetLevel
    MWBsetDirection = mwdll.MWBsetDirection
    MWBgetDirection = mwdll.MWBgetDirection
    MWBsetMinLength = mwdll.MWBsetMinLength
    MWBsetParam = mwdll.MWBsetParam
    MWBgetParam = mwdll.MWBgetParam
    MWBgetBarcodeLocation = mwdll.MWBgetBarcodeLocation
    MWBsetResultType = mwdll.MWBsetResultType
    MWBgetResultType = mwdll.MWBgetResultType
    MWBsetDuplicatesTimeout = mwdll.MWBsetDuplicatesTimeout
    MWBsetDuplicate = mwdll.MWBsetDuplicate_pchar
    MWPgetSupportedParsers = mwdll.MWPgetSupportedParsers

    # Functions which need a Python wrapper (see below)
    _MWBscanGrayscaleImage = mwdll.MWBscanGrayscaleImage
    _MWPgetFormattedText = mwdll.MWPgetFormattedText
    _MWPgetJSON = mwdll.MWPgetJSON
    _MWBcreateRegionsFromTiles = mwdll.MWBcreateRegionsFromTiles
    _MWBscanGrayscaleRegions = mwdll.MWBscanGrayscaleRegions
    
# Linux
elif platform.system() == 'Linux':
    libc = ctypes.CDLL(find_library("c"))

    # Load either the 32-bit or 64-bit library for ARM or x86
    if "arm" in platform.processor() or "aarch" in platform.processor():
        if (8 * struct.calcsize("P")) == 32:
            mwLib = ctypes.cdll.LoadLibrary('../lib/arm/32bit/libBarcodeScanner.so')
        else:
            mwLib = ctypes.cdll.LoadLibrary('../lib/arm/64bit/libBarcodeScanner64.so')
    else:
        if (8 * struct.calcsize("P")) == 32:
            mwLib = ctypes.cdll.LoadLibrary('../lib/x86/32bit/libBarcodeScanner.so')
        else:
            mwLib = ctypes.cdll.LoadLibrary('demo/lib/x86/64bit/libBarcodeScanner.so')
            
    MWBgetLibVersion = mwLib.MWB_getLibVersion
    MWBgetLibVersionText = mwLib.MWB_getLibVersionText
    MWBsetScanningRect = mwLib.MWB_setScanningRect
    MWBgetScanningRect = mwLib.MWB_getScanningRect
    MWBregisterSDK = mwLib.MWB_registerSDK
    MWBregisterSDKCustom = mwLib.MWB_registerSDKCustom
    MWBgetDeviceID = mwLib.MWB_getDeviceID
    MWBgetLicenseString = mwLib.MWB_getLicenseString
    MWBsetTargetRect = mwLib.MWB_setTargetRect
    MWBgetTargetRect = mwLib.MWB_getTargetRect
    MWBsetActiveCodes = mwLib.MWB_setActiveCodes
    MWBgetActiveCodes = mwLib.MWB_getActiveCodes
    MWBgetSupportedCodes = mwLib.MWB_getSupportedCodes
    MWBenableCode = mwLib.MWB_enableCode
    MWBdisableCode = mwLib.MWB_disableCode
    MWBsetActiveSubcodes = mwLib.MWB_setActiveSubcodes
    MWBgetActiveSubcodes = mwLib.MWB_getActiveSubcodes
    MWBenableSubcode = mwLib.MWB_enableSubcode
    MWBdisableSubcode = mwLib.MWB_disableSubcode
    MWBsetCodePriority = mwLib.MWB_setCodePriority
    MWBcleanupLib = mwLib.MWB_cleanupLib
    MWBgetLastType = mwLib.MWB_getLastType
    MWBsetFlags = mwLib.MWB_setFlags
    MWBenableFlag = mwLib.MWB_enableFlag
    MWBdisableFlag = mwLib.MWB_disableFlag
    MWBgetFlags = mwLib.MWB_getFlags
    MWBsetLevel = mwLib.MWB_setLevel
    MWBsetDirection = mwLib.MWB_setDirection
    MWBgetDirection = mwLib.MWB_getDirection
    MWBsetMinLength = mwLib.MWB_setMinLength
    MWBsetParam = mwLib.MWB_setParam
    MWBgetParam = mwLib.MWB_getParam
    MWBgetBarcodeLocation = mwLib.MWB_getBarcodeLocation
    MWBsetResultType = mwLib.MWB_setResultType
    MWBgetResultType = mwLib.MWB_getResultType
    MWBsetDuplicatesTimeout = mwLib.MWB_setDuplicatesTimeout
    MWBsetDuplicate = mwLib.MWB_setDuplicate

    MWPgetSupportedParsers = mwLib.MWP_getSupportedParsers
    
    # Functions which need a Python wrapper (see below)
    _MWBscanGrayscaleImage = mwLib.MWB_scanGrayscaleImage
    _MWPgetFormattedText = mwLib.MWP_getFormattedText
    _MWPgetJSON = mwLib.MWP_getJSON
    _MWBcreateRegionsFromTiles = mwLib.MWB_createRegionsFromTiles
    _MWBscanGrayscaleRegions = mwLib.MWB_scanGrayscaleRegions

# Unsupported
else:
    print('Unsupported operating system')
    exit()

#
# Define the parameters and return value
#

# unsigned int MWBgetLibVersion(void)
MWBgetLibVersion.argtypes = None
MWBgetLibVersion.restype = ctypes.c_int

# char* MWBgetLibVersionText(void)
MWBgetLibVersionText.argtypes = None
MWBgetLibVersionText.restype = ctypes.c_char_p

# int MWBsetScanningRect(const uint32_t codeMask, float left, float top, float width, float height)
MWBsetScanningRect.argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
MWBsetScanningRect.restype = ctypes.c_int

# int MWBgetScanningRect(const uint32_t codeMask, float *left, float *top, float *width, float *height)
MWBgetScanningRect.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
MWBgetScanningRect.restype = ctypes.c_int

# int MWBregisterSDK(const char * key)
MWBregisterSDK.argtypes = [ctypes.c_char_p]
MWBregisterSDK.restype = ctypes.c_int

# int MWBregisterSDKCustom(const char * key, const char* customData)
MWBregisterSDKCustom.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
MWBregisterSDKCustom.restype = ctypes.c_int

# char* MWBgetDeviceID(void)
MWBgetDeviceID.argtypes = None
MWBgetDeviceID.restype = ctypes.c_char_p

# char* MWBgetLicenseString(void)
MWBgetLicenseString.argtypes = None
MWBgetLicenseString.restype = ctypes.c_char_p

# int MWBsetTargetRect(float left, float top, float width, float height)
MWBsetTargetRect.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float]
MWBsetTargetRect.restype = ctypes.c_int

# int MWBgetTargetRect(float *left, float *top, float *width, float *height)
MWBgetTargetRect.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
MWBgetTargetRect.restype = ctypes.c_int

# int MWBsetActiveCodes(const uint32_t codeMask)
MWBsetActiveCodes.argtypes = [ctypes.c_int]
MWBsetActiveCodes.restype = ctypes.c_int

# int MWBgetActiveCodes(void)
MWBgetActiveCodes.argtypes = None
MWBgetActiveCodes.restype = ctypes.c_int

# unsigned int MWBgetSupportedCodes(void)
MWBgetSupportedCodes.argtypes = None
MWBgetSupportedCodes.restype = ctypes.c_int

# int MWBenableCode(const uint32_t codeMask)
MWBenableCode.argtypes = [ctypes.c_int]
MWBenableCode.restype = ctypes.c_int

# int MWBdisableCode(const uint32_t codeMask)
MWBdisableCode.argtypes = [ctypes.c_int]
MWBdisableCode.restype = ctypes.c_int

# int MWBsetActiveSubcodes(const uint32_t codeMask, const uint32_t subMask)
MWBsetActiveSubcodes.argtypes = [ctypes.c_int, ctypes.c_int]
MWBsetActiveSubcodes.restype = ctypes.c_int

# int MWBgetActiveSubcodes(const uint32_t codeMask
MWBgetActiveSubcodes.argtypes = [ctypes.c_int]
MWBgetActiveSubcodes.restype = ctypes.c_int

# int MWBenableSubcode(const uint32_t codeMask, const uint32_t subMask)
MWBenableSubcode.argtypes = [ctypes.c_int, ctypes.c_int]
MWBenableSubcode.restype = ctypes.c_int

# int MWBdisableSubcode(const uint32_t codeMask, const uint32_t subMask)
MWBdisableSubcode.argtypes = [ctypes.c_int, ctypes.c_int]
MWBdisableSubcode.restype = ctypes.c_int

# int MWBsetCodePriority(const uint32_t codeMask, const uint8_t priority)
MWBsetCodePriority.argtypes = [ctypes.c_int, ctypes.c_byte]
MWBsetCodePriority.restype = ctypes.c_int

# int MWBcleanupLib(void)
MWBcleanupLib.argtypes = None
MWBcleanupLib.restype = ctypes.c_int

# int MWBgetLastType(void)
MWBgetLastType.argtypes = None
MWBgetLastType.restype = ctypes.c_int

# int MWBsetFlags(const uint32_t codeMask, const uint32_t flags)
MWBsetFlags.argtypes = [ctypes.c_int, ctypes.c_int]
MWBsetFlags.restype = ctypes.c_int

# int MWBenableFlag(const uint32_t codeMask, const uint32_t flag)
MWBenableFlag.argtypes = [ctypes.c_int, ctypes.c_int]
MWBenableFlag.restype = ctypes.c_int

# int MWBdisableFlag(const uint32_t codeMask, const uint32_t flag)
MWBdisableFlag.argtypes = [ctypes.c_int, ctypes.c_int]
MWBdisableFlag.restype = ctypes.c_int

# int MWBgetFlags(const uint32_t codeMask)
MWBgetFlags.argtypes = [ctypes.c_int]
MWBgetFlags.restype = ctypes.c_int

# int MWBsetLevel(const int level)
MWBsetLevel.argtypes = [ctypes.c_int]
MWBsetLevel.restype = ctypes.c_int

# int MWBsetDirection(const uint32_t direction)
MWBsetDirection.argtypes = [ctypes.c_int]
MWBsetDirection.restype = ctypes.c_int

# MWBgetDirection(void)
MWBgetDirection.argtypes = None
MWBgetDirection.restype = ctypes.c_int

# int MWBsetMinLength(const uint32_t codeMask, const uint32_t minLength)
MWBsetMinLength.argtypes = [ctypes.c_int, ctypes.c_int]
MWBsetMinLength.restype = ctypes.c_int

# int MWBsetParam(const uint32_t codeMask, const uint32_t paramId, const uint32_t paramValue)
MWBsetParam.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
MWBsetParam.restype = ctypes.c_int

# int MWBgetParam(const uint32_t codeMask, const uint32_t paramId)
MWBgetParam.argtypes = [ctypes.c_int, ctypes.c_int]
MWBgetParam.restype = ctypes.c_int

# int MWBgetBarcodeLocation(float *points)
MWBgetBarcodeLocation.argtypes = [ctypes.POINTER(ctypes.c_float)]
MWBgetBarcodeLocation.restype = ctypes.c_int

# int MWBsetResultType(const uint32_t resultType)
MWBsetResultType.argtypes = [ctypes.c_int]
MWBsetResultType.restype = ctypes.c_int

# int MWBgetResultType(void)
MWBgetResultType.argtypes = None
MWBgetResultType.restype = ctypes.c_int

# int MWBsetDuplicatesTimeout(uint32_t timeout)
MWBsetDuplicatesTimeout.argtypes = [ctypes.c_int]
MWBsetDuplicatesTimeout.restype = ctypes.c_int

# void MWBsetDuplicate(uint8_t* barcode, int length)
MWBsetDuplicate.argtypes = [ctypes.c_char_p, ctypes.c_int]
MWBsetDuplicate.restype = None

# unsigned int MWPgetSupportedParsers(void)
MWPgetSupportedParsers.argtypes = None
MWPgetSupportedParsers.restype = ctypes.c_int

if platform.system() == 'Windows':
    #
    # Windows - the output buffers from the MWBscanGrayscaleImage, MWBscanGrayscaleRegions, MWPgetFormattedText,
    #           and MWPgetJSON functions must be declared and provided by the calling program (whereas under 
    #           Linux, the buffer is allocated by the barcode library). To have a consistant Python wrapper, we 
    #           will have to allocate the buffer here and, well, hope that it's big enough. These wrappers all use
    #           "worse case" estimations for that size, and we check it once the function completes. Note though
    #           that if we do exceed the size we used here then we have to throw an exception (as memory is 
    #           almost certainly corrupt at that point). If the exception is thrown, the buffer size would need 
    #           to be increased.
    #

    # MWBscanGrayscaleImage
    #
    # Wrapper function to get the scan results in a ctypes string buffer, but also verify that we
    # didn't overrun the buffer.
    #
    # This function returns a tuple:
    #  resultLen  - Negative for an error, otherwise the # of bytes in scanResult
    #  scanResult - A ctypes string buffer (bytes); we return a scanResult as this is the expected
    #               input for MWResult, the class for decoding the scan results 
    #
    # int MWBscanGrayscaleImage(uint8_t*  pp_image,  int lenX,  int lenY, uint8_t *pp_data)
    _MWBscanGrayscaleImage.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
    _MWBscanGrayscaleImage.restype = ctypes.c_int
    
    def MWBscanGrayscaleImage(grayScale, width, height):

        # Sizing the results array can be complex if using MWB.MWB_RESULT_TYPE_MW (i.e, all the meta data from the scan) versus just the scan
        # results (i.e., the barcode contents). Meta data returned is variable in length based on the barcode type, length, and number of 
        # barcodes being scanned. A minimum estimation is about 5K per barcode decoded (if you're using multicode, which can decode up to 
        # 150 codes in a single pass, a very large buffer could be required). For this reason, we are using a large buffer here.
        scanResults = ctypes.create_string_buffer(100000)

        # Check the image for barcode(s)
        resultLen = _MWBscanGrayscaleImage(grayScale, width, height, scanResults)

        # Check to make sure we didn't overrun our buffer; if we did we have no choice but to throw an exception
        if resultLen > ctypes.sizeof(scanResults):
            raise BufferError('scanResults buffer too small')
        
        return resultLen, scanResults
  
    # MWBscanGrayscaleRegions
    #
    # Wrapper function to get the scan results in a ctypes string buffer, but also verify that we
    # didn't overrun the buffer. We also need to convert a python float array to a byte array of
    # the float values (to pass to the scanner library function).
    #
    # This function returns a tuple:
    #  resultLen  - Negative for an error, otherwise the # of bytes in scanResult
    #  scanResult - A ctypes string buffer (bytes); we return a scanResult as this is the expected
    #               input for MWResult, the class for decoding the scan results 
    #
    # int MWBscanGrayscaleRegions(uint8_t*  pp_image,  int lenX,  int lenY, float* regionsData, int numberOfRegions, int maxThreads, uint8_t *pp_data)
    #
    _MWBscanGrayscaleRegions.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
    _MWBscanGrayscaleRegions.restype = ctypes.c_int

    def MWBscanGrayscaleRegions(pp_image,  lenX,  lenY, regionsData, regionCount, maxThreads):
        # Sizing the results array can be complex if using MWB.MWB_RESULT_TYPE_MW (i.e, all the meta data from the scan) versus just the scan
        # results (i.e., the barcode contents). Meta data returned is variable in length based on the barcode type, length, and number of 
        # barcodes being scanned. A minimum estimation is about 5K per barcode decoded (if you're using multicode, which can decode up to 
        # 150 codes in a single pass, a very large buffer could be required). For this reason, we are using a large buffer here.
        scanResults = ctypes.create_string_buffer(100000)

        # Convert the float array to a byte array
        regions = struct.pack("f" * len(regionsData), *regionsData)

        # Check the image for barcode(s)
        resultLen = _MWBscanGrayscaleRegions(pp_image, lenX, lenY, regions, regionCount, maxThreads, scanResults)

        # Check to make sure we didn't overrun our buffer; if we did we have no choice but to throw an exception
        if resultLen > ctypes.sizeof(scanResults):
            raise BufferError('scanResults buffer too small')
        
        return resultLen, scanResults

    # MWPgetFormattedText
    #
    # Wrapper function to get the parser results in a ctypes string buffer, but also verify that we
    # didn't overrun the buffer.
    #
    # This function returns a tuple:
    #  returnLen    - Negative for an error, otherwise the length of the returned data buffer
    #  parserResult - A ctypes string buffer (bytes); we return a scanResult as this is the expected
    #                 input for MWResult, the class for decoding the scan results 
    #
    # double MWPgetFormattedText(int parser_type, uint8_t * p_input, int inputLength, uint8_t *pp_output)
    _MWPgetFormattedText.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
    _MWPgetFormattedText.restype = ctypes.c_double

    def MWPgetFormattedText(parserMask, parserInput, parserInputLen):

        parserResult = ctypes.create_string_buffer(10000)
        
        # Run the parser for formatted text
        resultLen = _MWPgetFormattedText(parserMask, parserInput, parserInputLen, parserResult)

        if resultLen > ctypes.sizeof(parserResult):
            raise BufferError('parserResult buffer too small')
        
        return resultLen, parserResult

    # MWPgetJSON
    #
    # Wrapper function to get the parser results in a ctypes string buffer, but also verify that we
    # didn't overrun the buffer.
    #
    # This function returns a tuple:
    #  returnLen    - Negative for an error, otherwise the length of the returned data buffer
    #  parserResult - A ctypes string buffer (bytes); we return a scanResult as this is the expected
    #                 input for MWResult, the class for decoding the scan results 
    #
    # double MWPgetJSON(int parser_type, uint8_t* p_input, int inputLength, uint8_t *pp_output)
    _MWPgetJSON.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
    _MWPgetJSON.restype = ctypes.c_double

    def MWPgetJSON(parserMask, parserInput, parserInputLen):

        parserResult = ctypes.create_string_buffer(10000)
        
        # Run the parser for formatted text
        resultLen = _MWPgetJSON(parserMask, parserInput, parserInputLen, parserResult)
        
        if resultLen > ctypes.sizeof(parserResult):
            raise BufferError('parserResult buffer too small')
        
        return resultLen, parserResult

else:
    #
    # Linux - the output buffers from the MWBscanGrayscaleImage, MWBscanGrayscaleRegions, MWPgetFormattedText,
    #         and MWPgetJSON functions are all dynamically allocated by the shared library itself: the 
    #         calling program is responsible for freeing it. This all changes the parameter lists of the
    #         functions as compared to the Windows DLL. We will copy the data returned to a python ctypes 
    #         string buffer, free the memory returned by the function, then return the results as a tuple 
    #         for all four functions
    #

    # MWBscanGrayscaleImage
    #
    # Wrapper function to manage the dynamically allocated return results: we copy the returned data
    # to a ctypes string buffer, then free the memory allocated by the barcode scanner's library.
    #
    # This function returns a tuple:
    #  resultLen  - Negative for an error, otherwise the # of bytes in scanResult
    #  scanResult - A ctypes string buffer (bytes); we return a scanResult as this is the expected
    #               input for MWResult, the class for decoding the scan results 
    #
    _MWBscanGrayscaleImage.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte))]
    _MWBscanGrayscaleImage.restype = ctypes.c_int

    def MWBscanGrayscaleImage(grayScale, width, height):

        buffer = ctypes.POINTER(ctypes.c_ubyte)()
        
        # The barcode scanning library dynamically allocates the buffer for the return results (the
        # buffer parameter is a uint8_t **). Note that we are responsible for freeing this memory
        resultLen = _MWBscanGrayscaleImage(grayScale, width, height, buffer)

        if resultLen > 0:
            # Copy the results to a ctypes string buffer
            scanResult = ctypes.create_string_buffer(resultLen)
            scanResult[0:resultLen] = buffer[0:resultLen]
        else:
            scanResult = ctypes.create_string_buffer(0)
        
        # Free the memory returned by _MWBscanGrayscaleImage()
        libc.free(buffer)
        
        return resultLen, scanResult

    # MWBscanGrayscaleRegions
    #
    # Wrapper function to get the scan results in a ctypes string buffer, but also verify that we
    # didn't overrun the buffer.
    #
    # This function returns a tuple:
    #  resultLen  - Negative for an error, otherwise the # of bytes in scanResult
    #  scanResult - A ctypes string buffer (bytes); we return a scanResult as this is the expected
    #               input for MWResult, the class for decoding the scan results 
    #
    # int MWBscanGrayscaleRegions(uint8_t*  pp_image,  int lenX,  int lenY, float* regionsData, int numberOfRegions, int maxThreads, uint8_t *pp_data)
    #
    _MWBscanGrayscaleRegions.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte))]
    _MWBscanGrayscaleRegions.restype = ctypes.c_int

    def MWBscanGrayscaleRegions(pp_image,  lenX,  lenY, regionsData, regionCount, maxThreads):

        buffer = ctypes.POINTER(ctypes.c_ubyte)()
        
        # Convert the float array to a byte array
        regions = struct.pack("f" * len(regionsData), *regionsData)

        # The barcode scanning library dynamically allocates the buffer for the return results (the
        # buffer parameter is a uint8_t **). Note that we are responsible for freeing this memory
        resultLen = _MWBscanGrayscaleRegions(pp_image, lenX, lenY, regions, regionCount, maxThreads, buffer)

        if resultLen > 0:
            # Copy the results to a ctypes string buffer
            scanResult = ctypes.create_string_buffer(resultLen)
            scanResult[0:resultLen] = buffer[0:resultLen]
        else:
            scanResult = ctypes.create_string_buffer(0)
        
        # Free the memory returned by _MWBscanGrayscaleRegions()
        libc.free(buffer)
        
        return resultLen, scanResult

    # MWPgetFormattedText
    #
    # Wrapper function to manage the dynamically allocated return results: we copy the returned data
    # to a ctypes string buffer, then free the memory allocated by the barcode scanner's library.
    #
    # This function returns a tuple:
    #  returnLen    - Negative for an error, otherwise the length of the returned data buffer
    #  parserResult - A ctypes string buffer (bytes); we return a scanResult as this is the expected
    #                 input for MWResult, the class for decoding the scan results 
    #
    # double MWPgetFormattedText(int parser_type, uint8_t * p_input, int inputLength, uint8_t **pp_output)
    _MWPgetFormattedText.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte))]
    _MWPgetFormattedText.restype = ctypes.c_double

    def MWPgetFormattedText(parserMask, parserInput, parserInputLen):

        buffer = ctypes.POINTER(ctypes.c_ubyte)()
        
        # The barcode scanning library dynamically allocates the buffer for the return results (the
        # buffer parameter is a uint8_t **). Note that we are responsible for freeing this memory
        resultLen = _MWPgetFormattedText(parserMask, parserInput, parserInputLen, buffer)

        if resultLen > 0:
            # Copy the results to a ctypes string buffer
            rLen = int(resultLen)
            parserResult = ctypes.create_string_buffer(rLen)
            parserResult[0:rLen] = buffer[0:rLen]
        else:
            parserResult = ctypes.create_string_buffer(0)
        
        # Free the memory returned by _MWPgetFormattedText()
        libc.free(buffer)
        
        return resultLen, parserResult

    # MWPgetJSON
    #
    # Wrapper function to manage the dynamically allocated return results: we copy the returned data
    # to a ctypes string buffer, then free the memory allocated by the barcode scanner's library.
    #
    # This function returns a tuple:
    #  returnLen    - Negative for an error, otherwise the length of the returned data buffer
    #  parserResult - A ctypes string buffer (bytes); we return a scanResult as this is the expected
    #                 input for MWResult, the class for decoding the scan results 
    #
    # double MWPgetJSON(int parser_type, uint8_t* p_input, int inputLength, uint8_t **pp_output)
    _MWPgetJSON.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte))]
    _MWPgetJSON.restype = ctypes.c_double

    def MWPgetJSON(parserMask, parserInput, parserInputLen):

        buffer = ctypes.POINTER(ctypes.c_ubyte)()
        
        # The barcode scanning library dynamically allocates the buffer for the return results (the
        # buffer parameter is a uint8_t **). Note that we are responsible for freeing this memory
        resultLen = _MWPgetJSON(parserMask, parserInput, parserInputLen, buffer)

        if resultLen > 0:
            # Copy the results to a ctypes string buffer
            rLen = int(resultLen)
            parserResult = ctypes.create_string_buffer(rLen)
            parserResult[0:rLen] = buffer[0:rLen]
        else:
            parserResult = ctypes.create_string_buffer(0)
        
        # Free the memory returned by _MWPgetJSON()
        libc.free(buffer)
        
        return resultLen, parserResult

# MWBcreateRegionsFromTiles
#
# Wrapper function to create a python array of floats from the barcode scanner library (which returns them
# as a raw byte array)
#
# This function returns a tuple:
#  regionCount (int) - the number of regions created
#  regionData (float[]) - the coordinates/szies of the regions created
#
# int MWBcreateRegionsFromTiles(int tilesX, int tilesY, int overlap, float *regionsData)
#
_MWBcreateRegionsFromTiles.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
_MWBcreateRegionsFromTiles.restype = ctypes.c_int

def MWBcreateRegionsFromTiles(tilesX, tilesY, overlap):
    # We need a mutable buffer for the tile definitions
    nbrOfFloats = tilesX * tilesY * 4
    regionBuffer = ctypes.create_string_buffer(nbrOfFloats * 4)

    # Create the regions (based on number of X & Y tiles)
    regionCount = _MWBcreateRegionsFromTiles(tilesX, tilesY, overlap, regionBuffer)
    
    # Convert to a tuple
    regions = struct.unpack("f" * nbrOfFloats, regionBuffer.raw)
    
    # Now copy to our flaot array
    regionData = [0.0] * nbrOfFloats 
    i = 0
    for x in regions:
        regionData[i] = x
        i += 1

    return regionCount, regionData

#
# Constants
#

# Maximum/minimum grayscale image sizes (pixels)
MWB_GRAYSCALE_LENX_MIN = 25
MWB_GRAYSCALE_LENX_MAX = 5000
MWB_GRAYSCALE_LENY_MIN = 25
MWB_GRAYSCALE_LENY_MAX = 5000


# Basic function return values
MWB_RT_OK = 0
MWB_RT_FAIL = -1
MWB_RT_NOT_SUPPORTED = -2
MWB_RT_BAD_PARAM = -3

# Return values for RegisterSDK function
MWB_RTREG_OK = 0
MWB_RTREG_INVALID_KEY = -1
MWB_RTREG_INVALID_CHECKSUM = -2
MWB_RTREG_INVALID_APPLICATION = -3
MWB_RTREG_INVALID_SDK_VERSION = -4
MWB_RTREG_INVALID_KEY_VERSION = -5
MWB_RTREG_INVALID_PLATFORM = -6
MWB_RTREG_KEY_EXPIRED = -7
MWB_RTREG_AIMER_REQUIRED = -8
MWB_RTREG_AIMER_NOT_DETECTED = -9

# Warnings
MWB_RTREG_CUSTOM_SIZE_EXCEEDED = -100

# Configuration values for use with MWB_setFlags

# Global decoder flags value: apply sharpening on input image
MWB_CFG_GLOBAL_HORIZONTAL_SHARPENING = 0x1
MWB_CFG_GLOBAL_VERTICAL_SHARPENING = 0x2
MWB_CFG_GLOBAL_SHARPENING = 0x3

# Global decoder flags value: apply rotation on input image
MWB_CFG_GLOBAL_ROTATE90 = 0x04
MWB_CFG_GLOBAL_ROTATE180 = 0x08

# Global decoder flags value: calculate location for 1D barcodeTypes (Code128, Code93, Code39 supported)
MWB_CFG_GLOBAL_CALCULATE_1D_LOCATION = 0x10

# Global decoder flags value: fail 1D decode if result is not confirmed by location expanding (Code128, Code93, Code39 supported)
MWB_CFG_GLOBAL_VERIFY_1D_LOCATION = 0x20

# Global decoder flags value: fail decode if result is not touching the center of viewfinder (2D + Code128, Code93, Code39 supported)
#                             1D location flags will be enabled automatically with this one
MWB_CFG_GLOBAL_USE_CENTRIC_SCANNING = 0x40

# Global decoder flags value: disable some image pre=processing, suitable for devices with weak CPU
MWB_CFG_GLOBAL_DISABLE_PREPROCESSING = 0x80

# Global decoder flags value: Enable multiple barcode detection in single image
MWB_CFG_GLOBAL_ENABLE_MULTI = 0x100

# Global decoder flags value: multiple scan lines density
MWB_CFG_GLOBAL_SCANLINESx2 = 0x200
MWB_CFG_GLOBAL_SCANLINESx4 = 0x400
MWB_CFG_GLOBAL_SCANLINESx8 = 0x800

# Code39 decoder flags value: require checksum check
MWB_CFG_CODE39_REQUIRE_CHECKSUM = 0x2

# Code39 decoder flags value: don't require stop symbol - can lead to false results
MWB_CFG_CODE39_DONT_REQUIRE_STOP = 0x4

# Code39 decoder flags value: decode full ASCII
MWB_CFG_CODE39_EXTENDED_MODE = 0x8

# Code39 decoder flags value: Try decoding result to CODE32. if failed, Code39 will return
MWB_CFG_CODE39_CODE32_ENABLED = 0x10

# Code39 decoder flags value: ADD 'A' prefix to Code32 result
MWB_CFG_CODE39_CODE32_PREFIX = 0x20

# Code93 decoder flags value: decode full ASCII
MWB_CFG_CODE93_EXTENDED_MODE = 0x8

# UPC/EAN decoder disable addons detection
MWB_CFG_EANUPC_DISABLE_ADDON = 0x1
MWB_CFG_EANUPC_DONT_EXPAND_UPCE = 0x2

# Code25 decoder flags value: require checksum check
# MWB_CFG_CODE25_REQ_CHKSUM is deprecated and shouldn't be used in combination with other checksum flags
MWB_CFG_CODE25_REQ_CHKSUM               = 0x01
MWB_CFG_CODE25_REQ_CHKSUM_STANDARD      = 0x02
MWB_CFG_CODE25_REQ_CHKSUM_INTERLEAVED   = 0x04
MWB_CFG_CODE25_REQ_CHKSUM_IATA          = 0x08
MWB_CFG_CODE25_REQ_CHKSUM_MATRIX        = 0x10
MWB_CFG_CODE25_REQ_CHKSUM_COOP          = 0x20
MWB_CFG_CODE25_REQ_CHKSUM_INVERTED      = 0x40

# Code11 decoder flags value: require checksum check; MWB_CFG_CODE11_REQ_SINGLE_CHKSUM is set by default
MWB_CFG_CODE11_REQ_SINGLE_CHKSUM = 0x1
MWB_CFG_CODE11_REQ_DOUBLE_CHKSUM = 0x2

# MSI Plessey decoder flags value: require checksum check; MWB_CFG_MSI_REQ_10_CHKSUM is set by default
MWB_CFG_MSI_REQ_10_CHKSUM = 0x01
MWB_CFG_MSI_REQ_1010_CHKSUM = 0x02
MWB_CFG_MSI_REQ_11_IBM_CHKSUM = 0x04
MWB_CFG_MSI_REQ_11_NCR_CHKSUM = 0x08
MWB_CFG_MSI_REQ_1110_IBM_CHKSUM = 0x10
MWB_CFG_MSI_REQ_1110_NCR_CHKSUM = 0x20

# Codabar decoder flags value: include start/stop symbols in result
MWB_CFG_CODABAR_INCLUDE_STARTSTOP = 0x1

# Datamatrix decoder flags value: enable DPM mode
MWB_CFG_DM_DPM_MODE = 0x2

# Telepen decoder flags
MWB_CFG_TELEPEN_FORCE_NUMERIC = 0x1

# Barcode decoder param types
MWB_PAR_ID_ECI_MODE = 0x08
MWB_PAR_ID_RESULT_PREFIX = 0x10
MWB_PAR_ID_VERIFY_LOCATION = 0x20

# working for Datamatrix currently
MWB_PAR_ID_SCAN_COLOR = 0x40

# set safe zone scale factor for 1D barcode type in range 0 - 100%
MWB_PAR_ID_SAFE_ZONE_SCALE = 0x80
    
# Barcode param values
MWB_PAR_VALUE_ECI_DISABLED = 0x00  # default
MWB_PAR_VALUE_ECI_ENABLED = 0x01

MWB_PAR_VALUE_RESULT_PREFIX_NEVER = 0x00  # default
MWB_PAR_VALUE_RESULT_PREFIX_ALWAYS = 0x01
MWB_PAR_VALUE_RESULT_PREFIX_DEFAULT = 0x02

MWB_PAR_VALUE_VERIFY_LOCATION_OFF = 0x00
MWB_PAR_VALUE_VERIFY_LOCATION_ON = 0x01

MWB_PAR_VALUE_COLOR_NORMAL = 0x01
MWB_PAR_VALUE_COLOR_INVERTED = 0x02
MWB_PAR_VALUE_COLOR_BOTH = 0x04 # default

# Bit mask identifiers for supported decoder types
MWB_CODE_MASK_NONE = 0x00000000
MWB_CODE_MASK_QR = 0x00000001
MWB_CODE_MASK_DM = 0x00000002
MWB_CODE_MASK_RSS = 0x00000004  # Gs1 Databar
MWB_CODE_MASK_39 = 0x00000008
MWB_CODE_MASK_EANUPC = 0x00000010
MWB_CODE_MASK_128 = 0x00000020
MWB_CODE_MASK_PDF = 0x00000040
MWB_CODE_MASK_AZTEC = 0x00000080
MWB_CODE_MASK_25 = 0x00000100
MWB_CODE_MASK_93 = 0x00000200
MWB_CODE_MASK_CODABAR = 0x00000400
MWB_CODE_MASK_DOTCODE = 0x00000800
MWB_CODE_MASK_11 = 0x00001000
MWB_CODE_MASK_MSI = 0x00002000
MWB_CODE_MASK_MAXICODE = 0x00004000
MWB_CODE_MASK_POSTAL = 0x00008000
MWB_CODE_MASK_TELEPEN = 0x00010000
MWB_CODE_MASK_ALL = 0x00ffffff

# Bit mask identifiers for RSS (Gs1 Databar) decoder types
MWB_SUBC_MASK_RSS_14 = 0x00000001
MWB_SUBC_MASK_RSS_14_STACK = 0x00000002
MWB_SUBC_MASK_RSS_LIM = 0x00000004
MWB_SUBC_MASK_RSS_EXP = 0x00000008

# Bit mask identifiers for QR decoder types
MWB_SUBC_MASK_QR_STANDARD = 0x00000001
MWB_SUBC_MASK_QR_MICRO = 0x00000002

# Bit mask identifiers for PDF decoder types
MWB_SUBC_MASK_PDF_STANDARD = 0x00000001
MWB_SUBC_MASK_PDF_MICRO = 0x00000002

# Bit mask identifiers for 2 of 5 decoder types
MWB_SUBC_MASK_C25_INTERLEAVED = 0x00000001
MWB_SUBC_MASK_C25_STANDARD = 0x00000002
MWB_SUBC_MASK_C25_ITF14 = 0x00000004
MWB_SUBC_MASK_C25_IATA = 0x00000008
MWB_SUBC_MASK_C25_MATRIX = 0x00000010
MWB_SUBC_MASK_C25_COOP = 0x00000020
MWB_SUBC_MASK_C25_INVERTED = 0x00000040

# Bit mask identifiers for POSTAL decoder types
MWB_SUBC_MASK_POSTAL_POSTNET = 0x00000001
MWB_SUBC_MASK_POSTAL_PLANET = 0x00000002
MWB_SUBC_MASK_POSTAL_IM = 0x00000004
MWB_SUBC_MASK_POSTAL_ROYAL = 0x00000008
MWB_SUBC_MASK_POSTAL_AUSTRALIAN = 0x00000010

# Bit mask identifiers for UPC/EAN decoder types
MWB_SUBC_MASK_EANUPC_EAN_13 = 0x00000001
MWB_SUBC_MASK_EANUPC_EAN_8 = 0x00000002
MWB_SUBC_MASK_EANUPC_UPC_A = 0x00000004
MWB_SUBC_MASK_EANUPC_UPC_E = 0x00000008
MWB_SUBC_MASK_EANUPC_UPC_E1 = 0x00000010

# Bit mask identifiers for 1D scanning direction 
MWB_SCANDIRECTION_HORIZONTAL = 0x00000001
MWB_SCANDIRECTION_VERTICAL = 0x00000002
MWB_SCANDIRECTION_OMNI = 0x00000004
MWB_SCANDIRECTION_AUTODETECT = 0x00000008
MWB_SCANDIRECTION_CUSTOM = 0x00000010

FOUND_NONE = 0
FOUND_DM = 1
FOUND_39 = 2
FOUND_RSS_14 = 3
FOUND_RSS_14_STACK = 4
FOUND_RSS_LIM = 5
FOUND_RSS_EXP = 6
FOUND_EAN_13 = 7
FOUND_EAN_8 = 8
FOUND_UPC_A = 9
FOUND_UPC_E = 10
FOUND_128 = 11
FOUND_PDF = 12
FOUND_QR = 13
FOUND_AZTEC = 14
FOUND_25_INTERLEAVED = 15
FOUND_25_STANDARD = 16
FOUND_93 = 17
FOUND_CODABAR = 18
FOUND_DOTCODE = 19
FOUND_128_GS1 = 20
FOUND_ITF14 = 21
FOUND_11 = 22
FOUND_MSI = 23
FOUND_25_IATA = 24
FOUND_25_MATRIX = 25
FOUND_25_COOP = 26
FOUND_25_INVERTED = 27
FOUND_QR_MICRO = 28
FOUND_MAXICODE = 29
FOUND_POSTNET = 30
FOUND_PLANET = 31
FOUND_IMB = 32
FOUND_ROYALMAIL = 33
FOUND_MICRO_PDF = 34
FOUND_32 = 35
FOUND_AUSTRALIAN = 36
FOUND_TELEPEN = 37

# Identifiers for result types
MWB_RESULT_TYPE_RAW = 0x00000001
MWB_RESULT_TYPE_MW = 0x00000002

# Identifiers for result fields types
MWB_RESULT_FT_BYTES = 0x00000001
MWB_RESULT_FT_TEXT = 0x00000002
MWB_RESULT_FT_TYPE = 0x00000003
MWB_RESULT_FT_SUBTYPE = 0x00000004
MWB_RESULT_FT_SUCCESS = 0x00000005
MWB_RESULT_FT_ISGS1 = 0x00000006
MWB_RESULT_FT_LOCATION = 0x00000007
MWB_RESULT_FT_IMAGE_WIDTH = 0x00000008
MWB_RESULT_FT_IMAGE_HEIGHT = 0x00000009
MWB_RESULT_FT_PARSER_BYTES = 0x0000000A

MWB_RESULT_FT_MODULES_COUNT_X = 0x0000000B
MWB_RESULT_FT_MODULES_COUNT_Y = 0x0000000C
MWB_RESULT_FT_MODULE_SIZE_X = 0x0000000D
MWB_RESULT_FT_MODULE_SIZE_Y = 0x0000000E
MWB_RESULT_FT_SKEW = 0x0000000F
MWB_RESULT_FT_KANJI = 0x00000010

MWB_RESULT_FT_BARCODE_WIDTH = 0x00000011
MWB_RESULT_FT_BARCODE_HEIGHT = 0x00000012
MWB_RESULT_FT_TEXT_ENCODING = 0x00000013

MWB_RESULT_FT_PDF_ROWS = 0x00000020
MWB_RESULT_FT_PDF_COLUMNS = 0x00000021
MWB_RESULT_FT_PDF_TRUNCATED = 0x00000022
MWB_RESULT_FT_PDF_ECLEVEL = 0x00000023
MWB_RESULT_FT_PDF_CODEWORDS = 0x00000024

# Descriptive names of result field types
MWB_RESULT_FNAME_BYTES = "Bytes"
MWB_RESULT_FNAME_TEXT = "Text"
MWB_RESULT_FNAME_TYPE = "Type"
MWB_RESULT_FNAME_SUBTYPE = "Subtype"
MWB_RESULT_FNAME_SUCCESS = "Success"
MWB_RESULT_FNAME_ISGS1 = "GS1 compliance"
MWB_RESULT_FNAME_KANJI = "Kanji encoding"
MWB_RESULT_FNAME_TEXT_ENCODING = "Text encoding"
MWB_RESULT_FNAME_LOCATION = "Location"
MWB_RESULT_FNAME_IMAGE_WIDTH = "Image Width"
MWB_RESULT_FNAME_IMAGE_HEIGHT = "Image Height"
MWB_RESULT_FNAME_PARSER_BYTES = "Parser Input"

MWB_RESULT_FNAME_MODULES_COUNT_X = "Modules Count X"
MWB_RESULT_FNAME_MODULES_COUNT_Y = "Modules Count Y"
MWB_RESULT_FNAME_MODULE_SIZE_X = "Module Size X"
MWB_RESULT_FNAME_MODULE_SIZE_Y = "Module Size Y"
MWB_RESULT_FNAME_SKEW = "Skew"

MWB_RESULT_FNAME_BARCODE_WIDTH = "Barcode Width"
MWB_RESULT_FNAME_BARCODE_HEIGHT = "Barcode Height"

MWB_RESULT_FNAME_PDF_ROWS = "PDF Rows"
MWB_RESULT_FNAME_PDF_COLUMNS = "PDF Columns"
MWB_RESULT_FNAME_PDF_TRUNCATED = "PDF Truncated"
MWB_RESULT_FNAME_PDF_ECLEVEL = "PDF ECLevel"
MWB_RESULT_FNAME_PDF_CODEWORDS = "PDF Codewords"



