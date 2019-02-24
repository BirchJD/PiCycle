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
#/* Display class. Handle any graphical requirements.                        */
#/****************************************************************************/


import math
import pygame
import datetime
import Menu


class Display:
#  /*************************************/
# /* Define application colour scheme. */
#/*************************************/
   ALPHA_MESSAGE = 150
   ALPHA_MENU = 150
   ALPHA_EDIT = 100
   ALPHA_RECORDS = 200

   COLOUR_TITLE_BACKGROUND = (0x5F, 0x5F, 0xFF)
   COLOUR_BRAKE = (0xFF, 0x00, 0x00)
   COLOUR_READY = (0x7F, 0x7F, 0xFF)
   COLOUR_GO = (0x00, 0xFF, 0x00)
   COLOUR_FINISH = (0x00, 0xFF, 0x00)
   COLOUR_FALSE_START = (0xFF, 0x7F, 0x7F)
   COLOUR_PAUSED = (0xFF, 0xFF, 0xFF)
   COLOUR_RECORDS = (0xFF, 0xFF, 0xFF)
   COLOUR_KEYS = (0xFF, 0xFF, 0xFF)
   COLOUR_MENU_ITEM = (0xFF, 0x00, 0x00)
   COLOUR_MENU_ITEM_BORDER = (0x00, 0x00, 0x00)
   COLOUR_MENU_BACKGROUND = (0x00, 0x00, 0x00)
   COLOUR_EDIT_BACKGROUND = (0x00, 0x00, 0x7F)
   COLOUR_EDIT_ITEM = (0xFF, 0x00, 0x00)
   COLOUR_TITLE = (0xFF, 0xFF, 0xFF)
   COLOUR_SUBTITLE = (0xCF, 0xCF, 0xFF)
   COLOUR_STANDINGS = (0x7F, 0x7F, 0x7F)
   COLOUR_STANDING = (0x7F, 0x4F, 0x4F)
   COLOUR_GRASS = (0x3F, 0x7F, 0x3F)
   COLOUR_ROAD = (0x5F, 0x5F, 0x5F)
   COLOUR_ROAD_LINE = (0xFF, 0xFF, 0xFF)
   COLOUR_SUN = (0xFF, 0xDF, 0x00)
   COLOUR_LAP_LINE = (0xFF, 0xFF, 0xFF)
   COLOUR_FINISH_LINE = (0xFF, 0x7F, 0x7F)
   COLOUR_CYCLE = (0x4F, 0x4F, 0x4F)


   def __init__(self, ThisSurface, ThisMaxCycles):
#  /*********************************************************/
# /* Scale application graphics to display size available. */
#/*********************************************************/
      self.MaxCycles = ThisMaxCycles
      self.PngCyclist = []
      for Count in range(self.MaxCycles):
         self.PngCyclist.append(pygame.image.load("GRAPHIC/cyclist" + str(Count) + ".png"))
      self.PngTree = pygame.image.load("GRAPHIC/tree.png")
      self.PngLapFlag = pygame.image.load("GRAPHIC/lap_flag.png")
      self.PngFinishFlag = pygame.image.load("GRAPHIC/finish_flag.png")
      (self.Width, self.Height) = pygame.Surface.get_size(ThisSurface)
      self.LargeFontSize = self.Height / 11
      self.LargeBorderFontSize = int(self.LargeFontSize * 1.4)
      self.SmallFontSize = self.Height / 14
      self.SmallBorderFontSize = int(self.SmallFontSize * 1.4)
      self.TinyFontSize = self.Height / 22
      self.LargeFontGap = self.LargeFontSize * 2 / 3
      self.LargeBorderFontGap = self.LargeBorderFontSize * 2 / 3
      self.SmallFontGap = self.SmallFontSize * 2 / 3
      self.SmallBorderFontGap = self.SmallBorderFontSize * 2 / 3
      self.TinyFontGap = self.TinyFontSize * 2 / 3
      self.LargeFont = pygame.font.Font(None, self.LargeFontSize)
      self.LargeMenuFont = pygame.font.Font(None, int(self.LargeBorderFontSize * 0.82))
      self.LargeBorderFont = pygame.font.Font(None, self.LargeBorderFontSize)
      self.SmallFont = pygame.font.Font(None, self.SmallFontSize)
      self.SmallBorderFont = pygame.font.Font(None, self.SmallBorderFontSize)
      self.TinyFont = pygame.font.Font(None, self.TinyFontSize)
      self.RecordSummaryPos = 0
      self.RoadSpeed = 0
      self.RoadOffset = 0


   def SetRoadSpeed(self, NewRoadSpeed):
#  /**********************************************************/
# /* Set the speed of the road animation between 0 and 0.5. */
#/**********************************************************/
      if NewRoadSpeed < 0:
         NewRoadSpeed = 0
      elif NewRoadSpeed > 0.5:
         NewRoadSpeed = 0.5
      self.RoadSpeed = NewRoadSpeed


#  /*****************************************************/
# /* Get current date and time, formatted for display. */
#/*****************************************************/
   def GetDateTime(self):
      Now = datetime.datetime.now()
      return Now.strftime("%Y-%m-%d %H:%M:%S")


