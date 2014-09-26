#encoding=utf-8

import sys
import os
import commands
import platform
import subprocess
import tempfile

#获取脚本文件的当前路径
def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    #如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

"""
执行command，并打印log
"""
def execCommand(command, tag=None):
    if tag != None:
        print "exec command:", tag
    print "  execCommand:", command
    state = None
    output = None
    if platform.system() != 'Windows':
        (state, output) = commands.getstatusoutput(command)
    else:
        outputF = tempfile.mktemp()
        errorF  = tempfile.mktemp()

        state = subprocess.call(command, stdout=open(outputF, "w"), stderr=open(errorF, "w"))
        output = "".join(open(outputF, "r").readlines())
        output += "".join(open(errorF, "r").readlines())
    print "  state:", state
    if state != 0:
        # 出现错误
        print (output.decode('gbk', 'ignore'), "error")
    else:
        # 正确
        # print (output, tag)
        pass

    return state, output

"""
获取当前目录的svn url地址
"""
def get_svn_url(dirpath):
    root_tag = "Repository Root:"
    relative_tag = "Relative URL:"

    root_svn_url = None
    relative_svn_url = None
    if os.path.isdir(dirpath):
        command = "svn info " + dirpath
        state, output = execCommand(command)

        for line in output.split("\n"):
            if line.startswith(root_tag):
                root_svn_url = line[len(root_tag):].strip()

            if line.startswith(relative_tag):
                relative_svn_url = line[len(relative_tag):].strip()

    return root_svn_url, relative_svn_url

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    print get_svn_url(r"E:\Tmp\svn")

