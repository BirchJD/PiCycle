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
#/* Cycle class.                                                             */
#/****************************************************************************/


import os
import math
import time
import random
import datetime
import pygame
import User


class Cycle:
#  /********************/
# /* Class constants. */
#/********************/
   STATUS_STOPPED = 0
   STATUS_RUNNING = 1


   def __init__(self, NewStartPos, MainUser, MainEvent):
#  /*******************************/
# /* initialise class variables. */
#/*******************************/
      self.WavLap = pygame.mixer.Sound("SOUND/lap.wav")
      self.WavLastLap = pygame.mixer.Sound("SOUND/last-lap.wav")

      self.State = self.STATUS_STOPPED

      self.ThisUser = MainUser
      self.ThisEvent = MainEvent

      self.StartPos = NewStartPos
      self.Position = self.StartPos
      self.LastPosition = self.StartPos

      self.MinSpeed = 15
      self.MaxSpeed = 20
      self.Speed = 0
      self.SpeedTimer = time.time()

      self.WheelDiameterInch = 26.0
      self.WheelDiameterCm = 66.0
      self.TotalPulseCount = 0.0
      self.TotalDistance = 0.0
      self.EventDistancePulseCount = 0.0
      self.EventDistance = 0.0
      self.EventLapDistance = 1.0
      self.LastEventDistance = 0.0

      self.EventLap = 1
      self.EventLapComplete = 0
      self.EventLapStartTime = 0
      self.EventLapTime = datetime.datetime.now()
      self.EventLastLapTime = datetime.datetime.now()
      self.LastEventTime = datetime.timedelta(0, 0)


#/********************************/
#/* Load cycle data from a file. */
#/********************************/
   def LoadCycle(self):
#  /*******************/
# /* Default values. */
#/*******************/
      self.WheelDiameterInch = 26.0
      self.WheelDiameterCm = 66.0
      self.TotalPulseCount = 0.0

      if os.path.isfile("CYCLE/CYCLE.CYC"):
         File = open("CYCLE/CYCLE.CYC", 'r', 0)
         TextLine = "."
         while TextLine != "":
            TextLine = File.readline()
            TextLine = TextLine.replace("\n", "")
            if TextLine[:20] == "WHEEL_DIAMETER_INCH=":
               self.WheelDiameterInch = float(TextLine[20:])
            elif TextLine[:18] == "WHEEL_DIAMETER_CM=":
               self.WheelDiameterCm = float(TextLine[18:])
            elif TextLine[:18] == "TOTAL_PULSE_COUNT=":
               self.TotalPulseCount = float(TextLine[18:])
         File.close()


#/******************************/
#/* Save cycle data to a file. */
#/******************************/
   def SaveCycle(self):
      File = open("CYCLE/CYCLE.CYC", 'w', 0)
      File.write("WHEEL_DIAMETER_INCH=" + str(self.WheelDiameterInch) + "\n")
      File.write("WHEEL_DIAMETER_CM=" + str(self.WheelDiameterCm) + "\n")
      File.write("TOTAL_PULSE_COUNT=" + str(self.TotalPulseCount) + "\n")
      File.close()


#/*************************************/
#/* Handle cycle sensor pulse events. */
#/*************************************/
   def Pulse(self, Period, NewSpeed):
      if self.ThisEvent.GetState() != self.ThisEvent.STATE_EVENT_PAUSED:
#  /*******************************************************/
# /* Perform computer player random cycle speed changes. */
#/*******************************************************/
         if NewSpeed != -1:
            if self.State == self.STATUS_STOPPED:
               self.Speed = 0
            elif self.State == self.STATUS_RUNNING:
               NewPeriod = Period * (((NewSpeed / 60.0 / 60.0) * self.ThisUser.GetUnitScale()) / (math.pi * self.GetWheelDiameter()))
               self.TotalPulseCount += NewPeriod
               self.EventDistancePulseCount += NewPeriod
               self.ThisUser.SetTotalPulseCount(self.ThisUser.GetTotalPulseCount() + NewPeriod)

               self.Speed = NewSpeed
         else:
#  /******************************************************************/
# /* Perform user cycle speed changes based on sensor pulse period. */
#/******************************************************************/
            self.TotalPulseCount += Period
            self.ThisUser.SetTotalPulseCount(self.ThisUser.GetTotalPulseCount() + Period)
            if self.ThisEvent.GetState() == self.ThisEvent.STATE_EVENT_READY:
               self.ThisEvent.SetState(self.ThisEvent.STATE_EVENT_FALSE_START)
            elif self.ThisEvent.GetState() == self.ThisEvent.STATE_EVENT_GO or self.ThisEvent.GetState() == self.ThisEvent.STATE_EVENT_RUNNING or self.ThisEvent.GetState() == self.ThisEvent.STATE_EVENT_OFF:
               if self.ThisEvent.GetDistance() == 0 or self.EventDistance < self.ThisEvent.GetDistance():
                  self.EventDistancePulseCount += Period