#/*********************************/
#/* Display a centered text line. */
#/*********************************/
   def DiaplyCenterTextLine(self, ThisSurface, ThisTextAlpha, ThisTextColour, ThisTextBackground, ThisTextFont, ThisText):
      TempSurface = pygame.Surface((self.Width, ThisTextFont.size(ThisText)[1]))
      TempSurface.set_alpha(ThisTextAlpha)
      TempSurface.fill(ThisTextBackground)
      ThisSurface.blit(TempSurface, (0, self.Height / 2 - ThisTextFont.size(ThisText)[1] / 2))

      Text = ThisTextFont.render(ThisText, True, ThisTextColour)
      ThisSurface.blit(Text, (self.Width / 2 - ThisTextFont.size(ThisText)[0] / 2, self.Height / 2 - ThisTextFont.size(ThisText)[1] / 2))


   def Header(self, ThisSurface, ThisCyclist, Cycles, MainEvent, IsInEvent):
#  /***********/
# /* Line 1. */
#/***********/
      yPos = 0

#  /******************/
# /* Display Speed. */
#/******************/
      ThisText = format(Cycles[ThisCyclist].GetSpeed(), "1.1f") + " " + Cycles[ThisCyclist].GetUser().GetSpeedUnits()
      Text = self.LargeFont.render(ThisText, True, self.COLOUR_TITLE)
      ThisSurface.blit(Text, (self.Width / 4 - self.LargeFont.size(ThisText)[0] / 2, yPos))

#  /**********************/
# /* Display Date/Time. */
#/**********************/
      ThisText = self.GetDateTime()
      Text = self.LargeFont.render(ThisText, True, self.COLOUR_TITLE)
      ThisSurface.blit(Text, (self.Width * 3 / 4 - self.LargeFont.size(ThisText)[0] / 2, yPos))

#  /***********/
# /* Line 2. */
#/***********/
      yPos += self.LargeFontGap

#  /***************************/
# /* Display Total Distance. */
#/***************************/
      ThisText = format(Cycles[ThisCyclist].GetTotalDistance(), "1.2f") + Cycles[ThisCyclist].GetUser().GetUnits() + " TOTAL"
      Text = self.SmallFont.render(ThisText, True, self.COLOUR_TITLE)
      ThisSurface.blit(Text, (self.Width / 4 - self.SmallFont.size(ThisText)[0] / 2, yPos))

#  /**************************/
# /* Display User Distance. */
#/**************************/
      ThisText = format(Cycles[ThisCyclist].GetUserDistance(), "1.2f") + Cycles[ThisCyclist].GetUser().GetUnits() + " USER"
      Text = self.SmallFont.render(ThisText, True, self.COLOUR_TITLE)
      ThisSurface.blit(Text, (self.Width * 3 / 4 - self.SmallFont.size(ThisText)[0] / 2, yPos))

#  /***********/
# /* Line 3. */
#/***********/
      yPos += self.SmallFontGap

#  /*************************/
# /* Display Elapsed Time. */
#/*************************/
      ThisText = "ELAPSED: " + MainEvent.GetElapsedTime()
      Text = self.SmallFont.render(ThisText, True, self.COLOUR_TITLE)
      ThisSurface.blit(Text, (self.Width / 4 - self.SmallFont.size(ThisText)[0] / 2, yPos))

#  /***************************/
# /* Display Remaining Time. */
#/***************************/
      Value = MainEvent.GetRemainingTime()
      if Value != "0:00:00":
         ThisText = "REMAINING: " + Value
         Text = self.SmallFont.render(ThisText, True, self.COLOUR_TITLE)
         ThisSurface.blit(Text, (self.Width * 3 / 4 - self.SmallFont.size(ThisText)[0] / 2, yPos))

#  /***********/
# /* Line 4. */
#/***********/
      yPos += self.SmallFontGap

#  /***********************************************/
# /* Display Cyclist Position VS Computer Users. */
#/***********************************************/
      ThisText = "POS: " + format(Cycles[ThisCyclist].GetPos(), "1d") + " OF " + format(self.MaxCycles, "1d")
      Text = self.LargeFont.render(ThisText, True, self.COLOUR_SUBTITLE)
      ThisSurface.blit(Text, (self.Width / 4 - self.LargeFont.size(ThisText)[0] / 2, yPos + self.SmallFontGap / 2))

#  /**************************************/
# /* Display Current Lap Of Total Laps. */
#/**************************************/
      Value = MainEvent.GetLapCount()
      ThisText = "LAP: " + format(Cycles[ThisCyclist].GetEventLap(), "1d")
      if Value > 1:
         ThisText += " OF " + format(Value, "1d")
      Text = self.SmallFont.render(ThisText, True, self.COLOUR_SUBTITLE)
      ThisSurface.blit(Text, (self.Width * 3 / 4 - self.SmallFont.size(ThisText)[0] / 2, yPos))

#  /***********/
# /* Line 5. */
#/***********/
      yPos += self.SmallFontGap

#  /***********************************************/
# /* Display Current Distance Of Total Distance. */
#/***********************************************/
      Value = MainEvent.GetDistance()
      if Value != 0:
         ThisText = format(Cycles[ThisCyclist].GetEventDistance(), "1.2f") + Cycles[ThisCyclist].GetUser().GetUnits() + " OF " + format(Value, "1.2f") + Cycles[ThisCyclist].GetUser().GetUnits()
         Text = self.SmallFont.render(ThisText, True, self.COLOUR_TITLE)
         ThisSurface.blit(Text, (self.Width * 3 / 4 - self.SmallFont.size(ThisText)[0] / 2, yPos))

