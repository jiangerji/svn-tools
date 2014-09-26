#encoding=utf-8

import sys
import codecs
import os
import commands
import platform
import subprocess
import tempfile

from svn_common import *
from config import DEPENDS_SVN
from config import JAVA_VERSION_CODE_FORMAT

"""
当完成update后执行
"""
def post_update():
    """
    Post-update
        PATH DEPTH REVISION ERROR CWD 
    """
    print "\n========post update========"
    print sys.argv, len(sys.argv)
    # 执行更新的一些信息
    update_info_path = sys.argv[1]

    # 暂时没有用
    depth = sys.argv[2]

    # 更新后的版本
    revision = sys.argv[3]

    # 更新出错的错误日志
    error_info_path = sys.argv[4]

    # 当前目录
    cwd = sys.argv[5]

    svn_url, relative_url = get_svn_url(cwd)
    print "cwd:", cwd
    print "svn_url:", svn_url
    print "relative_url:", relative_url

    # update sdk version
    update_sdk_version = False

    if DEPENDS_SVN.has_key(svn_url):
        for project in DEPENDS_SVN.get(svn_url):
            depend_svns = project["depends"]
            lk_sdk_svn  = project["url"]
            lk_sdk_dir  = project["dir"]
            lk_package_name = project["package"]

            # depend_svns = DEPENDS_SVN.get(svn_url)[0]
            # lk_sdk_svn  = DEPENDS_SVN.get(svn_url)[0][0]
            # lk_sdk_dir  = DEPENDS_SVN.get(svn_url)[1]
            # lk_package_name = DEPENDS_SVN.get(svn_url)[2]

            if relative_url.find(lk_sdk_svn) >= 0:
                # 为监控svn下的子目录
                update_sdk_version = True
                lk_sdk_dir = cwd[0:-len(relative_url[2+len(lk_sdk_svn):])]
            else:
                for dsvn in DEPENDS_SVN.get(svn_url)[0]:
                    if relative_url.find(dsvn) >= 0 or dsvn.find(relative_url[2:]) >= 0:
                        update_sdk_version = True
                        break

                if update_sdk_version:
                    if lk_sdk_dir == None:
                        relatives = relative_url[2:].split("/")
                        sdk_paths = lk_sdk_svn.split("/")
                        length = 0
                        if len(relatives) < len(sdk_paths):
                            length = len(relatives)
                        else:
                            length = len(sdk_paths)
                        dirs = ""
                        lk_sdk_dir = cwd
                        for i in range(length):
                            if relatives[i] != sdk_paths[i]:
                                dirs = os.path.sep.join(sdk_paths[i:])

                                par_dir = cwd
                                print i
                                for j in range(length-i):
                                    par_dir = os.path.dirname(par_dir)

                                lk_sdk_dir = os.path.join(par_dir, dirs)
                                break

            print lk_sdk_dir, os.path.isdir(lk_sdk_dir)
            print "need update sdk version:", update_sdk_version

            if update_sdk_version:
                filepath = "src" + os.path.sep + os.path.sep.join(lk_package_name.split("."))+os.path.sep+"Versions.java"
                fp = open(os.path.join(lk_sdk_dir, filepath), "w")
                fp.write(JAVA_VERSION_CODE_FORMAT%(lk_package_name, revision))
                fp.close()

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    log_file_path = os.path.join(os.path.dirname(sys.path[0]), "log"+os.path.sep+"post-update.log")
    log_dir_path = os.path.dirname(log_file_path)
    if not os.path.isdir(log_dir_path):
        os.makedirs(log_dir_path)

    logFile = codecs.open(log_file_path, "a+", "utf-8")

    oldStdout = sys.stdout  
    sys.stdout = logFile

    post_update()

    sys.stdout = oldStdout