#  /******************************************/
# /* Record period between wheel rotations. */
#/******************************************/
            SpeedTimerDelta = time.time() - self.SpeedTimer

#  /**********************************************/
# /* Calcuate speed from period between pulses. */
#/**********************************************/
            if SpeedTimerDelta:
               self.Speed = math.pi * self.GetWheelDiameter() / self.ThisUser.GetUnitScale() / (SpeedTimerDelta / 60.0 / 60.0)
            else:
               self.Speed = 0
         self.SpeedTimer = time.time()


#/************************************/
#/* Called every application period. */
#/************************************/
   def Period(self, UserCycle = False):
#   /********************************************/
#  /* Calculate distance from circumference of */
# /* wheel by number of wheel rotations.      */
#/********************************************/
      self.TotalDistance = math.pi * self.GetWheelDiameter() * self.TotalPulseCount / self.ThisUser.GetUnitScale()
      self.EventDistance = math.pi * self.GetWheelDiameter() * self.EventDistancePulseCount / self.ThisUser.GetUnitScale()
      LastEventLap = self.EventLap
      self.EventLap = 1 + int(self.EventDistance / self.EventLapDistance)
      self.EventLapComplete = (self.EventDistance % self.EventLapDistance) * self.EventLapDistance

#  /**************************************************/
# /* Handle user crossing the lap line in an event. */
#/**************************************************/
      if UserCycle == True and self.ThisEvent.GetState() == self.ThisEvent.STATE_EVENT_RUNNING and LastEventLap != self.EventLap:
         if self.EventLap == self.ThisEvent.GetLapCount() + 1:
            self.WavLastLap.play()
         else:
            self.WavLap.play()
         self.EventLastLapTime = self.EventLapTime
         self.EventLapTime = datetime.datetime.now()


#/******************************************/
#/* Clear the cycle to a known idle state. */
#/******************************************/
   def Reset(self):
      self.State = self.STATUS_STOPPED
      self.EventDistancePulseCount = 0
      self.Position = self.StartPos
      self.EventLap = 1
      self.EventLapComplete = 0
      self.EventLapStartTime = 0
      self.EventLastLapTime = datetime.datetime.now()
      self.EventLapTime = datetime.datetime.now()
      self.Speed = 0
      self.SpeedTimer = time.time()


#/********************************/
#/* Start the cycle in an event. */
#/********************************/
   def Start(self):
      self.State = self.STATUS_RUNNING
      self.EventLastLapTime = datetime.datetime.now()
      self.EventLapTime = datetime.datetime.now()


#/********************************************************/
#/* Get the configured diameter of the cycle wheel.      */
#/* Required for acurate distance and speed calculation. */
#/********************************************************/
   def GetWheelDiameter(self):
      if self.ThisUser.GetUnits() == "M":
         return self.WheelDiameterInch
      else:
         return self.WheelDiameterCm


#/********************************************************/
#/* Set the configured diameter of the cycle wheel.      */
#/* Required for acurate distance and speed calculation. */
#/********************************************************/
   def SetWheelDiameter(self, NewWheelDiameter):
      if self.ThisUser.GetUnits() == "M":
         self.WheelDiameterInch = float(NewWheelDiameter)
         self.WheelDiameterCm = self.WheelDiameterInch * User.User.INCHES_TO_CM
      else:
         self.WheelDiameterCm = float(NewWheelDiameter)
         self.WheelDiameterInch = self.WheelDiameterCm / User.User.INCHES_TO_CM


#/************************************************************************/
#/* Get accumulated total distance of cycle since application first run. */
#/************************************************************************/
   def GetTotalDistance(self):
      return self.TotalDistance


#/*******************************************/
#/* Get last event total distance of cycle. */
#/*******************************************/
   def GetLastEventDistance(self):
      return self.LastEventDistance


#/*******************************************/
#/* Set last event total distance of cycle. */
#/*******************************************/
   def SetLastEventDistance(self, NewLastEventDistance):
      self.LastEventDistance = NewLastEventDistance


#/***************************************/
#/* Get last event total time of cycle. */
#/***************************************/
   def GetLastEventTime(self):
      return self.LastEventTime


#/***************************************/
#/* Set last event total time of cycle. */
#/***************************************/
   def SetLastEventTime(self, NewLastEventTime):
      self.LastEventTime = NewLastEventTime