#  /***********/
# /* Line 6. */
#/***********/
      yPos += self.SmallFontGap

#  /**************************/
# /* Display Average Speed. */
#/**************************/
      ThisText = "AVG: " + format(Cycles[ThisCyclist].GetAvgSpeed(), "1.2f") + " " + Cycles[ThisCyclist].GetUser().GetSpeedUnits()
      Text = self.SmallFont.render(ThisText, True, self.COLOUR_SUBTITLE)
      ThisSurface.blit(Text, (0, yPos))

#  /****************************************/
# /* Display Personal Best Average Speed. */
#/****************************************/
      ThisText = "PB: " + format(Cycles[ThisCyclist].GetUser().GetPersonalBestAvgSpeed(), "1.2f") + " " + Cycles[ThisCyclist].GetUser().GetSpeedUnits()
      Text = self.SmallFont.render(ThisText, True, self.COLOUR_SUBTITLE)
      ThisSurface.blit(Text, (self.Width * 3 / 6 - self.SmallFont.size(ThisText)[0] / 2, yPos))

#  /*********************************/
# /* Display Record Average Speed. */
#/*********************************/
      ThisText = "REC: " + format(MainEvent.GetRecordAvgSpeed(), "1.2f") + " " + Cycles[ThisCyclist].GetUser().GetSpeedUnits()
      Text = self.SmallFont.render(ThisText, True, self.COLOUR_SUBTITLE)
      ThisSurface.blit(Text, (self.Width - self.SmallFont.size(ThisText)[0], yPos))

#  /***********/
# /* Line 7. */
#/***********/
      yPos += self.SmallFontGap

#  /*****************************/
# /* Display Current Lap Time. */
#/*****************************/
      ThisText = "LAP: " + str(Cycles[ThisCyclist].GetLapPeriod()).split(".")[0]
      Text = self.SmallFont.render(ThisText, True, self.COLOUR_SUBTITLE)
      ThisSurface.blit(Text, (0, yPos))

#  /**************************/
# /* Display Last Lap Time. */
#/**************************/
      ThisText = "LAST: " + str(Cycles[ThisCyclist].GetLastLapPeriod()).split(".")[0]
      Text = self.SmallFont.render(ThisText, True, self.COLOUR_SUBTITLE)
      ThisSurface.blit(Text, (self.Width * 3 / 8 - self.SmallFont.size(ThisText)[0] / 2, yPos))

#  /*******************************************/
# /* Display Personal Best Average Lap Time. */
#/*******************************************/
      ThisText = "PB: " + str(Cycles[ThisCyclist].GetUser().GetPersonalBestLapTime()).split(".")[0]
      Text = self.SmallFont.render(ThisText, True, self.COLOUR_SUBTITLE)
      ThisSurface.blit(Text, (self.Width * 5 / 8 - self.SmallFont.size(ThisText)[0] / 2, yPos))

#  /************************************/
# /* Display Record Average Lap Time. */
#/************************************/
      ThisText = "REC: " + str(MainEvent.GetRecordLapTime()).split(".")[0]
      Text = self.SmallFont.render(ThisText, True, self.COLOUR_SUBTITLE)
      ThisSurface.blit(Text, (self.Width - self.SmallFont.size(ThisText)[0], yPos))

#  /**************************************/
# /* During event, display key summary. */
#/**************************************/
      if MainEvent.GetState() == MainEvent.STATE_EVENT_PAUSED or (IsInEvent == True and MainEvent.GetState() == MainEvent.STATE_EVENT_RUNNING):
         yPos = (self.Height / 3) + self.TinyFontGap * 2

         ThisText = "ENTER - EXIT EVENT"
         Text = self.TinyFont.render(ThisText, True, self.COLOUR_KEYS)
         xPos = self.Width - self.TinyFont.size(ThisText)[0]

         TempSurface = pygame.Surface((self.TinyFont.size(ThisText)[0] + self.TinyFontGap / 2, 4 * self.TinyFontGap))
         TempSurface.set_alpha(self.ALPHA_RECORDS)
         TempSurface.fill(self.COLOUR_MENU_BACKGROUND)
         ThisSurface.blit(TempSurface, (self.Width - self.TinyFont.size(ThisText)[0] - self.TinyFontGap / 2, yPos - self.TinyFontGap / 2))

         ThisSurface.blit(Text, (xPos, yPos))

         yPos += self.TinyFontGap

         ThisText = "<- PAUSE/RESUME"
         Text = self.TinyFont.render(ThisText, True, self.COLOUR_KEYS)
         ThisSurface.blit(Text, (xPos, yPos))

         yPos += self.TinyFontGap

         ThisText = "-> MUSIC ON/OFF"
         Text = self.TinyFont.render(ThisText, True, self.COLOUR_KEYS)
         ThisSurface.blit(Text, (xPos, yPos))


   def Road(self, ThisSurface, ThisCyclist, Cycles, ThisEvent):
#  /************************************/
# /* Draw information HUD background. */
#/************************************/
      pygame.draw.rect(ThisSurface, self.COLOUR_TITLE_BACKGROUND, (0, 0, self.Width, self.Height / 80 + 1 * self.LargeFontGap + 6 * self.SmallFontGap), 0)

