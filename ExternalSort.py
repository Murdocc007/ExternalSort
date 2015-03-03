#!/usr/bin/env python

#
# Sort large text files in a minimum amount of memory
#

__author__ = 'aditya.ma'
import os
from os import listdir
from os.path import isfile, join

class TempFiles(object):
    FILENAME_FORMAT = 'file_{0}.dat'

    def __init__(self):
        self.filenames = []

    def write_file(self, data, file_number):
        filename = self.FILENAME_FORMAT.format(file_number)
        file = open(filename, 'w')
        file.write(data)
        file.close()
        self.filenames.append(filename)

    def get_filenames(self):
        return self.filenames

    def populate(self):
        current_dir=os.getcwd()
        myfiles= [ f for f in listdir(current_dir) if (isfile(join(current_dir,f)) and f!='ExternalSort.py') ]

        i = 0

        for file in myfiles:
            fp=open(current_dir+'/'+file,'r')
            lines = fp.readlines()
            temp_lines=[]
            for s in lines:
                if(s!=''and s!='\n'):
                    temp_lines.append(int(s))

            if temp_lines == []:
                break
            temp_lines.sort()
            lines=map(str,temp_lines)
            for j in range(len(lines)):
                lines[j]=lines[j]+'\n'

            self.write_file(''.join(lines), i)
            i += 1

    def cleanup(self):
        map(lambda f: os.remove(f), self.filenames)


class MergeSort(object):

    def select(self, choices,num_of_files):
        min_index = -1
        min_str = None

        print 'choices'
        print choices
        temp_array=[]

        for s in choices:
            if(s!=''and s!='\n'):
                temp_array.append(int(s))

        for i in range(num_of_files):
            if min_str is None:
                if i in choices:
                    min_str=choices[i]
                    min_index=i

            if i in choices:
                if int(min_str)>int(choices[i]):
                    min_str=choices[i]
                    min_index=i

        print 'minimum index'
        print min_index
        return min_index


class FilesArray(object):
    def __init__(self, files):
        self.files = files
        self.empty = set()
        self.num_buffers =len(files)
        self.buffers = {i: None for i in range(self.num_buffers)}

    def get_dict(self):
        return  {i: self.buffers[i] for i in range(self.num_buffers) if i not in self.empty}


    def refresh(self):
        for i in range(self.num_buffers):
            if self.buffers[i] is None and i not in self.empty:
                self.buffers[i] = self.files[i].readline()

                if self.buffers[i] == '':
                    self.empty.add(i)

        if len(self.empty) == self.num_buffers:
            return False

        return True

    def emptybuffer(self, index):
        value = self.buffers[index]
        self.buffers[index] = None

        return value


class FileMerger(object):
    def __init__(self, merge_strategy):
        self.merge_strategy = merge_strategy

    def merge(self, filenames, outfilename):
        outfile = open(outfilename, 'w')
        buffers = FilesArray(self.get_file_handles(filenames))

        while buffers.refresh():
            min_index = self.merge_strategy.select(buffers.get_dict(),len(filenames))
            outfile.write(buffers.emptybuffer(min_index))

    def get_file_handles(self, filenames):
        files = {}
        for i in range(len(filenames)):
            files[i] = open(filenames[i], 'r')

        return files



class ExternalSort(object):
    def __init__(self,outputfile):
        self.output_file = outputfile

    def sort(self):
        temp = TempFiles()
        temp.populate()

        merger = FileMerger(MergeSort())
        merger.merge(temp.get_filenames(), self.output_file + '.out')

        temp.cleanup()


if __name__ == '__main__':
    outputfile='result'
    sorter = ExternalSort(outputfile)
    sorter.sort()
