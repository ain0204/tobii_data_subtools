#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------
# 2016/07/21
# Tobiiで記録したSDカード内から丸なし動画を抜いてくるスクリプト
# 引数にrecordingsディレクトリを入力
# Ex: 
# >> python get_recording_data.py <hoge>/projects/<foo>/recordings <OUTPUT_DIR>
# ---------
import os
import sys
import json
import shutil
import platform


def getDirNames( dir_path ):
    """
    指定ディレクトリ下にあるディレクトリ名のリストを得る
    """
    names = os.listdir( dir_path + '/' )
    dir_names = []
    for name in names:
        if os.path.isdir( dir_path + '/' + name ):
            dir_names.append( name )
    return dir_names


def get_movie_name( json_file_name ):
    """
    json fileからRecording名を取得する
    """
    PYTHON_VERSION = platform.python_version_tuple()[0]
    if PYTHON_VERSION == '3':
        json_file = open( json_file_name, 'r'  )
    else:
        json_file = open( json_file_name, 'rb' )

    json_data = json_file.read( )
    json_file.close( )
    dec_data = json.loads( json_data )
    return dec_data['rec_info']['Name']


def getRecordingData( dir_path='.', output_dir='.', copy_flag=True ):
    """
    recordingsディレクトリ下の動画データを移動する
    元データを消してしまわないように、全てコピーで操作するようにしている
    コピーする必要が無ければcopy_flagをFalseに
    """
    # '/'が入力されていたらカット
    if dir_path[-1] == '/':
        dir_path = dir_path[:-1]
    if output_dir[-1] == '/':
        output_dir = output_dir[:-1]

    # 出力用ディレクトリが無ければ作成
    if not os.path.exists( output_dir ) and output_dir != '.':
        os.mkdir( output_dir )
        print( 'mkdir: ' + output_dir )
        
    for dir_name in getDirNames( dir_path ):
        movie_name = get_movie_name( dir_path + '/' + dir_name + '/recording.json' )
        segments_dir_names =  getDirNames( dir_path + '/' + dir_name + '/segments' )
        for segments_dir_name in segments_dir_names:
            from_file_path = dir_path + '/' + dir_name + '/segments/' + segments_dir_name + '/fullstream.mp4'
            if len( segments_dir_names ) == 1:
                to_file_path = output_dir + '/' + movie_name + '.mp4'
            else:
                to_file_path = output_dir + '/' + movie_name + '_' + segments_dir_name + '.mp4'

            if copy_flag:
                shutil.copy2( from_file_path, to_file_path )
                print( 'Copy!: \'{0}\' -> \'{1}\''.format( from_file_path, to_file_path ) )
            else:
                shutil.move( from_file_path, to_file_path )
                print( 'Move!: \'{0}\' -> \'{1}\''.format( from_file_path, to_file_path ) )

                
if __name__ == "__main__":
    param = sys.argv
    if len( param ) == 1:
        getRecordingData( )
    elif len(param) == 2:
        getRecordingData( dir_path   = param[1] )
    elif len(param) == 3:
        getRecordingData( dir_path   = param[1],
        output_dir = param[2], copy_flag = False )
    else:
        print( "argment error!!" )
