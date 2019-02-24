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
#/* Event finite state machine class.                                        */
#/****************************************************************************/


import os
import datetime
import pygame


class Event:
#  /************************/
# /* Define event states. */
#/************************/
   STATE_EVENT_OFF = 0
   STATE_EVENT_FALSE_START = 1
   STATE_EVENT_START = 2
   STATE_EVENT_BRAKE = 3
   STATE_EVENT_READY = 4
   STATE_EVENT_GO = 5
   STATE_EVENT_RUNNING = 6
   STATE_EVENT_PAUSED = 7
   STATE_EVENT_FINISH = 8


   def __init__(self):
#  /*******************************/
# /* Initialise class variables. */
#/*******************************/
      self.WavBrake = pygame.mixer.Sound("SOUND/brake.wav")
      self.WavReady = pygame.mixer.Sound("SOUND/ready.wav")
      self.WavGo = pygame.mixer.Sound("SOUND/go.wav")
      self.WavFinish = pygame.mixer.Sound("SOUND/finish.wav")
      self.RecordAvgSpeed = 0.0
      self.RecordAvgSpeedUser = "CU1"
      self.RecordDistance = 0.0
      self.RecordDistanceUser = "CU1"
      self.RecordFinishDistance = 0.0
      self.RecordFinishDistanceUser = "CU1"
      self.RecordLapTime = datetime.timedelta(1, -1)
      self.RecordLapTimeUser = "CU1"
      self.RecordFinishTime = datetime.timedelta(1, -1)
      self.RecordFinishTimeUser = "CU1"
      self.Reset(0, [])


#/************************************/
#/* Reset class to known idle state. */
#/************************************/
   def Reset(self, Cyclist, Cycles):
      self.ThisCyclist = Cyclist
      self.ThisCycles = Cycles

      self.EventName = "DEMO"
      self.Start(self.EventName)


#/*******************/
#/* Start an event. */
#/*******************/
   def Start(self, NewEventName):
#  /************************************************************************/
# /* Reset all cycles and set their speed range to user's selected level. */
#/************************************************************************/
      for Count in range(len(self.ThisCycles)):
         self.ThisCycles[Count].Reset()
         self.ThisCycles[Count].SetSpeedRange(self.ThisCycles[self.ThisCyclist].GetUser().GetLevel() - 5, self.ThisCycles[self.ThisCyclist].GetUser().GetLevel() + 5)

#  /*****************************************************/
# /* Load the relavent event data from the event file. */
#/*****************************************************/
      self.EventName = NewEventName
      self.LoadEvent(self.EventName + ".EVT")

#  /*********************************************************************/
# /* Load the user's historic date for the event from the user's file. */
#/*********************************************************************/
      if self.ThisCycles:
         self.ThisCycles[self.ThisCyclist].GetUser().LoadUserEvent(self.EventName + ".UEV")

#  /****************************************************************/
# /* Load the records for this event from the event records file. */
#/****************************************************************/
      self.LoadRecords(self.EventName + ".REC")

#  /**********************************************************/
# /* Set the timers to the current date and time initially. */
#/**********************************************************/
      self.PauseStartTime = datetime.datetime.now()
      self.PauseTime = datetime.datetime.now()
      self.StartTime = datetime.datetime.now()
      self.FinishTime = datetime.datetime.now()
      self.StateTimer = datetime.datetime.now()


#/*************************************************/
#/* Load event data from the specific event file. */
#/*************************************************/
   def LoadEvent(self, FileName):
      self.EventState = self.STATE_EVENT_START
      self.ElapseTime = datetime.timedelta(0, 0)
      self.LapCount = 10
      self.LapDistance = 1.0

      File = open("EVENTS/" + FileName, 'r', 0)
      TextLine = "."
      while TextLine != "":
         TextLine = File.readline()
         if TextLine[:12] == "ELAPSE_TIME=":
            self.ElapseTime = datetime.timedelta(0, int(TextLine[12:]))
         elif TextLine[:10] == "LAP_COUNT=":
            self.LapCount = int(TextLine[10:])
         elif TextLine[:13] == "LAP_DISTANCE=":
            self.LapDistance = float(TextLine[13:])
         elif TextLine[:12] == "EVENT_STATE=":
            self.EventState = int(TextLine[12:])
      File.close()

      self.Distance = self.LapCount * self.LapDistance