#  /*************/
# /* Draw sun. */
#/*************/
      Radius = self.Height * 4 / 20
      pygame.draw.circle(ThisSurface, self.COLOUR_SUN, (self.Width - Radius * 9 / 10, self.Height * 15 / 20), Radius, 0)

#  /***************/
# /* Draw grass. */
#/***************/
      pygame.draw.rect(ThisSurface, self.COLOUR_GRASS, (0, self.Height * 2 / 3, self.Width, self.Height / 3), 0)

#  /**************/
# /* Draw road. */
#/**************/
      pygame.draw.polygon(ThisSurface, self.COLOUR_ROAD, ((self.Width * 11 / 24, self.Height * 2 / 3), (self.Width * 13 / 24, self.Height * 2 / 3), (self.Width, self.Height), (0, self.Height)), 0)

#  /****************************/
# /* Draw white line on road. */
#/****************************/
      pygame.draw.polygon(ThisSurface, self.COLOUR_ROAD_LINE, ((self.Width * 50 / 100, (self.Height * 2 / 3) + 5), (self.Width * 50 / 100, (self.Height * 2 / 3) + 5), (self.Width * 48 / 100, self.Height), (self.Width * 52 / 100, self.Height)), 0)

#  /*********************************************/
# /* Draw gaps in white line with perspective. */
#/*********************************************/
      for Count in range(1, 10):
         yPos = self.Height - (self.Height / 3 * math.log(10.0001 - (Count + self.RoadOffset), 11))
         if self.Height * 2 / 3 < yPos:
            LineGap = (50 * math.log(0.0001 + ((yPos - (self.Height * 2 / 3)) / (self.Height / 3) * 10), 100))
            pygame.draw.rect(ThisSurface, self.COLOUR_ROAD, (self.Width * 48 / 100, yPos, self.Width * 4 / 100, LineGap), 0)

#  /****************************/
# /* Move gaps in white line. */
#/****************************/
      self.RoadOffset += self.RoadSpeed
      if self.RoadOffset > 1:
         self.RoadOffset = 0.1

#  /******************/
# /* Draw lap line. */
#/******************/
      Proximity = 1.0 - Cycles[ThisCyclist].GetEventDistance() % ThisEvent.GetLapDistance()
      if Proximity > 0 and Proximity < 0.5:
         ProximityLog = math.log(0.0001 + (Proximity * 20000), 12000)
#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
         xPos = (self.Width * 11 / 24) * ProximityLog
         Distance = self.Height - (self.Height / 3) * ProximityLog
         Width = self.Width - (self.Width * 22 / 24) * ProximityLog
         Height = (self.Height / 20) - (self.Height / 20) * ProximityLog
         Aspect = (self.Width / 15) * (1 - ProximityLog)

         pygame.draw.polygon(ThisSurface, self.COLOUR_LAP_LINE, ((xPos, Distance), (xPos + Width, Distance), (xPos + Width + Aspect, Distance + Height), (xPos - Aspect, Distance + Height)), 0)

#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
         xPos =  (self.Width * 11 / 64) - (self.Width / 2) + (self.Width * 101 / 128) * ProximityLog
         Distance = (self.Height * 75 / 100) - (self.Height * 22 / 256) * ProximityLog
         Width = int((self.Width / 3) - (self.Width / 3) * ProximityLog)
         Height = int((self.Height / 4) - (self.Height / 4) * ProximityLog)
#  /******************/
# /* Draw lap flag. */
#/******************/
         ScaledPng = pygame.transform.scale(self.PngLapFlag, (Width, Height))
         ThisSurface.blit(ScaledPng, (xPos, Distance))
#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
         xPos =  (self.Width * 79 / 160) + (self.Width / 2) - (self.Width * 58 / 128) * ProximityLog
         Distance = (self.Height * 75 / 100) - (self.Height * 22 / 256) * ProximityLog
         Width = int((self.Width / 3) - (self.Width / 3) * ProximityLog)
         Height = int((self.Height / 4) - (self.Height / 4) * ProximityLog)
#  /******************/
# /* Draw lap flag. */
#/******************/
         ScaledPng = pygame.transform.scale(self.PngLapFlag, (Width, Height))
         ThisSurface.blit(ScaledPng, (xPos, Distance))

#  /*********************/
# /* Draw finish line. */
#/*********************/
      if ThisEvent.GetDistance() > 0 and Cycles[ThisCyclist].GetEventLap() == ThisEvent.GetLapCount():
         Proximity = ThisEvent.GetLapDistance() - (Cycles[ThisCyclist].GetEventDistance() - (ThisEvent.GetLapDistance() * (ThisEvent.GetLapCount() - 1))) % ThisEvent.GetLapDistance()
         if Proximity > 0 and Proximity < 0.5:
            ProximityLog = math.log(0.0001 + (Proximity * 20000), 12000)
#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
            xPos = (self.Width * 11 / 24) * ProximityLog
            Distance = self.Height - (self.Height / 3) * ProximityLog
            Width = self.Width - (self.Width * 22 / 24) * ProximityLog
            Height = (self.Height / 20) - (self.Height / 20) * ProximityLog
            Aspect = (self.Width / 15) * (1 - ProximityLog)

            pygame.draw.polygon(ThisSurface, self.COLOUR_FINISH_LINE, ((xPos, Distance), (xPos + Width, Distance), (xPos + Width + Aspect, Distance + Height), (xPos - Aspect, Distance + Height)), 0)

