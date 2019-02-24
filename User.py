# PiCycle - Python Exersize Bike Trainer
# Copyright (C) 2019 Jason Birch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#/****************************************************************************/
#/* PiCycle - Python Exersize Bike Trainer.                                  */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2019-02-14 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* User class.                                                              */
#/****************************************************************************/


import os
import datetime


class User:
#/***************************/
#/* Define class constants. */
#/***************************/
   INCHES_TO_CM = 2.54
   INCHES_PER_MILE = 63360
   CM_PER_KM = 100000


   def __init__(self, NewID):
#  /**********************************/
# /* Intialise with default values. */
#/**********************************/
      self.ID = NewID
      self.Name = "CU" + str(self.ID)
      self.PersonalBestAvgSpeed = 0.0
      self.PersonalBestLapTime = datetime.timedelta(1, -1)
      self.LoadUser(self.Name + ".USR")


#/****************************************/
#/* Load user data from the user's file. */
#/****************************************/
   def LoadUser(self, FileName):
#  /******************************************/
# /* Load the last active user from a file. */
#/******************************************/
      if FileName == "" and os.path.isfile("USERS/DEFAULT.LD"):
         File = open("USERS/DEFAULT.LD", 'r', 0)
         FileName = File.readline()
         File.close()

#  /************************/
# /* Default user values. */
#/************************/
      self.Level = 99
      self.PlayMusic = "OFF"
      self.Units = "M"
      self.UnitsFine = "\""
      self.SpeedUnits = "MPH"
      self.UnitScale = self.INCHES_PER_MILE
      self.TotalPulseCount = 0
      self.NetworkStatus = "OFF"
      self.NetworkIP = "192.168.001.100"
      self.NetworkPort = "1024"

#  /**************************************/
# /* Load user values from user's file. */
#/**************************************/
      if os.path.isfile("USERS/" + FileName):
         File = open("USERS/" + FileName, 'r', 0)
         TextLine = "."
         while TextLine != "":
            TextLine = File.readline()
            TextLine = TextLine.replace("\n", "")
            if TextLine[:5] == "NAME=":
               self.Name = TextLine[5:]
            elif TextLine[:6] == "LEVEL=":
               self.Level = int(TextLine[6:])
            elif TextLine[:11] == "PLAY_MUSIC=":
               self.PlayMusic = TextLine[11:]
            elif TextLine[:6] == "UNITS=":
               self.Units = TextLine[6:]
               self.SwitchUnits(self.Units)
            elif TextLine[:18] == "TOTAL_PULSE_COUNT=":
               self.TotalPulseCount = int(TextLine[18:])
            elif TextLine[:14] == "NETWORK_STATUS=":
               self.NetworkStatus = TextLine[14:]
            elif TextLine[:11] == "NETWORK_IP=":
               self.NetworkIP = TextLine[11:]
            elif TextLine[:13] == "NETWORK_PORT=":
               self.NetworkPort = str(TextLine[13:])
         File.close()


#/**************************************/
#/* Save user data to the user's file. */
#/**************************************/
   def SaveUser(self, FileName):
      File = open("USERS/DEFAULT.LD", 'w', 0)
      File.write(FileName)
      File.close()

      File = open("USERS/" + FileName, 'w', 0)
      File.write("NAME=" + self.Name + "\n")
      File.write("LEVEL=" + str(self.Level) + "\n")
      File.write("UNITS=" + self.Units + "\n")
      File.write("PLAY_MUSIC=" + self.PlayMusic + "\n")
      File.write("TOTAL_PULSE_COUNT=" + str(self.TotalPulseCount) + "\n")
      File.write("NETWORK_STATUS=" + self.NetworkStatus + "\n")
      File.write("NETWORK_IP=" + self.NetworkIP + "\n")
      File.write("NETWORK_PORT=" + self.NetworkPort + "\n")
      File.close()


#/******************************************************/
#/* Load user's event data from the user's event file. */
#/******************************************************/
   def LoadUserEvent(self, FileName):
      self.PersonalBestAvgSpeed = 0.0
      self.PersonalBestLapTime = datetime.timedelta(1, -1)

      if not os.path.isdir("USER_EVENT/" + self.Name):
         os.mkdir("USER_EVENT/" + self.Name)

      if os.path.isfile("USER_EVENT/" + self.Name + "/" + FileName):
         File = open("USER_EVENT/" + self.Name + "/" + FileName, 'r', 0)
         TextLine = "."
         while TextLine != "":
            TextLine = File.readline()
            if TextLine[:23] == "PERSONAL_BEST_LAP_TIME=":
               self.PersonalBestLapTime = datetime.timedelta(0, int(TextLine[23:]))
            elif TextLine[:24] == "PERSONAL_BEST_AVG_SPEED=":
               self.PersonalBestAvgSpeed = float(TextLine[24:])


