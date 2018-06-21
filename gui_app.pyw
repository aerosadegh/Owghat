# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import json
import datetime as dt
import jdatetime as jdt
import pytz
from time import sleep
import sys
import persian as pr
import locale
from pprint import pprint

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
    
    

data = None

def update_citys():
    res_citys = requests.get("https://prayer.aviny.com/api/city")
    try:
        return json.loads(res_citys.text)

    except Exception as e:
        print('Error Occured:\n', e)
        #print(dir(e))
        #print(str(e.reason)[12:])

def update_provice():
    res_province = requests.get("https://prayer.aviny.com/api/province")
    try:
        return json.loads(res_province.text)

    except Exception as e:
        print('Error Occured:\n', e)
        #print(dir(e))
        #print(str(e.reason)[12:])


def update_country():
    res_country = requests.get("https://prayer.aviny.com/api/country")
    try:
        return json.loads(res_country.text)

    except Exception as e:
        print('Error Occured:\n', e)
        #print(dir(e))
        #print(str(e.reason)[12:])


def update_state(city_code):
    try:
        res_data = requests.get(f"https://prayer.aviny.com/api/prayertimes/{city_code:}" )
        return json.loads(res_data.text)
    
    except ConnectionError:
        print('Fake Data...')
        res_data = dict(zip(['Imsaak', 'Sunrise', 'Noon', 'Sunset', 'Maghreb', 'Midnight', 'TimeZone', 'CountryName', 
                         'TodayQamari', 'CityName'],
                        ['03:37:00', '06:11:00', '14:05:00', '18:19:00', '22:25:00', '00:48:00', "4.5", 
                         'ایران'  , '۱۴۳۷ رمضان 04',  'تهران']))
        pprint(res_data)
        return res_data
    except Exception as e:
        print('Error Occured:\n', e)
        #print(dir(e))
        #print(str(e.reason)[12:])        

def utc_to_local(utc_dt, tz='3.5'):
    local_tz = pytz.FixedOffset(float(tz)*60)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    ldt = local_tz.normalize(local_dt)
    return ldt


def pars_delta(time_dalta):
    #print(time_dalta.days, time_dalta.seconds, time_dalta.microseconds)
    d = divmod(time_dalta.seconds,86400)  # days
    h = divmod(d[1],3600)  # hours
    m = divmod(h[1],60)  # minutes
    s = m[1]  # seconds
    return h[0], m[0], s
    

def dater(now_datetime, time_simple):
    if isinstance(time_simple, str):
        if time_simple[:2] == '00':
            now_datetime += jdt.timedelta(days=1)
            
        time_simple = jdt.datetime.strptime(time_simple, '%H:%M:%S')
    
    return jdt.datetime(now_datetime.year, now_datetime.month, now_datetime.day, 
                        time_simple.hour, time_simple.minute, time_simple.second,
                        tzinfo=now_datetime.tzinfo)   