#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
            xPos =  (self.Width * 11 / 64) - (self.Width / 2) + (self.Width * 101 / 128) * ProximityLog
            Distance = (self.Height * 75 / 100) - (self.Height * 22 / 256) * ProximityLog
            Width = int((self.Width / 3) - (self.Width / 3) * ProximityLog)
            Height = int((self.Height / 4) - (self.Height / 4) * ProximityLog)
#  /******************/
# /* Draw lap flag. */
#/******************/
            ScaledPng = pygame.transform.scale(self.PngFinishFlag, (Width, Height))
            ThisSurface.blit(ScaledPng, (xPos, Distance))
#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
            xPos =  (self.Width * 79 / 160) + (self.Width / 2) - (self.Width * 58 / 128) * ProximityLog
            Distance = (self.Height * 75 / 100) - (self.Height * 22 / 256) * ProximityLog
            Width = int((self.Width / 3) - (self.Width / 3) * ProximityLog)
            Height = int((self.Height / 4) - (self.Height / 4) * ProximityLog)
#  /******************/
# /* Draw lap flag. */
#/******************/
            ScaledPng = pygame.transform.scale(self.PngFinishFlag, (Width, Height))
            ThisSurface.blit(ScaledPng, (xPos, Distance))

#  /*******************/
# /* Draw left tree. */
#/*******************/
      Proximity = (0.25 - Cycles[ThisCyclist].GetEventDistance()) % ThisEvent.GetLapDistance()
      if Proximity > 0 and Proximity < 0.5:
         ProximityLog = math.log(0.0001 + (Proximity * 20000), 12000)
#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
         xPos =  (self.Width * 11 / 64) - (self.Width / 2) + (self.Width * 101 / 128) * ProximityLog
         Distance = (self.Height * 426 / 256) * ProximityLog - self.Height
         Width = int((self.Width / 3) - (self.Width / 3) * ProximityLog)
         Height = int((self.Height * 2) - (self.Height * 2) * ProximityLog)
#  /**************/
# /* Draw tree. */
#/**************/
         ScaledPng = pygame.transform.scale(self.PngTree, (Width, Height))
         ThisSurface.blit(ScaledPng, (xPos, Distance))

#  /********************/
# /* Draw right tree. */
#/********************/
      Proximity = (0.33 - Cycles[ThisCyclist].GetEventDistance()) % ThisEvent.GetLapDistance()
      if Proximity > 0 and Proximity < 0.5:
         ProximityLog = math.log(0.0001 + (Proximity * 20000), 12000)
#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
         xPos =  (self.Width * 79 / 160) + (self.Width / 2) - (self.Width * 58 / 128) * ProximityLog
         Distance = (self.Height * 426 / 256) * ProximityLog - self.Height
         Width = int((self.Width / 3) - (self.Width / 3) * ProximityLog)
         Height = int((self.Height * 2) - (self.Height * 2) * ProximityLog)
#  /**************/
# /* Draw tree. */
#/**************/
         ScaledPng = pygame.transform.scale(self.PngTree, (Width, Height))
         ThisSurface.blit(ScaledPng, (xPos, Distance))

#  /*******************/
# /* Draw left tree. */
#/*******************/
      Proximity = (0.45 - Cycles[ThisCyclist].GetEventDistance()) % ThisEvent.GetLapDistance()
      if Proximity > 0 and Proximity < 0.5:
         ProximityLog = math.log(0.0001 + (Proximity * 20000), 12000)
#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
         xPos =  (self.Width * 11 / 64) - (self.Width / 2) + (self.Width * 101 / 128) * ProximityLog
         Distance = (self.Height * 426 / 256) * ProximityLog - self.Height
         Width = int((self.Width / 3) - (self.Width / 3) * ProximityLog)
         Height = int((self.Height * 2) - (self.Height * 2) * ProximityLog)
#  /**************/
# /* Draw tree. */
#/**************/
         ScaledPng = pygame.transform.scale(self.PngTree, (Width, Height))
         ThisSurface.blit(ScaledPng, (xPos, Distance))

#  /********************/
# /* Draw right tree. */
#/********************/
      Proximity = (0.55 - Cycles[ThisCyclist].GetEventDistance()) % ThisEvent.GetLapDistance()
      if Proximity > 0 and Proximity < 0.5:
         ProximityLog = math.log(0.0001 + (Proximity * 20000), 12000)
#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
         xPos =  (self.Width * 79 / 160) + (self.Width / 2) - (self.Width * 58 / 128) * ProximityLog
         Distance = (self.Height * 426 / 256) * ProximityLog - self.Height
         Width = int((self.Width / 3) - (self.Width / 3) * ProximityLog)
         Height = int((self.Height * 2) - (self.Height * 2) * ProximityLog)
#  /**************/
# /* Draw tree. */
#/**************/
         ScaledPng = pygame.transform.scale(self.PngTree, (Width, Height))
         ThisSurface.blit(ScaledPng, (xPos, Distance))

#  /*******************/
# /* Draw left tree. */
#/*******************/
      Proximity = (0.66 - Cycles[ThisCyclist].GetEventDistance()) % ThisEvent.GetLapDistance()
      if Proximity > 0 and Proximity < 0.5:
         ProximityLog = math.log(0.0001 + (Proximity * 20000), 12000)