#/****************************************************/
#/* Save user's event data to the user's event file. */
#/****************************************************/
   def SaveUserEvent(self, FileName):
      File = open("USER_EVENT/" + self.Name + "/" + FileName, 'w', 0)
      File.write("PERSONAL_BEST_LAP_TIME=" + str(self.PersonalBestLapTime.seconds) + "\n")
      File.write("PERSONAL_BEST_AVG_SPEED=" + str(self.PersonalBestAvgSpeed) + "\n")
      File.close()


#/******************/
#/* Get user name. */
#/******************/
   def GetName(self):
      return self.Name


#/******************/
#/* Set user name. */
#/******************/
   def SetName(self, NewName):
      self.Name = NewName


#/*******************/
#/* Get user level. */
#/*******************/
   def GetLevel(self):
      return self.Level


#/*******************/
#/* Set user level. */
#/*******************/
   def SetLevel(self, NewLevel):
      self.Level = int(NewLevel)


#/***************************/
#/* Get user best lap time. */
#/***************************/
   def GetPersonalBestLapTime(self):
      return self.PersonalBestLapTime


#/***************************/
#/* Set user best lap time. */
#/***************************/
   def SetPersonalBestLapTime(self, NewLapTime):
      self.PersonalBestLapTime = NewLapTime


#/********************************/
#/* Get user best average speed. */
#/********************************/
   def GetPersonalBestAvgSpeed(self):
      return self.PersonalBestAvgSpeed


#/********************************/
#/* Set user best average speed. */
#/********************************/
   def SetPersonalBestAvgSpeed(self, NewPersonalBestAvgSpeed):
      self.PersonalBestAvgSpeed = NewPersonalBestAvgSpeed


#/***************************************************/
#/* Get appropreate scaling value to convert units. */
#/***************************************************/
   def GetUnitScale(self):
      return self.UnitScale


#/***************************************************/
#/* Set appropreate scaling value to convert units. */
#/***************************************************/
   def GetUnitScale(self):
      return self.UnitScale


#/*******************************************/
#/* Get user preference for distance units. */
#/*******************************************/
   def GetUnits(self):
      return self.Units


#/************************************************/
#/* Get user preference for fine distance units. */
#/************************************************/
   def GetUnitsFine(self):
      return self.UnitsFine


#/****************************************/
#/* Get user preference for speed units. */
#/****************************************/
   def GetSpeedUnits(self):
      return self.SpeedUnits


#/*************************************************************/
#/* Change user units preference between metric and imperial. */
#/*************************************************************/
   def SwitchUnits(self, NewUnits = ""):
      if NewUnits == "Km" or (NewUnits == "" and self.Units == "M"):
         self.UnitScale = self.CM_PER_KM
         self.Units = "Km"
         self.UnitsFine = "cm"
         self.SpeedUnits = "Km/H"
      else:
         self.UnitScale = self.INCHES_PER_MILE
         self.Units = "M"
         self.UnitsFine = "\""
         self.SpeedUnits = "MPH"

      return self.Units


#/***********************************/
#/* Get the current network status. */
#/***********************************/
   def GetNetworkStatus(self):
      return self.NetworkStatus


#/***********************************/
#/* Set the current network status. */
#/***********************************/
   def SwitchNetworkStatus(self):
      if self.NetworkStatus == "OFF":
         self.NetworkStatus = "ON"
      else:
         self.NetworkStatus = "OFF"


#/**************************************/
#/* Get the current play music status. */
#/**************************************/
   def GetPlayMusic(self):
      return self.PlayMusic


#/**************************************/
#/* Set the current play music status. */
#/**************************************/
   def SwitchPlayMusic(self):
      if self.PlayMusic == "OFF":
         self.PlayMusic = "ON"
      else:
         self.PlayMusic = "OFF"


#/*******************************/
#/* Get the current network IP. */
#/*******************************/
   def GetNetworkIP(self):
      return self.NetworkIP


#/*******************************/
#/* Set the current network IP. */
#/*******************************/
   def SetNetworkIP(self, NewNetworkIP):
      self.NetworkIP = NewNetworkIP


#/*********************************/
#/* Get the current network Port. */
#/*********************************/
   def GetNetworkPort(self):
      return self.NetworkPort


#/*********************************/
#/* Set the current network Port. */
#/*********************************/
   def SetNetworkPort(self, NewNetworkPort):
      self.NetworkPort = NewNetworkPort


#/***********************************************/
#/* Get the users total distance sensor pulses. */
#/***********************************************/
   def GetTotalPulseCount(self):
      return self.TotalPulseCount


#/***********************************************/
#/* Set the users total distance sensor pulses. */
#/***********************************************/
   def SetTotalPulseCount(self, NewTotalPulseCount):
      self.TotalPulseCount = NewTotalPulseCount

