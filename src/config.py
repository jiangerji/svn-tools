#encoding=utf-8

import os
import sys

def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    #如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

# 用于生成版本代码的模板
_code_template = os.path.join(cur_file_dir(), "config-code-template")
JAVA_VERSION_CODE_FORMAT = open(_code_template, "r").read()

# 需要依赖的svn库，更新需要将SDK的版本进行更新
DEPENDS_SVN = {}

"""
蓝港自主的svn配置
"""
LK_SDK_SVN = "eUsdk/branches/china-linekong/0.1.2/Native_SDK"
LK_SDK_DIR = None

eSdk_DEPENDS_SVN = [
    LK_SDK_SVN,
    "eUsdk/branches/common/LK_AntiRobot",
    "eUsdk/branches/china-linekong/0.1.2/eBilling_v2",
    "eUsdk/branches/china-linekong/0.1.2/LK_SDK_RES"
]

DEPENDS_SVN ["svn://192.168.41.231:7654/repos_esuite"] = [
    eSdk_DEPENDS_SVN,   # 需要监控的svn和该svn依赖的svn
    LK_SDK_DIR,         # 需要监控的svn目录位置
    "com.linekong.sdk.util" # 版本文件的报名
]

# ========================= 读取配置文件 =========================
import xml.etree.ElementTree as ET 
from xml.dom import minidom

def parse_project(root):
    projects = []
    for element in root.getElementsByTagName("project"):
        element_url = element.getAttribute("url")

        element_dir = None
        dir_tags = element.getElementsByTagName("dir")
        if len(dir_tags) > 0:
            try:
                element_dir = dir_tags[0].childNodes[0].nodeValue
            except Exception, e:
                pass

        # 获取Versions.java的包名
        element_version_package = None
        tags = element.getElementsByTagName("name")
        if len(tags) > 0:
            try:
                element_version_package = tags[0].childNodes[0].nodeValue
            except Exception, e:
                pass
        else:
            print "没有配置Versions.java的包名！"
            exit()

        depend_svns = [element_url]
        tags = element.getElementsByTagName("depends-svn")
        for tag in tags:
            url_tags = tag.getElementsByTagName("url")
            for url_tag in url_tags:
                try:
                    depend_svns.append(url_tag.childNodes[0].nodeValue)
                except:
                    pass

        print element_url
        print element_dir
        print element_version_package
        print depend_svns
        project = {}
        project["url"] = element_url
        project["dir"] = element_dir
        project["package"] = element_version_package
        project["depends"] = depend_svns

        projects.append(project)
    return projects

import svn_common

svn_config_file = os.path.join(svn_common.cur_file_dir(), "config-svn-depends.xml")

xmldoc = minidom.parse(svn_config_file)
firstNode = xmldoc.documentElement
pNode = firstNode

pNode.getElementsByTagName("svn-root")

for element in pNode.getElementsByTagName("svn-root"):
    element_url = element.getAttribute("url")
    
    DEPENDS_SVN[element_url] = parse_project(element)
    print DEPENDS_SVN