#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
         xPos =  (self.Width * 11 / 64) - (self.Width / 2) + (self.Width * 101 / 128) * ProximityLog
         Distance = (self.Height * 426 / 256) * ProximityLog - self.Height
         Width = int((self.Width / 3) - (self.Width / 3) * ProximityLog)
         Height = int((self.Height * 2) - (self.Height * 2) * ProximityLog)
#  /**************/
# /* Draw tree. */
#/**************/
         ScaledPng = pygame.transform.scale(self.PngTree, (Width, Height))
         ThisSurface.blit(ScaledPng, (xPos, Distance))

#  /********************/
# /* Draw right tree. */
#/********************/
      Proximity = (0.75 - Cycles[ThisCyclist].GetEventDistance()) % ThisEvent.GetLapDistance()
      if Proximity > 0 and Proximity < 0.5:
         ProximityLog = math.log(0.0001 + (Proximity * 20000), 12000)
#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
         xPos =  (self.Width * 79 / 160) + (self.Width / 2) - (self.Width * 58 / 128) * ProximityLog
         Distance = (self.Height * 426 / 256) * ProximityLog - self.Height
         Width = int((self.Width / 3) - (self.Width / 3) * ProximityLog)
         Height = int((self.Height * 2) - (self.Height * 2) * ProximityLog)
#  /**************/
# /* Draw tree. */
#/**************/
         ScaledPng = pygame.transform.scale(self.PngTree, (Width, Height))
         ThisSurface.blit(ScaledPng, (xPos, Distance))


   def Cycles(self, ThisSurface, ThisEvent, ThisCyclist, Cycles, CycleSort):
#  /**************************************************/
# /* Display all cyclests, except the first person. */
#/**************************************************/
      yPos = self.Height / 3 + self.TinyFontGap / 2

      TempSurface = pygame.Surface((self.Width * 7 / 20, (self.MaxCycles + 1) * self.TinyFontGap))
      TempSurface.set_alpha(self.ALPHA_RECORDS)
      TempSurface.fill(self.COLOUR_MENU_BACKGROUND)
      ThisSurface.blit(TempSurface, (0, yPos + self.TinyFontGap / 2))

      for ThisCycle in range(self.MaxCycles):
         Cycles[CycleSort[ThisCycle]].SetPos(ThisCycle + 1)

#  /*********************************************/
# /* Sort the position standngs of the cycles. */
#/*********************************************/
         if ThisCycle < self.MaxCycles - 1 and Cycles[CycleSort[ThisCycle]].GetEventDistance() < Cycles[CycleSort[ThisCycle + 1]].GetEventDistance():
            Temp = CycleSort[ThisCycle + 1]
            CycleSort[ThisCycle + 1] = CycleSort[ThisCycle]
            CycleSort[ThisCycle] = Temp

#  /************************************************/
# /* Display the position standngs of the cycles. */
#/************************************************/
         yPos += self.TinyFontGap

         LapProximity = Cycles[CycleSort[ThisCycle]].GetEventLapComplete() - Cycles[ThisCyclist].GetEventLapComplete()
         if LapProximity >= Cycles[CycleSort[ThisCycle]].GetEventLapDistance() / 2:
            LapProximity -= Cycles[CycleSort[ThisCycle]].GetEventLapDistance()
         elif LapProximity <= -Cycles[CycleSort[ThisCycle]].GetEventLapDistance() / 2:
            LapProximity += Cycles[CycleSort[ThisCycle]].GetEventLapDistance()
         ThisText = Cycles[CycleSort[ThisCycle]].GetUser().GetName() + " " + format(Cycles[CycleSort[ThisCycle]].GetSpeed(), "1.1f") + Cycles[CycleSort[ThisCycle]].GetUser().GetSpeedUnits() + " " + format(Cycles[CycleSort[ThisCycle]].GetEventDistance(), "1.2f") + Cycles[CycleSort[ThisCycle]].GetUser().GetUnits() + " [" + format(Cycles[CycleSort[ThisCycle]].GetEventLap(), "1d") + "] " + format(LapProximity, "1.2f")
         if CycleSort[ThisCycle] == ThisCyclist:
            Text = self.TinyFont.render(ThisText, True, self.COLOUR_STANDING)
         else:
            Text = self.TinyFont.render(ThisText, True, self.COLOUR_STANDINGS)
         ThisSurface.blit(Text, (0, yPos))

         if CycleSort[ThisCycle] != ThisCyclist:
#  /*********************************************************/
# /* Only display the cyclest if within viewable distance. */
#/*********************************************************/
            LapDistance = Cycles[CycleSort[ThisCycle]].GetEventDistance() - Cycles[ThisCyclist].GetEventDistance()
            Proximity = LapDistance % ThisEvent.GetLapDistance()
            if Proximity > 0 and Proximity < 0.5:
               ProximityLog = math.log(0.0001 + (Proximity * 20000), 12000)
#  /***************************/
# /* Calculate aspect ratio. */
#/***************************/
               xPos = (CycleSort[ThisCycle] * self.Width / self.MaxCycles) + ((self.Width / 2) - (CycleSort[ThisCycle] * self.Width / self.MaxCycles)) * math.log(0.0001 + (Proximity * 8000), 12000)
               Distance = (self.Height * 51 / 80) + (self.Height / 9) * math.log(0.0001 + (Proximity * 30), 40000)
               Width = int((self.Width / self.MaxCycles) - (self.Width / self.MaxCycles) * ProximityLog)
               Height = int((self.Height / 2) - (self.Height / 2) * ProximityLog)
