#!/usr/bin/python3
"""
Created on Mon May 26 17:56 2023

@author: kenna
"""


# Import required modules
import argparse, sys


# Import system modules
from HdfsAudioStore.mainWrappers import HBaseMainWrapper


# Parse arguments
parser = argparse.ArgumentParser(
    description = "App to get and post audio data into HBase table",
    formatter_class = argparse.RawTextHelpFormatter
)
parser.add_argument("-t", "--table_name", action = 'store', type = str, help = "HBase table\n")
parser.add_argument("-s", "--host", action = 'store', type = str, help = "HBase DB host\n")
parser.add_argument("-p", "--port", action = 'store', type = int, help = "HBase DB port\n")
parser.add_argument("-a", "--action", action = "store", type = str, help = "IMPORT | EXPORT action to take on DB")
parser.add_argument("-r", "--export_data", action = 'store', type = str, help = "Data for READ operation format rowKey='' outPath=''")
parser.add_argument("-i", "--import_data", action = 'store', type = str, help = "Data for IMPORT operation format trackPath=,owner=")
parser.add_argument("-c", "--create_table", action = 'store', type = bool, help = "Create table\n")
parser.add_argument("-k", "--rowKey", action = 'store', type = str, help = "Row key")
args = parser.parse_args()


# Exit if key arguments are not supplied
if args.table_name == None or args.host == None or args.port == None or args.action == None:
    print("\n\nExiting, key variables not supplied")
    parser.print_help()
    sys.exit()


# May note be necessary
if args.create_table is None:
    args.create_table = False


# Handle import action
if args.action.lower() == "import":
    if len(args.import_data.split(" ")) != 2 or len(args.import_data.split("=")) != 3:
        print("\n\nExiting, invalid import arguments supplied")
        parser.print_help()
        sys.exit()

    if args.import_data.split("=")[0] == "trackPath":
        trackPath = args.import_data.split("=")[1].replace(" owner", "").replace("\"", "").replace("'", "")
        owner = args.import_data.split("=")[2].replace("\"", "").replace("'", "")
    else:
        owner = args.import_data.split("=")[1].replace(" trackPath", "").replace("\"", "").replace("'", "")
        trackPath = args.import_data.split("=")[2].replace("\"", "").replace("'", "")


# Handle read action
if args.action.lower() == "export":
    if len(args.export_data.split(" ")) != 2 or len(args.export_data.split("=")) != 3:
        print("\n\nExiting, invalid read arguments supplied")
        parser.print_help()
        sys.exit()

    if args.export_data.split("=")[0] == "rowKey":
        rowKey = args.export_data.split("=")[1].replace(" outPath", "").replace("\"", "").replace("'", "")
        outPath = args.export_data.split("=")[2].replace("\"", "").replace("'", "")
    else:
        outPath = args.export_data.split("=")[1].replace(" rowKey", "").replace("\"", "").replace("'", "")
        rowKey = args.export_data.split("=")[2].replace("\"", "").replace("'", "")



# Helper method to support import
def import_main(trackPath: str, owner: str, audio_id: str = None):
    """
    Helper method for main to support imports
    """
    hbaseAudioStoreCli = HBaseMainWrapper.HBaseMain(args.table_name, args.host, args.port, args.create_table)
    hbaseAudioStoreCli.importTrack(trackPath, owner, rowKey = audio_id)


# Helper method to support import
def export_main(rowKey: str, outPath: str):
    """
    Helper method for main to support imports
    """
    hbaseAudioStoreCli = HBaseMainWrapper.HBaseMain(args.table_name, args.host, args.port, args.create_table)
    hbaseAudioStoreCli.writeAudio(rowKey, outPath)


if __name__ == '__main__':

    # Import audio
    if args.action.lower() == "import":

        if args.rowKey != None:
            print(f'Main: Using rowKey = {args.rowKey}')
            import_main(trackPath, owner, args.rowKey)
        else:
            import_main(trackPath, owner)

    # Export audio data
    elif args.action.lower() == "export":
        export_main(rowKey, outPath)

    # Exit
    else:
        print("\n\nExiting, unsupported action")
        parser.print_help()
        sys.exit()