#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------
# 2016/07/21
# 出力したtsvファイルを対応するファイルごとに分けてcsvとして保存するプログラム
# Ex:
# >> python data_separater.py <FILE NAME>
# ---------
import sys
import csv
import platform


def get_name_col( header ):
    """
    "Recording name"に対応する列を検索する
    """
    for i, data_name in enumerate( header ):
        if data_name == 'Recording name':
            return i
    return -1


def separate_file( file_name ):
    """
    ファイル中のRecording名を見てファイルを分ける
    """
    PYTHON_VERSION = platform.python_version_tuple()[0]
    if PYTHON_VERSION == '3':
        reader = csv.reader( open( file_name, 'r'  ), delimiter='\t' )
        HEADER = next( reader )
    else:
        reader = csv.reader( open( file_name, 'rb' ), delimiter='\t' )
        HEADER = reader.next()

    REC_NAME_INDEX = get_name_col( HEADER )
    if REC_NAME_INDEX == -1:
        sys.exit( 'Error: REC_NAME_INDEX is not found.' )
        
    recording_name = "init_recording_name"    
    for row in reader:
        if recording_name != row[REC_NAME_INDEX]:
            # Recording名が切り替わったら新しくファイルを作る
            print( ' - new file: ' + recording_name )
            if PYTHON_VERSION == '3':
                writer = csv.writer( open( row[REC_NAME_INDEX]+'.csv', 'w'  ) )
            else:
                writer = csv.writer( open( row[REC_NAME_INDEX]+'.csv', 'wb' ) )
            writer.writerow( HEADER )
            recording_name = row[REC_NAME_INDEX]

        writer.writerow( row )

        
if __name__ == '__main__':
    param = sys.argv
    if len( sys.argv ) > 0:
        file_name = param[1]
        print( "load file name: " + file_name )
    else:
        sys.exit( "Error: no args" )

    separate_file( file_name )

    print( "ok." )