#/************************************************************/
#/* Load event records from the specific event records file. */
#/************************************************************/
   def LoadRecords(self, FileName):
      self.RecordAvgSpeed = 0.0
      self.RecordAvgSpeedUser = "CU1"
      self.RecordDistance = 0.0
      self.RecordDistanceUser = "CU1"
      self.RecordFinishDistance = 0.0
      self.RecordFinishDistanceUser = "CU1"
      self.RecordLapTime = datetime.timedelta(1, -1)
      self.RecordLapTimeUser = "CU1"
      self.RecordFinishTime = datetime.timedelta(1, -1)
      self.RecordFinishTimeUser = "CU1"

      if os.path.isfile("USER_EVENT/" + FileName):
         File = open("USER_EVENT/" + FileName, 'r', 0)
         TextLine = "."
         while TextLine != "":
            TextLine = File.readline()
            if TextLine[:16] == "RECORD_LAP_TIME=":
               self.RecordLapTime = datetime.timedelta(0, int(TextLine[16:]))
            elif TextLine[:21] == "RECORD_LAP_TIME_USER=":
               self.RecordLapTimeUser = TextLine[21:24]
            elif TextLine[:17] == "RECORD_AVG_SPEED=":
               self.RecordAvgSpeed = float(TextLine[17:])
            elif TextLine[:22] == "RECORD_AVG_SPEED_USER=":
               self.RecordAvgSpeedUser = TextLine[22:25]
            elif TextLine[:16] == "RECORD_DISTANCE=":
               self.RecordDistance = float(TextLine[16:])
            elif TextLine[:21] == "RECORD_DISTANCE_USER=":
               self.RecordDistanceUser = TextLine[21:24]
            elif TextLine[:23] == "RECORD_FINISH_DISTANCE=":
               self.RecordFinishDistance = float(TextLine[23:])
            elif TextLine[:28] == "RECORD_FINISH_DISTANCE_USER=":
               self.RecordFinishDistanceUser = TextLine[28:31]
            elif TextLine[:19] == "RECORD_FINISH_TIME=":
               self.RecordFinishTime = datetime.timedelta(0, int(TextLine[19:]))
            elif TextLine[:24] == "RECORD_FINISH_TIME_USER=":
               self.RecordFinishTimeUser = TextLine[24:27]


#/**********************************************************/
#/* Save event records to the specific event records file. */
#/**********************************************************/
   def SaveRecords(self, FileName):
      File = open("USER_EVENT/" + FileName, 'w', 0)
      File.write("RECORD_LAP_TIME=" + str(self.RecordLapTime.seconds) + "\n")
      File.write("RECORD_LAP_TIME_USER=" + self.RecordLapTimeUser + "\n")
      File.write("RECORD_AVG_SPEED=" + str(self.RecordAvgSpeed) + "\n")
      File.write("RECORD_AVG_SPEED_USER=" + self.RecordAvgSpeedUser + "\n")
      File.write("RECORD_DISTANCE=" + str(self.RecordDistance) + "\n")
      File.write("RECORD_DISTANCE_USER=" + self.RecordDistanceUser + "\n")
      File.write("RECORD_FINISH_DISTANCE=" + str(self.RecordFinishDistance) + "\n")
      File.write("RECORD_FINISH_DISTANCE_USER=" + self.RecordFinishDistanceUser + "\n")
      File.write("RECORD_FINISH_TIME=" + str(self.RecordFinishTime.seconds) + "\n")
      File.write("RECORD_FINISH_TIME_USER=" + self.RecordFinishTimeUser + "\n")
      File.close()


#/********************************/
#/* Get the current event state. */
#/********************************/
   def GetState(self):
      return self.EventState


#/********************************/
#/* Set the current event state. */
#/********************************/
   def SetState(self, NewState):
      self.EventState = NewState


#/************************************/
#/* Called every application period. */
#/************************************/
   def Period(self):
#  /********************************************************************/
# /* Before the GO status, ensure the start time is the current time. */
#/********************************************************************/
      if self.EventState < self.STATE_EVENT_GO:
         self.StartTime = datetime.datetime.now()

#  /*************************************************************************/
# /* Before the FINISH status, ensure the finish time is the current time. */
#/*************************************************************************/
      if self.EventState < self.STATE_EVENT_FINISH:
         self.FinishTime = datetime.datetime.now()

      if self.EventState == self.STATE_EVENT_START:
#  /******************************************************************/
# /* Event Start Status: Move to Brake status and play brake sound. */
#/******************************************************************/
         self.EventState = self.STATE_EVENT_BRAKE
         self.WavBrake.play()
      elif self.EventState == self.STATE_EVENT_PAUSED:
#   /******************************************/
#  /* Event Paused Status: Adjust event      */
# /* start time to account for paused time. */
#/******************************************/
         self.StartTime = self.PauseStartTime + (datetime.datetime.now() - self.PauseTime)
         self.StateTimer = datetime.datetime.now()
      elif self.EventState == self.STATE_EVENT_FALSE_START:
#  /*****************************************************************/
# /* Event False Start Status: After 3 seconds, restart the event. */
#/*****************************************************************/
         if (datetime.datetime.now() - self.StateTimer).seconds >= 3:
            self.StateTimer = datetime.datetime.now()
            self.EventState = self.STATE_EVENT_BRAKE
      elif self.EventState == self.STATE_EVENT_BRAKE:
#   /**********************************************/
#  /* Event Brake Status: After 3 seconds,       */
# /* move to Ready status and play ready sound. */
#/**********************************************/
         if (datetime.datetime.now() - self.StateTimer).seconds >= 3:
            self.StateTimer = datetime.datetime.now()
            self.EventState = self.STATE_EVENT_READY
            self.WavReady.play()
      elif self.EventState == self.STATE_EVENT_READY:
#   /**************************************************************/
#  /* Event Ready Status: After 2 seconds,                       */
# /* move to Go status and play go sound. Plus start all cycles.*/
#/**************************************************************/
         if (datetime.datetime.now() - self.StateTimer).seconds >= 2:
            self.StateTimer = datetime.datetime.now()
            self.EventState = self.STATE_EVENT_GO
            self.WavGo.play()
            for Count in range(len(self.ThisCycles)):
               self.ThisCycles[Count].Start()
      elif self.EventState == self.STATE_EVENT_GO:
#  /************************************************************/
# /* Event Go Status: After 1 second, move to Running status. */
#/************************************************************/
         if (datetime.datetime.now() - self.StateTimer).seconds >= 1:
            self.StateTimer = datetime.datetime.now()
            self.EventState = self.STATE_EVENT_RUNNING
      elif self.EventState == self.STATE_EVENT_RUNNING:
#   /******************************************************/
#  /* Event Running Status: After event, move to Finish  */
# /* status and play finish sound. Plus update records. */
#/******************************************************/
         if (self.ElapseTime.seconds > 0 and (self.ElapseTime - (self.FinishTime - self.StartTime)).days < 0) or (self.Distance > 0 and self.ThisCycles[self.ThisCyclist].GetEventDistance() >= self.Distance):
            self.EventState = self.STATE_EVENT_FINISH
            self.StateTimer = datetime.datetime.now()

            EventTime = self.FinishTime - self.StartTime
            self.ThisCycles[self.ThisCyclist].SetLastPos(self.ThisCycles[self.ThisCyclist].GetPos())
            self.ThisCycles[self.ThisCyclist].SetLastEventTime(EventTime)
            self.ThisCycles[self.ThisCyclist].SetLastEventDistance(self.ThisCycles[self.ThisCyclist].GetEventDistance())

            if self.RecordFinishTime == 0 or EventTime < self.RecordFinishTime:
               self.RecordFinishTime = EventTime
               self.RecordFinishTimeUser = self.ThisCycles[self.ThisCyclist].GetUser().GetName()
            if self.ThisCycles[self.ThisCyclist].GetEventDistance() > self.RecordFinishDistance:
               self.RecordFinishDistance = self.ThisCycles[self.ThisCyclist].GetEventDistance()
               self.RecordFinishDistanceUser = self.ThisCycles[self.ThisCyclist].GetUser().GetName()

            if self.ThisCycles[self.ThisCyclist].GetAvgSpeed() > self.ThisCycles[self.ThisCyclist].GetUser().GetPersonalBestAvgSpeed():
               self.ThisCycles[self.ThisCyclist].GetUser().SetPersonalBestAvgSpeed(self.ThisCycles[self.ThisCyclist].GetAvgSpeed())
            if self.ThisCycles[self.ThisCyclist].GetAvgSpeed() > self.GetRecordAvgSpeed():
               self.SetRecordAvgSpeed(self.ThisCycles[self.ThisCyclist].GetAvgSpeed(), self.ThisCycles[self.ThisCyclist].GetUser().GetName())

            if self.ThisCycles[self.ThisCyclist].GetAvgLapTime() < self.ThisCycles[self.ThisCyclist].GetUser().GetPersonalBestLapTime().seconds:
               self.ThisCycles[self.ThisCyclist].GetUser().SetPersonalBestLapTime(datetime.timedelta(0, self.ThisCycles[self.ThisCyclist].GetAvgLapTime()))
            if self.ThisCycles[self.ThisCyclist].GetAvgLapTime() < self.GetRecordLapTime().seconds:
               self.SetRecordLapTime(datetime.timedelta(0, self.ThisCycles[self.ThisCyclist].GetAvgLapTime()), self.ThisCycles[self.ThisCyclist].GetUser().GetName())

            self.ThisCycles[self.ThisCyclist].GetUser().SaveUserEvent(self.EventName + ".UEV")
            self.SaveRecords(self.EventName + ".REC")
            self.WavFinish.play()
      elif self.EventState == self.STATE_EVENT_FINISH:
#  /*************************************************************/
# /* Event Finish Status: After 5 seconds, move to Off status. */
#/*************************************************************/
         if (datetime.datetime.now() - self.StateTimer).seconds >= 5:
            self.StartTime = datetime.datetime.now()
            self.FinishTime = datetime.datetime.now()
            self.StateTimer = datetime.datetime.now()
            self.EventState = self.STATE_EVENT_OFF


#/*****************************************************/
#/* Return status of currently in paused mode or not. */
#/*****************************************************/
   def IsPaused(self):
      return (self.EventState == self.STATE_EVENT_PAUSED)


#/*********************************/
#/* Toggle paused mode on or off. */
#/*********************************/
   def Pause(self):
      if self.EventState == self.STATE_EVENT_PAUSED:
         self.StartTime = self.PauseStartTime + (datetime.datetime.now() - self.PauseTime)
         self.EventState = self.EventLastState
      else:
         self.PauseStartTime = self.StartTime
         self.PauseTime = datetime.datetime.now()
         self.EventLastState = self.EventState
         self.EventState = self.STATE_EVENT_PAUSED


#/*********************************/
#/* Return event elapsed seconds. */
#/*********************************/
   def GetElapsedSeconds(self):
      TimeDelta = datetime.datetime.now() - self.StartTime
      if self.EventState >= self.STATE_EVENT_FINISH:
         TimeDelta = self.FinishTime - self.StartTime
      return TimeDelta.seconds


#/******************************/
#/* Return event elapsed time. */
#/******************************/
   def GetElapsedTime(self):
      TimeDelta = datetime.datetime.now() - self.StartTime
      if self.EventState >= self.STATE_EVENT_FINISH:
         TimeDelta = self.FinishTime - self.StartTime
      return str(TimeDelta).split(".")[0]


#/********************************/
#/* Return event remaining time. */
#/********************************/
   def GetRemainingTime(self):
      TimeDelta = self.ElapseTime - (datetime.datetime.now() - self.StartTime) + datetime.timedelta(0, 1)
      if TimeDelta.days < 0:
         TimeDelta = datetime.timedelta(0)
      return str(TimeDelta).split(".")[0]


#/**************************/
#/* Get event elapse time. */
#/**************************/
   def GetElapseTime(self):
      return self.ElapseTime


#/***************************/
#/* Get event lap distance. */
#/***************************/
   def GetLapDistance(self):
      return self.LapDistance


#/***********************/
#/* Get event distance. */
#/***********************/
   def GetDistance(self):
      return self.Distance


#/************************/
#/* Get event lap count. */
#/************************/
   def GetLapCount(self):
      if self.LapCount == 0:
         return 1
      else:
         return self.LapCount


#/************************/
#/* Get record lap time. */
#/************************/
   def GetRecordLapTime(self):
      return self.RecordLapTime


#/************************/
#/* Set record lap time. */
#/************************/
   def SetRecordLapTime(self, NewRecordLapTime, NewUser):
      self.RecordLapTime = NewRecordLapTime
      self.RecordLapTimeUser = NewUser


#/*****************************/
#/* Get record average speed. */
#/*****************************/
   def GetRecordAvgSpeed(self):
      return self.RecordAvgSpeed


#/*****************************/
#/* Set record average speed. */
#/*****************************/
   def SetRecordAvgSpeed(self, NewRecordAvgSpeed, NewUser):
      self.RecordAvgSpeed = NewRecordAvgSpeed
      self.RecordAvgSpeedUser = NewUser