#  /*****************/
# /* Draw cyclest. */
#/*****************/
               ScaledPng = pygame.transform.scale(self.PngCyclist[CycleSort[ThisCycle]], (Width, Height))
               ThisSurface.blit(ScaledPng, (xPos, Distance))


   def Event(self, ThisSurface, MainEvent):
      ThisState = MainEvent.GetState()
      if ThisState == MainEvent.STATE_EVENT_BRAKE:
#  /**********************************************************/
# /* Display BRAKE on top of a semi-transparant background. */
#/**********************************************************/
         self.DiaplyCenterTextLine(ThisSurface, self.ALPHA_MESSAGE, self.COLOUR_BRAKE, self.COLOUR_MENU_BACKGROUND, self.LargeFont, "BRAKE")
      elif ThisState == MainEvent.STATE_EVENT_READY:
#  /**********************************************************/
# /* Display READY on top of a semi-transparant background. */
#/**********************************************************/
         self.DiaplyCenterTextLine(ThisSurface, self.ALPHA_MESSAGE, self.COLOUR_READY, self.COLOUR_MENU_BACKGROUND, self.LargeFont, "READY")
      elif ThisState == MainEvent.STATE_EVENT_GO:
#  /*******************************************************/
# /* Display GO on top of a semi-transparant background. */
#/*******************************************************/
         self.DiaplyCenterTextLine(ThisSurface, self.ALPHA_MESSAGE, self.COLOUR_GO, self.COLOUR_MENU_BACKGROUND, self.LargeFont, "GO")
      elif ThisState == MainEvent.STATE_EVENT_FINISH:
#  /***********************************************************/
# /* Display FINISH on top of a semi-transparant background. */
#/***********************************************************/
         self.DiaplyCenterTextLine(ThisSurface, self.ALPHA_MESSAGE, self.COLOUR_FINISH, self.COLOUR_MENU_BACKGROUND, self.LargeFont, "FINISH")
      elif ThisState == MainEvent.STATE_EVENT_FALSE_START:
#  /****************************************************************/
# /* Display FALSE START on top of a semi-transparant background. */
#/****************************************************************/
         self.DiaplyCenterTextLine(ThisSurface, self.ALPHA_MESSAGE, self.COLOUR_FALSE_START, self.COLOUR_MENU_BACKGROUND, self.LargeFont, "FALSE START")
      elif ThisState == MainEvent.STATE_EVENT_PAUSED:
#  /***********************************************************/
# /* Display PAUSED on top of a semi-transparant background. */
#/***********************************************************/
         self.DiaplyCenterTextLine(ThisSurface, self.ALPHA_MESSAGE, self.COLOUR_PAUSED, self.COLOUR_MENU_BACKGROUND, self.LargeFont, "PAUSED")


   def Records(self, ThisSurface, RecordSumary, StartFlag):
#  /*****************************************************************/
# /* Display records text on top of a semi-transparant background. */
#/*****************************************************************/
      TempSurface = pygame.Surface((self.Width * 18 / 24, self.Height))
      TempSurface.set_alpha(self.ALPHA_RECORDS)
      TempSurface.fill(self.COLOUR_MENU_BACKGROUND)
      ThisSurface.blit(TempSurface, (self.Width * 3 / 24, 0))

#  /*************************************/
# /* Intially start at top of display. */
#/*************************************/
      if StartFlag == True:
         self.RecordSummaryPos = 0
      elif self.RecordSummaryPos / self.SmallFontGap >= 2 * len(RecordSumary):
#  /**************************************************************/
# /* When fully scrolled wrap back to effect a continus scroll. */
#/**************************************************************/
         self.RecordSummaryPos -= (len(RecordSumary) * self.SmallFontGap)

#  /****************************************/
# /* Scroll records display one position. */
#/****************************************/
      self.RecordSummaryPos += (self.SmallFontGap / 8)

#  /*********************************/
# /* Display lines of record text. */
#/*********************************/
      ItemCount = 0
      yPos = self.Height - self.RecordSummaryPos
      for Count in range(2 * len(RecordSumary)):
         if yPos > -self.SmallFontGap and yPos < self.Height + self.SmallFontGap:
#  /*********************/
# /* Display column 1. */
#/*********************/
            ThisText = RecordSumary[ItemCount].split("|")
            Text = self.SmallFont.render(ThisText[0], True, self.COLOUR_RECORDS)
            ThisSurface.blit(Text, (self.SmallFontGap + self.Width * 3 / 24, yPos))

#  /*********************/
# /* Display column 2. */
#/*********************/
            ThisText = RecordSumary[ItemCount].split("|")
            Text = self.SmallFont.render(ThisText[1], True, self.COLOUR_RECORDS)
            ThisSurface.blit(Text, (self.SmallFontGap + self.Width * 7 / 24, yPos))

#  /*********************/
# /* Display column 3. */
#/*********************/
            ThisText = RecordSumary[ItemCount].split("|")
            Text = self.SmallFont.render(ThisText[2], True, self.COLOUR_RECORDS)
            ThisSurface.blit(Text, (self.SmallFontGap + self.Width * 11 / 24, yPos))