#/****************************************/
#/* Get user associated with this cycle. */
#/****************************************/
   def GetUser(self):
      return self.ThisUser


#/**************************************************************/
#/* Get accumulated total distance of user since user created. */
#/**************************************************************/
   def GetUserDistance(self):
      return math.pi * self.GetWheelDiameter() * self.ThisUser.GetTotalPulseCount() / self.ThisUser.GetUnitScale()


#/************************************************/
#/* Get the total distance for the active event. */
#/************************************************/
   def GetEventDistance(self):
      return self.EventDistance


#/***************************************************/
#/* Get the distance for a lap of the active event. */
#/***************************************************/
   def GetEventLapDistance(self):
      return self.EventLapDistance


#/***************************************/
#/* Get the current speed of the cycle. */
#/***************************************/
   def GetSpeed(self):
#   /************************************************************************/
#  /* If a pulse has not been received by the sensor in an excessive time, */
# /* consider that the wheel of the cycle has stopped rotating.           */
#/************************************************************************/
      if time.time() - self.SpeedTimer > 2:
         self.Speed = 0
      return self.Speed


#/******************************************************/
#/* Get the average cycle speed for the current event. */
#/******************************************************/
   def GetAvgSpeed(self):
      return self.GetEventDistance() / (0.00001 + self.ThisEvent.GetElapsedSeconds() / (60.0 * 60.0))


#/***************************************************/
#/* Get the average lap time for the current event. */
#/***************************************************/
   def GetAvgLapTime(self):
      return self.ThisEvent.GetElapsedSeconds() / self.ThisEvent.GetLapCount()


#/************************************************/
#/* For computer cyclists, alter the cycle speed */
#/* within the range for the current user level. */
#/************************************************/
   def VarySpeedInRange(self):
      if self.Speed == 0:
         self.Speed = self.MinSpeed + random.randrange(self.MaxSpeed - self.MinSpeed)
      else:
         if random.randrange(50) == 0:
            self.Speed += random.randrange(100) / 100.0 - 0.5
            if self.Speed < self.MinSpeed:
               self.Speed = self.MinSpeed
            if self.Speed > self.MaxSpeed:
               self.Speed = self.MaxSpeed


#/*****************************************************/
#/* Get the current cycle position out of all cycles. */
#/*****************************************************/
   def GetPos(self):
      return self.Position


#/*****************************************************/
#/* Set the current cycle position out of all cycles. */
#/*****************************************************/
   def SetPos(self, NewPosition):
      self.Position = NewPosition


#/********************************************************/
#/* Get the last event cycle position out of all cycles. */
#/********************************************************/
   def GetLastPos(self):
      return self.LastPosition


#/********************************************************/
#/* Set the last event cycle position out of all cycles. */
#/********************************************************/
   def SetLastPos(self, NewPosition):
      self.LastPosition = NewPosition


#/*********************************************************/
#/* Set the min and max speed values for computer cycles, */
#/* based on the user level.                              */
#/*********************************************************/
   def SetSpeedRange(self, NewMinSpeed, NewMaxSpeed):
      self.MinSpeed = NewMinSpeed
      self.MaxSpeed = NewMaxSpeed
      if self.MinSpeed <= 0:
         self.MinSpeed = 0.5
      if self.MaxSpeed <= 0:
         self.MaxSpeed = 0.5


#/************************************************/
#/* Get the number of laps for the active event. */
#/************************************************/
   def GetEventLap(self):
      return self.EventLap


#/**********************************************************/
#/* Get the number of laps completed for the active event. */
#/**********************************************************/
   def GetEventLapComplete(self):
      return self.EventLapComplete


#/**************************************/
#/* Get the time into the current lap. */
#/**************************************/
   def GetLapPeriod(self):
      if self.ThisEvent.GetState() == self.ThisEvent.STATE_EVENT_GO or self.ThisEvent.GetState() == self.ThisEvent.STATE_EVENT_RUNNING or self.ThisEvent.GetState() == self.ThisEvent.STATE_EVENT_OFF:
         return datetime.datetime.now() - self.EventLapTime
      else:
         return datetime.timedelta(0)

#/*************************************/
#/* Get the time of the previous lap. */
#/*************************************/
   def GetLastLapPeriod(self):
      if self.ThisEvent.GetState() == self.ThisEvent.STATE_EVENT_RUNNING or self.ThisEvent.GetState() == self.ThisEvent.STATE_EVENT_FINISH or self.ThisEvent.GetState() == self.ThisEvent.STATE_EVENT_OFF:
         return self.EventLapTime - self.EventLastLapTime
      else:
         return datetime.timedelta(0)

