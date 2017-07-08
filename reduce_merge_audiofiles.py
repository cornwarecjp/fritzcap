#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#################################################################################
# Workaround for the bug in the fritzcap. Sometimes the phone wav file is splited into
# two files before and after phone connection. The lines in the merged file are then not
# synchronized. This tool create a new mix file with the correct synchronisation and use the
# linux sox tool to create a ogg file.
#
# usage:
#    reduce_merge_audiofiles <path_to_the_folder_with_wav_files>
#
# (c) tom2bor 2011 (tom2bor in http://www.ip-phone-forum.de/)
##################################################################################
# Copyright (c) 2011, tom2bor
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##################################################################################


import sys
import os
import datetime
import re
from sets import Set

def merge_reduce_3files(file1, file2, file3, path="", prefix=""):
    size_file_1 = os.path.getsize(file1)
    size_file_2 = os.path.getsize(file2)
    size_file_3 = os.path.getsize(file3)


    if (size_file_1 < size_file_2 and size_file_1 < size_file_3):
        first_file = file1
        if (size_file_2 < size_file_3):
            second_file = file2
            third_file = file3
        else:
            second_file = file3
            third_file = file2

    if (size_file_2 < size_file_1 and size_file_2 < size_file_3):
        first_file = file2
        if (size_file_1 < size_file_3):
            second_file = file1
            third_file = file3
        else:
            second_file = file3
            third_file = file1

    if (size_file_3 < size_file_1 and size_file_3 < size_file_2):
        first_file = file3
        if (size_file_1 < size_file_2):
            second_file = file1
            third_file = file2
        else:
            second_file = file2
            third_file = file1

    concat_file = "%s%sconc_%s%s_.wav" % (path,prefix,re.search("_(\d{1,2})_", first_file).group(1), re.search("(_\d{1,2})_", second_file).group(1))
    command1 = "sox %s %s %s" % (first_file,second_file,concat_file)
    mixed_file = "%s%smix_%s%s_%s" % (path,prefix,re.search("_(\d{1,2})_", first_file).group(1), re.search("_(\d{1,2})_", second_file).group(1), re.search("_(\d{1,2})_", third_file).group(1))
    command2 = "sox %s %s -M %s.wav" % (concat_file,third_file,mixed_file)
    command3 = "sox %s %s -M %s.ogg" % (concat_file,third_file,mixed_file)

    print "command1:'%s'" % command1
    os.system(command1)
    print "command2:'%s'" % command2
    os.system(command2)
    print "command3:'%s'" % command3
    os.system(command3)




def merge_reduce_dir(path):
    dir_list=os.listdir(path)
    dir_list.sort(compare)
    merge_reduce_files(path, dir_list)

def merge_reduce_files(path, file_names):
    path = path.replace("\\","/")
    if (path and not path.endswith("/")):
        path = path+"/"

#    file_names_set = Set(file_names)
    pattern1 = re.compile(r"((capture_?(\d*)_mix_)(\d+)_(\d+))\.wav")
    pattern2 = re.compile(r"(capture_?\d*_)(\d+)_\.wav")

    last_mix_wav = ""
    last_number = 1
    last_filenumber = 0

    for file_name in file_names:
        matchObj1 = pattern1.search(file_name)
        matchObj2 = pattern2.search(file_name)
        if (matchObj1):
            number1 = int(matchObj1.group(4))
            number2 = int(matchObj1.group(5))

            if (number1 < number2):
                first_number = number1
                second_number = number2
            else:
                first_number = number2
                second_number = number1

            if ((first_number - last_number) == 1):
                file1 = "%s%s" % (path,last_mix_wav)
                file2 = "%s%smix_%s_%s.ogg" % (path,prefix,first_number-2,first_number-1)
                command = "sox %s %s" % (file1,file2)
                print "command:'%s'" % command
                os.system(command)
            elif ((first_number - last_number) == 2):
                file1 = "%s%s%s_.wav" % (path,prefix,(first_number - 3))
                file2 = "%s%s%s_.wav" % (path,prefix,(first_number - 2))
                file3 = "%s%s%s_.wav" % (path,prefix,(first_number - 1))
                merge_reduce_3files(file1,file2,file3,path,prefix)
            last_number = second_number
            last_mix_wav = file_name

        elif (matchObj2):
            number = int(matchObj2.group(2))
            prefix = matchObj2.group(1)
            if (number > last_filenumber):
                last_filenumber = number


    if ((last_filenumber - last_number) == 0):
        file1 = "%s%smix_%s_%s.wav" % (path,prefix,last_filenumber-1,last_filenumber-0)
        file2 = "%s%smix_%s_%s.ogg" % (path,prefix,last_filenumber-1,last_filenumber-0)
        command = "sox %s %s" % (file1,file2)
        print "command:'%s'" % command
        os.system(command)
    elif ((last_filenumber - last_number) == 1):
        file1 = "%s%s%s_.wav" % (path,prefix,last_filenumber - 2)
        file2 = "%s%s%s_.wav" % (path,prefix,last_filenumber - 1)
        file3 = "%s%s%s_.wav" % (path,prefix,last_filenumber - 0)
        merge_reduce_3files(file1,file2,file3,path,prefix)


def compare(str1, str2):
    if (len(str1) > len(str2)):
        return 1
    elif (len(str1) < len(str2)):
        return -1
    else:
        if (str1 > str2):
            return 1
        elif (str1 < str2):
            return -1
        else:
            return 0

if __name__ == '__main__':
    merge_reduce_dir(sys.argv[1])