def event_manager(now, data, length=False):
    keys = ['Imsaak', 'Sunrise',
            'Noon', 'Sunset',
            'Maghreb', 'Midnight']
    
    if length:
        day = dater(now, data["Maghreb"]) - dater(now, data["Imsaak"])
        str_day = "{:02d}:{:02d}:{:02d}".format(*pars_delta(day))
        night = dater(now, data['Midnight'])  - dater(now, data["Maghreb"]) 
        night += night + jdt.timedelta(minutes=10)
        str_night = "{:02d}:{:02d}:{:02d}".format(*pars_delta(night))
        return str_day , str_night
    
    now_60sub = now - jdt.timedelta(minutes=1)
    for key in keys:
        chk = dater(now, data[key]) - now_60sub
        #print(chk.days, chk.seconds)
        if chk.days == 0:
            status = dater(now, data[key]) - now
            return status, key
    return None


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(1100, 751)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("overtime.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Frame.setWindowIcon(icon)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayoutWidget = QtGui.QWidget(Frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1081, 701))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.gridLayout.setMargin(5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_1v = QtGui.QLabel(self.gridLayoutWidget)
        self.label_1v.setFrameShape(QtGui.QFrame.Panel)
        self.label_1v.setFrameShadow(QtGui.QFrame.Raised)
        self.label_1v.setLineWidth(2)
        self.label_1v.setTextFormat(QtCore.Qt.RichText)
        self.label_1v.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1v.setObjectName(_fromUtf8("label_1v"))
        self.gridLayout.addWidget(self.label_1v, 5, 0, 1, 1)
        self.label_y3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_y3.setObjectName(_fromUtf8("label_y3"))
        self.gridLayout.addWidget(self.label_y3, 3, 0, 1, 1)
        self.label_y1 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_y1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_y1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_y1.setObjectName(_fromUtf8("label_y1"))
        self.gridLayout.addWidget(self.label_y1, 1, 0, 1, 1)
        self.label_y2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_y2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_y2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_y2.setObjectName(_fromUtf8("label_y2"))
        self.gridLayout.addWidget(self.label_y2, 2, 0, 1, 1)
        self.label_3v = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3v.setFrameShape(QtGui.QFrame.Panel)
        self.label_3v.setFrameShadow(QtGui.QFrame.Raised)
        self.label_3v.setLineWidth(2)
        self.label_3v.setTextFormat(QtCore.Qt.RichText)
        self.label_3v.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3v.setObjectName(_fromUtf8("label_3v"))
        self.gridLayout.addWidget(self.label_3v, 5, 2, 1, 1)
        self.label_4v = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4v.setFrameShape(QtGui.QFrame.Panel)
        self.label_4v.setFrameShadow(QtGui.QFrame.Raised)
        self.label_4v.setLineWidth(2)
        self.label_4v.setTextFormat(QtCore.Qt.RichText)
        self.label_4v.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4v.setObjectName(_fromUtf8("label_4v"))
        self.gridLayout.addWidget(self.label_4v, 5, 3, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(70, 0))
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setStyleSheet(_fromUtf8("color:rgb(0, 85, 127)"))
        self.label_3.setFrameShape(QtGui.QFrame.Box)
        self.label_3.setFrameShadow(QtGui.QFrame.Raised)
        self.label_3.setLineWidth(2)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 4, 2, 1, 1)
        self.label_d2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_d2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_d2.setObjectName(_fromUtf8("label_d2"))
        self.gridLayout.addWidget(self.label_d2, 2, 3, 1, 1)
        self.label_2v = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2v.setFrameShape(QtGui.QFrame.Panel)
        self.label_2v.setFrameShadow(QtGui.QFrame.Raised)
        self.label_2v.setLineWidth(2)
        self.label_2v.setTextFormat(QtCore.Qt.RichText)
        self.label_2v.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2v.setObjectName(_fromUtf8("label_2v"))
        self.gridLayout.addWidget(self.label_2v, 5, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6.setMinimumSize(QtCore.QSize(70, 0))
        self.label_6.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_6.setStyleSheet(_fromUtf8("color:rgb(0, 85, 127)"))
        self.label_6.setFrameShape(QtGui.QFrame.Box)
        self.label_6.setFrameShadow(QtGui.QFrame.Raised)
        self.label_6.setLineWidth(2)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 4, 5, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(70, 0))
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setStyleSheet(_fromUtf8("color:rgb(0, 85, 127)"))
        self.label_2.setFrameShape(QtGui.QFrame.Box)
        self.label_2.setFrameShadow(QtGui.QFrame.Raised)
        self.label_2.setLineWidth(2)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 1, 1, 1)
        self.label_6v = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6v.setFrameShape(QtGui.QFrame.Panel)
        self.label_6v.setFrameShadow(QtGui.QFrame.Raised)
        self.label_6v.setLineWidth(2)
        self.label_6v.setTextFormat(QtCore.Qt.RichText)
        self.label_6v.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6v.setObjectName(_fromUtf8("label_6v"))
        self.gridLayout.addWidget(self.label_6v, 5, 5, 1, 1)
        self.label_d1 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_d1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_d1.setObjectName(_fromUtf8("label_d1"))
        self.gridLayout.addWidget(self.label_d1, 1, 3, 1, 1)
        self.label_d3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_d3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_d3.setObjectName(_fromUtf8("label_d3"))
        self.gridLayout.addWidget(self.label_d3, 3, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(70, 0))
        self.label_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_4.setStyleSheet(_fromUtf8("color:rgb(0, 85, 127)"))
        self.label_4.setFrameShape(QtGui.QFrame.Box)
        self.label_4.setFrameShadow(QtGui.QFrame.Raised)
        self.label_4.setLineWidth(2)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 3, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setMinimumSize(QtCore.QSize(70, 0))
        self.label_5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_5.setStyleSheet(_fromUtf8("color:rgb(0, 85, 127)"))
        self.label_5.setFrameShape(QtGui.QFrame.Box)
        self.label_5.setFrameShadow(QtGui.QFrame.Raised)
        self.label_5.setLineWidth(2)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 4, 1, 1)
        self.label_1 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_1.setMinimumSize(QtCore.QSize(70, 0))
        self.label_1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_1.setStyleSheet(_fromUtf8("color:rgb(0, 85, 127)"))
        self.label_1.setFrameShape(QtGui.QFrame.Box)
        self.label_1.setFrameShadow(QtGui.QFrame.Raised)
        self.label_1.setLineWidth(2)
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.gridLayout.addWidget(self.label_1, 4, 0, 1, 1)
        self.label_5v = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5v.setFrameShape(QtGui.QFrame.Panel)
        self.label_5v.setFrameShadow(QtGui.QFrame.Raised)
        self.label_5v.setLineWidth(2)
        self.label_5v.setTextFormat(QtCore.Qt.RichText)
        self.label_5v.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5v.setObjectName(_fromUtf8("label_5v"))
        self.gridLayout.addWidget(self.label_5v, 5, 4, 1, 1)
        self.label_country = QtGui.QLabel(self.gridLayoutWidget)
        self.label_country.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_country.setObjectName(_fromUtf8("label_country"))
        self.gridLayout.addWidget(self.label_country, 0, 0, 1, 1)
        self.toolBox = QtGui.QToolBox(self.gridLayoutWidget)
        self.toolBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.toolBox.setAutoFillBackground(False)
        self.toolBox.setLocale(QtCore.QLocale(QtCore.QLocale.Persian, QtCore.QLocale.Iran))
        self.toolBox.setFrameShape(QtGui.QFrame.WinPanel)
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.page_remain = QtGui.QWidget()
        self.page_remain.setGeometry(QtCore.QRect(0, 0, 1067, 105))
        self.page_remain.setObjectName(_fromUtf8("page_remain"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.page_remain)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1061, 101))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_remain = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_remain.setMargin(0)
        self.gridLayout_remain.setObjectName(_fromUtf8("gridLayout_remain"))
        self.label_len_night = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_len_night.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_len_night.setFrameShape(QtGui.QFrame.Panel)
        self.label_len_night.setFrameShadow(QtGui.QFrame.Raised)
        self.label_len_night.setLineWidth(2)
        self.label_len_night.setMidLineWidth(2)
        self.label_len_night.setTextFormat(QtCore.Qt.RichText)
        self.label_len_night.setAlignment(QtCore.Qt.AlignCenter)
        self.label_len_night.setObjectName(_fromUtf8("label_len_night"))
        self.gridLayout_remain.addWidget(self.label_len_night, 1, 1, 1, 1)
        self.label_nlen = QtGui.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_nlen.setFont(font)
        self.label_nlen.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_nlen.setFrameShape(QtGui.QFrame.Box)
        self.label_nlen.setTextFormat(QtCore.Qt.RichText)
        self.label_nlen.setAlignment(QtCore.Qt.AlignCenter)
        self.label_nlen.setObjectName(_fromUtf8("label_nlen"))
        self.gridLayout_remain.addWidget(self.label_nlen, 0, 1, 1, 1)
        self.label_len_day = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_len_day.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_len_day.setFrameShape(QtGui.QFrame.Panel)
        self.label_len_day.setFrameShadow(QtGui.QFrame.Raised)
        self.label_len_day.setLineWidth(2)
        self.label_len_day.setMidLineWidth(2)
        self.label_len_day.setTextFormat(QtCore.Qt.RichText)
        self.label_len_day.setAlignment(QtCore.Qt.AlignCenter)
        self.label_len_day.setObjectName(_fromUtf8("label_len_day"))
        self.gridLayout_remain.addWidget(self.label_len_day, 1, 0, 1, 1)
        self.label_dlen = QtGui.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_dlen.setFont(font)
        self.label_dlen.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_dlen.setFrameShape(QtGui.QFrame.Box)
        self.label_dlen.setTextFormat(QtCore.Qt.RichText)
        self.label_dlen.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dlen.setObjectName(_fromUtf8("label_dlen"))
        self.gridLayout_remain.addWidget(self.label_dlen, 0, 0, 1, 1)
        self.label_remain = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_remain.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_remain.setTextFormat(QtCore.Qt.RichText)
        self.label_remain.setAlignment(QtCore.Qt.AlignCenter)
        self.label_remain.setObjectName(_fromUtf8("label_remain"))
        self.gridLayout_remain.addWidget(self.label_remain, 0, 2, 2, 1)
        self.gridLayout_remain.setRowMinimumHeight(0, 1)
        self.gridLayout_remain.setRowMinimumHeight(1, 1)
        self.gridLayout_remain.setColumnStretch(0, 1)
        self.gridLayout_remain.setColumnStretch(1, 1)
        self.gridLayout_remain.setColumnStretch(2, 2)
        self.toolBox.addItem(self.page_remain, _fromUtf8(""))
        self.page_cermony = QtGui.QWidget()
        self.page_cermony.setGeometry(QtCore.QRect(0, 0, 1067, 105))
        self.page_cermony.setObjectName(_fromUtf8("page_cermony"))
        self.label_cermony = QtGui.QLabel(self.page_cermony)
        self.label_cermony.setGeometry(QtCore.QRect(0, 0, 1061, 101))
        self.label_cermony.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_cermony.setTextFormat(QtCore.Qt.RichText)
        self.label_cermony.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cermony.setObjectName(_fromUtf8("label_cermony"))
        self.toolBox.addItem(self.page_cermony, _fromUtf8(""))
        self.gridLayout.addWidget(self.toolBox, 6, 0, 1, 6)
        self.label_B1 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_B1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_B1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_B1.setObjectName(_fromUtf8("label_B1"))
        self.gridLayout.addWidget(self.label_B1, 1, 1, 1, 2)
        self.label_B2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_B2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_B2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_B2.setObjectName(_fromUtf8("label_B2"))
        self.gridLayout.addWidget(self.label_B2, 2, 1, 1, 2)
        self.label_B3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_B3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_B3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_B3.setObjectName(_fromUtf8("label_B3"))
        self.gridLayout.addWidget(self.label_B3, 3, 1, 1, 2)
        self.label_A1 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_A1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_A1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_A1.setObjectName(_fromUtf8("label_A1"))
        self.gridLayout.addWidget(self.label_A1, 1, 4, 1, 2)
        self.label_A2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_A2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_A2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_A2.setObjectName(_fromUtf8("label_A2"))
        self.gridLayout.addWidget(self.label_A2, 2, 4, 1, 2)
        self.label_A3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_A3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_A3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_A3.setObjectName(_fromUtf8("label_A3"))
        self.gridLayout.addWidget(self.label_A3, 3, 4, 1, 2)
        self.comboBox_country = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBox_country.setObjectName(_fromUtf8("comboBox_country"))
        self.gridLayout.addWidget(self.comboBox_country, 0, 1, 1, 1)
        self.label_city = QtGui.QLabel(self.gridLayoutWidget)
        self.label_city.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_city.setLineWidth(2)
        self.label_city.setMidLineWidth(4)
        self.label_city.setObjectName(_fromUtf8("label_city"))
        self.gridLayout.addWidget(self.label_city, 0, 2, 1, 1)
        self.comboBox_city = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBox_city.setObjectName(_fromUtf8("comboBox_city"))
        self.gridLayout.addWidget(self.comboBox_city, 0, 3, 1, 3)
        self.gridLayout.setColumnMinimumWidth(0, 15)
        self.gridLayout.setColumnMinimumWidth(1, 5)
        self.gridLayout.setColumnMinimumWidth(2, 5)
        self.gridLayout.setColumnMinimumWidth(3, 5)
        self.gridLayout.setColumnMinimumWidth(4, 5)
        self.gridLayout.setColumnMinimumWidth(5, 5)
        self.gridLayout.setRowMinimumHeight(0, 60)
        self.gridLayout.setRowMinimumHeight(1, 60)
        self.gridLayout.setRowMinimumHeight(2, 60)
        self.gridLayout.setRowMinimumHeight(3, 60)
        self.gridLayout.setRowMinimumHeight(4, 60)
        self.gridLayout.setRowMinimumHeight(5, 60)
        self.gridLayout.setRowMinimumHeight(6, 60)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 1)
        self.gridLayout.setColumnStretch(5, 1)
        self.gridLayout.setRowStretch(0, 3)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setRowStretch(4, 1)
        self.gridLayout.setRowStretch(5, 1)
        self.gridLayout.setRowStretch(6, 3)

        self.retranslateUi(Frame)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Frame)
        Frame.setTabOrder(self.comboBox_city, self.comboBox_country)
        
        self.addition_ui()

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(_translate("Frame", "Owghat", None))
        self.label_1v.setText(_translate("Frame", "TextLabel", None))
        self.label_y3.setText(_translate("Frame", "TextLabel", None))
        self.label_y1.setText(_translate("Frame", "TextLabel", None))
        self.label_y2.setText(_translate("Frame", "TextLabel", None))
        self.label_3v.setText(_translate("Frame", "TextLabel", None))
        self.label_4v.setText(_translate("Frame", "TextLabel", None))
        self.label_3.setText(_translate("Frame", "غروب آفتاب", None))
        self.label_d2.setText(_translate("Frame", "TextLabel", None))
        self.label_2v.setText(_translate("Frame", "TextLabel", None))
        self.label_6.setText(_translate("Frame", "اذان صبح", None))
        self.label_2.setText(_translate("Frame", "اذان مغرب", None))
        self.label_6v.setText(_translate("Frame", "TextLabel", None))
        self.label_d1.setText(_translate("Frame", "TextLabel", None))
        self.label_d3.setText(_translate("Frame", "TextLabel", None))
        self.label_4.setText(_translate("Frame", "اذان ظهر", None))
        self.label_5.setText(_translate("Frame", "طلوع آفتاب", None))
        self.label_1.setText(_translate("Frame", "نیمه شب", None))
        self.label_5v.setText(_translate("Frame", "TextLabel", None))
        self.label_country.setText(_translate("Frame", "Country", None))
        self.label_len_night.setText(_translate("Frame", "باقیمانده", None))
        self.label_nlen.setText(_translate("Frame", "طول شب", None))
        self.label_len_day.setText(_translate("Frame", "باقیمانده", None))
        self.label_dlen.setText(_translate("Frame", "طول روز", None))
        self.label_remain.setText(_translate("Frame", "باقیمانده", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_remain), _translate("Frame", "وضعیت", None))
        self.label_cermony.setText(_translate("Frame", "مناسبت", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_cermony), _translate("Frame", "مناسبت", None))
        self.label_B1.setText(_translate("Frame", "TextLabel", None))
        self.label_B2.setText(_translate("Frame", "TextLabel", None))
        self.label_B3.setText(_translate("Frame", "TextLabel", None))
        self.label_A1.setText(_translate("Frame", "TextLabel", None))
        self.label_A2.setText(_translate("Frame", "TextLabel", None))
        self.label_A3.setText(_translate("Frame", "TextLabel", None))
        self.label_city.setText(_translate("Frame", "City", None))
        
    def addition_ui(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_status)
        self.timer.start(1000)
        
        cit = update_citys()
        prv = update_provice()
        cnt = update_country()
        prd = {pp['Code']:pp['Name'] for pp in prv}
        cnd = {pp['Code']:pp['Name'] for pp in cnt}
        c = ['{:} :: {:}'.format(city['Name'], prd[city['Province_Code']] if city['Country_Code']==1 else cnd[city['Country_Code']]) for city in cit]
        self.comboBox_city.addItems(c)
        self.comboBox_country.addItem('All')
        self.comboBox_city.currentIndexChanged.connect(self.citychange)
        self.city_index = 1
        self.show_status()
        self.set_date_labels()
        
        
    def citychange(self, i):
        global data
        self.city_index = i+1
        data = update_state(self.city_index)
        self.show_status()
        self.set_date_labels()

    def show_status(self):
        global data
        
        df = dict(zip(['Imsaak', 'Sunrise', 'Noon', 'Sunset', 'Maghreb', 'Midnight'],
                    ['اذان صبح', 'طلوع آفتاب', 'اذان ظهر', 'غروب آفتاب', 'اذان مغرب', 'نیمه شب']))
        
        dlabel = dict(zip(['Imsaak', 'Sunrise', 'Noon', 'Sunset', 'Maghreb', 'Midnight'],
                    ['label_6v', 'label_5v', 'label_4v', 'label_3v', 'label_2v', 'label_1v']))

        
        if not data:
            data = update_state(self.city_index)
        now = utc_to_local(jdt.datetime.utcnow(), data['TimeZone'])
        
        event_now = event_manager(now, data)
        
        if not event_now:
            print('updateing data...')
            data = update_state(self.city_index)
            now = utc_to_local(jdt.datetime.utcnow(), data['TimeZone'])
            event_now = event_manager(now, data)
        else:
            stat, key = event_now
            
        exec("""self.{:}.setStyleSheet('color:rgb(0, 170, 0)');self.{:}.setStyleSheet('');""".format(dlabel[key], dlabel[key][:-1]))
        self.label_remain.setStyleSheet('')
            
        if stat.days == -1:
            #print(key)
            self.set_date_labels()
            self.label_remain.setStyleSheet('color:rgb(0, 170, 0)')
            self.label_remain.setText(_translate("Frame", pr.enToPersianNumb('> {:}'.format(df[key])), None))
            
        else:
            then = stat.seconds
            d = divmod(then,86400)  # days
            h = divmod(d[1],3600)  # hours
            m = divmod(h[1],60)  # minutes
            s = m[1]  # seconds
            #print(key)
            dkey = df[key]
            #print('%d hours, %d minutes, %d seconds to %s' % (h[0],m[0],s, dkey) )
            h0 = h[0]
            m0 = m[0]
            if h == 0:        
                self.label_remain.setText(_translate("Frame", pr.enToPersianNumb(f'> {m0:02d}:{s:02d} دقیقه تا {dkey:}'), None)) 
            else:
                self.label_remain.setText(_translate("Frame", pr.enToPersianNumb(f'> {h0:02d}:{m0:02d}:{s:02d} تا {dkey:} '), None))
    
    def set_date_labels(self):
        Ly, Lw, Lm, Ld = dt.datetime.strftime(dt.datetime.utcnow(), '%Y %A %b %d').split(' ')
        Qd, Qm, Qy = data['TodayQamari'].split(' ')
        locale.setlocale(locale.LC_ALL, "fa_IR")
        Jy, Jm, Jd = jdt.datetime.strftime(jdt.datetime.utcnow(), '%Y %b %d').split(' ')
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        wday = dict(zip(['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday'],
                       [('دوشنبه', 'الإثنين'),
                        ('سه\u200cشنبه', 'الثلاثاء'),
                        ('چهارشنبه', 'الأربعاء'),
                        ('پنجشنبه', 'الخميس'),
                        ('جمعه', 'الجمعة'),
                        ('شنبه', 'السبت'),
                        ('یکشنبه', 'الأحَد'),]))
        now = utc_to_local(jdt.datetime.utcnow(), data['TimeZone'])
        ld , ln = event_manager(now, data , True)
        
        self.label_6v.setText(_translate("Frame", pr.enToPersianNumb(data['Imsaak']), None)) 
        self.label_5v.setText(_translate("Frame", pr.enToPersianNumb(data['Sunrise']), None)) 
        self.label_4v.setText(_translate("Frame", pr.enToPersianNumb(data['Noon']), None)) 
        self.label_3v.setText(_translate("Frame", pr.enToPersianNumb(data['Sunset']), None)) 
        self.label_2v.setText(_translate("Frame", pr.enToPersianNumb(data['Maghreb']), None)) 
        self.label_1v.setText(_translate("Frame", pr.enToPersianNumb(data['Midnight']), None)) 
        
        self.label_A1.setText(_translate("Frame", wday[Lw][0], None)) 
        self.label_A2.setText(_translate("Frame", wday[Lw][1], None)) 
        self.label_A3.setText(_translate("Frame", Lw, None)) 
        
        self.label_d1.setText(_translate("Frame", pr.enToPersianNumb(Jd), None)) 
        self.label_d2.setText(_translate("Frame", pr.enToPersianNumb(Qd), None)) 
        self.label_d3.setText(_translate("Frame", Ld, None)) 
        
        self.label_B1.setText(_translate("Frame", pr.enToPersianNumb(Jm), None))
        self.label_B2.setText(_translate("Frame", pr.enToPersianNumb(Qm), None))
        self.label_B3.setText(_translate("Frame", Lm, None))
        
        self.label_y1.setText(_translate("Frame", pr.enToPersianNumb(Jy), None))
        self.label_y2.setText(_translate("Frame", pr.enToPersianNumb(Qy), None))
        self.label_y3.setText(_translate("Frame", Ly, None))
        
        self.label_len_day.setText(_translate("Frame", pr.enToPersianNumb(ld), None))
        self.label_len_night.setText(_translate("Frame", pr.enToPersianNumb(ln), None))
        
        self.label_remain.setStyleSheet('')
        dlabel = dict(zip(['Imsaak', 'Sunrise', 'Noon', 'Sunset', 'Maghreb', 'Midnight'],
                    ['label_6v', 'label_5v', 'label_4v', 'label_3v', 'label_2v', 'label_1v']))
        for key in dlabel.keys():
            exec("""self.{:}.setStyleSheet('');self.{:}.setStyleSheet('color:rgb(0, 85, 127)'); """.format(dlabel[key], dlabel[key][:-1]))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Frame = QtGui.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())