#  /*********************/
# /* Display column 4. */
#/*********************/
            ThisText = RecordSumary[ItemCount].split("|")
            Text = self.SmallFont.render(ThisText[3], True, self.COLOUR_RECORDS)
            ThisSurface.blit(Text, (self.SmallFontGap + self.Width * 15 / 24, yPos))

#  /************************************/
# /* Wrap back to first line of text. */
#/************************************/
         ItemCount += 1
         if ItemCount >= len(RecordSumary):
            ItemCount = 0

#  /*********************************/
# /* Move to next line of display. */
#/*********************************/
         yPos += self.SmallFontGap


#/*******************/
#/* Display a menu. */
#/*******************/
   def Menu(self, ThisSurface, ThisMenu):
#  /*************************************************************/
# /* Display the menu on top of a semi-transparant background. */
#/*************************************************************/
      TempSurface = pygame.Surface((self.Width * 3 / 5, self.Height))
      TempSurface.set_alpha(self.ALPHA_MENU)
      TempSurface.fill(self.COLOUR_MENU_BACKGROUND)
      ThisSurface.blit(TempSurface, (self.Width * 1 / 5, 0))

#  /**********************************/
# /* Display each line of the menu. */
#/**********************************/
      yPos = (self.Height - self.LargeBorderFontGap * ThisMenu.GetSize()) / 2
      for Count in range(ThisMenu.GetSize()):
#  /************************************************************************/
# /* Highlight the selected menu item with a semi-transparent background. */
#/************************************************************************/
         if Count == ThisMenu.GetSelection():
            TempSurface = pygame.Surface((self.Width * 3 / 5, self.LargeBorderFontGap))
            TempSurface.set_alpha(self.ALPHA_MENU)
            TempSurface.fill(self.COLOUR_MENU_BACKGROUND)
            ThisSurface.blit(TempSurface, (self.Width * 1 / 5, yPos))

#  /***********************************************************/
# /* Dispaply a background for each letter of the menu item. */
#/***********************************************************/
         xSize = self.LargeBorderFont.size(ThisMenu.GetItem(Count))[0]
         xPos = self.Width / 2 - xSize / 2
         for LetterCount in range(len(ThisMenu.GetItem(Count))):
            Text = self.LargeBorderFont.render(ThisMenu.GetItem(Count)[LetterCount], True, self.COLOUR_MENU_ITEM_BORDER)
            ThisSurface.blit(Text, (xPos, yPos))
            xPos += self.LargeBorderFont.size(ThisMenu.GetItem(Count)[LetterCount])[0]

#  /**************************************************************************/
# /* Dispaply each letter of the menu item on top of the letter background. */
#/**************************************************************************/
         xPos = self.Width / 2 - xSize / 2 + self.LargeBorderFontGap / 1.4 * 0.1
         for LetterCount in range(len(ThisMenu.GetItem(Count))):
            Text = self.LargeMenuFont.render(ThisMenu.GetItem(Count)[LetterCount], True, self.COLOUR_MENU_ITEM)
            ThisSurface.blit(Text, (xPos, yPos + self.LargeBorderFontGap * 0.1))
            xPos += self.LargeBorderFont.size(ThisMenu.GetItem(Count)[LetterCount])[0]

#  /**********************/
# /* Move to next line. */
#/**********************/
         yPos += self.LargeBorderFontGap


#/*******************************/
#/* Display text while editing. */
#/*******************************/
   def Edit(self, ThisSurface, ThisUserEdit):
      xSize = len(ThisUserEdit.GetValue()) * self.LargeFontGap / 1.4
      xPos = self.Width / 2 - xSize / 2
      yPos = self.Height * 2 / 5

#  /*******************************************************************/
# /* Display the edit value on top of a semi-transparant background. */
#/*******************************************************************/
      TempSurface = pygame.Surface((self.Width, self.LargeFontGap * 1.4))
      TempSurface.set_alpha(self.ALPHA_EDIT)
      TempSurface.fill(self.COLOUR_EDIT_BACKGROUND)
      ThisSurface.blit(TempSurface, (0, yPos))

#  /**************************************************************************/
# /* Dispaply each letter of the menu item on top of the letter background. */
#/**************************************************************************/
      for LetterCount in range(len(ThisUserEdit.GetValue())):
#  /*****************************************/
# /* Highlight the character being edited. */
#/*****************************************/
         if ThisUserEdit.GetOffset() == LetterCount:
            TempSurface = pygame.Surface((self.LargeFontGap / 1.4, self.LargeFontGap * 1.4))
            TempSurface.set_alpha(self.ALPHA_EDIT)
            TempSurface.fill(self.COLOUR_EDIT_BACKGROUND)
            ThisSurface.blit(TempSurface, (xPos + self.LargeFontGap / 1.4 - self.LargeFont.size(ThisUserEdit.GetValue()[LetterCount])[0] / 2, yPos))

#  /*******************************/
# /* Display the next character. */
#/*******************************/
         Text = self.LargeMenuFont.render(ThisUserEdit.GetValue()[LetterCount], True, self.COLOUR_EDIT_ITEM)
         ThisSurface.blit(Text, (xPos + self.LargeFontGap / 1.4 - self.LargeFont.size(ThisUserEdit.GetValue()[LetterCount])[0] / 2, yPos))
         xPos += self.LargeFontGap / 1.4

