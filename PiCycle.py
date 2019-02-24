#!/usr/bin/python

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
#/* Main application finite state machine.                                   */
#/****************************************************************************/


import os
import time
import random
import pygame
import RPi.GPIO
import Display
import User
import Event
import Cycle
import Menu
import UserEdit


#/**************************/
#/* Application constants. */
#/**************************/
DEBUG = False

EVENT_TIMER = pygame.USEREVENT + 1

STATE_MAIN_MENU = 0
STATE_USER_MENU = 1
STATE_TIME_MENU = 2
STATE_DISTANCE_MENU = 3
STATE_CONFIG_MENU = 4
STATE_POWER_CONFIRM_MENU = 5
STATE_EXIT_EVENT_MENU = 6
STATE_RECORDS = 7
STATE_EVENT = 8
STATE_EDIT_NAME = 9
STATE_EDIT_LEVEL = 10
STATE_EDIT_WHEEL = 11
STATE_EDIT_NET_IP = 12
STATE_EDIT_NET_PORT = 13

PERIOD = 0.05
MAX_CYCLES = 9

GPIO_PULSE_PINS = [ 10, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
GPIO_KEYPAD_PINS = [ 7, 8, 9, 11, 25 ]
KEYPAD_KEYS = [ pygame.K_RETURN, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP ]
KEYPAD_CENTER_PIN = 0
KEYPAD_RIGHT_PIN = 1
KEYPAD_DOWN_PIN = 2
KEYPAD_LEFT_PIN = 3
KEYPAD_UP_PIN = 4

MUSIC = os.listdir("MUSIC/")


#/*********************************************/
#/* Timer for development and debug purposes. */
#/*********************************************/
def Timer():
   # Simulate user on cycle for debugging.
   if AppState == STATE_EVENT and MainEvent.GetState() == MainEvent.STATE_EVENT_RUNNING:
      Cycles[0].Pulse(1, -1)



#/***************************************/
#/* Raspberry Pi GPIO interupt routine. */
#/***************************************/
def KeyPressCallback(GpioPin):
   global GPIO_PULSE_PINS
   global GPIO_KEYPAD_PINS
   global KEYPAD_CENTER_PIN
   global KEYPAD_UP_PIN
   global KEYPAD_DOWN_PIN
   global KEYPAD_LEFT_PIN
   global KEYPAD_RIGHT_PIN
   global ExitFlag
   global KeyPress
   global Cycles

#   print("GPIO: " + format(GpioPin, "00d"))

#  /***************************************/
# /* Check for cycle wheel sensor pulse. */
#/***************************************/
   Found = False
   for Count in range(len(Cycles)):
      if GpioPin == GPIO_PULSE_PINS[Count]:
         Cycles[Count].Pulse(1, -1)
         Found = True
         break

#  /******************************************************/
# /* If no wheel sensor pulse detected, flag key press. */
#/******************************************************/
   if Found == False:
      KeyPress = GpioPin


#/************************************************************/
#/* Generate application menus to reflect the current state. */
#/************************************************************/
def BuildMenus(ThisCyclist):
   global UserName
   global UserLevel
   global PlayMusic
   global Units
   global FineUnits
   global SpeedUnits
   global WheelDiameter
   global NetworkStatus
   global NetworkIP
   global NetworkPort
   global MainMenu
   global UserMenu
   global TimeMenu
   global DistanceMenu
   global ConfigMenu
   global PowerConfirmMenu
   global ExitEventMenu

   UserName = Cycles[ThisCyclist].GetUser().GetName()
   UserLevel = Cycles[ThisCyclist].GetUser().GetLevel()
   PlayMusic = Cycles[ThisCyclist].GetUser().GetPlayMusic()
   Units = Cycles[ThisCyclist].GetUser().GetUnits()
   UnitsFine = Cycles[ThisCyclist].GetUser().GetUnitsFine()
   SpeedUnits = Cycles[ThisCyclist].GetUser().GetSpeedUnits()
   WheelDiameter = Cycles[ThisCyclist].GetWheelDiameter()
   NetworkStatus = Cycles[ThisCyclist].GetUser().GetNetworkStatus()
   NetworkIP = Cycles[ThisCyclist].GetUser().GetNetworkIP()
   NetworkPort = Cycles[ThisCyclist].GetUser().GetNetworkPort()

   MainMenu.SetMenu(("USER: " + UserName + " [" + str(UserLevel) + "]", "UNRESTRICTED", "TIME RACE", "DISTANCE RACE", "CONFIGURE", "RECORDS"))
   UserMenu.SetMenu(("USER: " + UserName, "LEVEL: " + str(UserLevel), "UNITS: " + Units, "MUSIC: " + PlayMusic, "BACK"))
   TimeMenu.SetMenu(("00:01:00", "00:05:00", "00:10:00", "00:15:00", "00:30:00", "01:00:00", "02:00:00", "04:00:00", "08:00:00", "12:00:00", "BACK"))
   DistanceMenu.SetMenu(("0.5" + Units, "1" + Units, "2" + Units, "5" + Units, "10" + Units, "15" + Units, "25" + Units, "50" + Units, "75" + Units, "100" + Units, "BACK"))
   ConfigMenu.SetMenu(("WHEEL: " + str(WheelDiameter) + UnitsFine, "NETWORK: " + NetworkStatus, NetworkIP, "PORT: " + NetworkPort, "POWER OFF", "BACK"))
   PowerConfirmMenu.SetMenu(("CANCEL", "POWER OFF"))
   ExitEventMenu.SetMenu(("CANCEL", "EXIT EVENT"))


#/**************************************/
#/* Start demonstartion (atract mode). */
#/**************************************/
def StartDemoMode(ThisCyclist, Cycles):
   BuildMenus(ThisCyclist)
   MainEvent.Reset(ThisCyclist, Cycles)


#/****************************************************/
#/* Load the record summary for the current cyclist. */
#/****************************************************/
def LoadRecordSummary(ThisCyclist):
   RecordSummary = []

#  /***************************/
# /* Load last event result. */
#/***************************/
   LastPosition = Cycles[ThisCyclist].GetLastPos()
   LastEventTime = Cycles[ThisCyclist].GetLastEventTime()
   LastEventDistance = Cycles[ThisCyclist].GetLastEventDistance()
   RecordSummary.append("LAST EVENT|||")
   RecordSummary.append("|||")
   RecordSummary.append("POSITION:||" + str(LastPosition) + "|")
   RecordSummary.append("TIME:||" + str(LastEventTime).split(".")[0] + "|")
   RecordSummary.append("DISTANCE:||" + format(LastEventDistance, "1.2f") + Units + "|")
   RecordSummary.append("|||")
   RecordSummary.append("|||")

#  /****************************/
# /* Load time trial records. */
#/****************************/
   RecordSummary.append("TIME TRIALS|||")
   RecordSummary.append("|||")
   for Count in range(TimeMenu.GetSize()):
      if TimeMenu.GetItem(Count) != "BACK":
         MainEvent.LoadRecords(TimeMenu.GetItem(Count).replace(":", "") + ".REC")
         RecordSummary.append(TimeMenu.GetItem(Count) + "|" + MainEvent.RecordFinishDistanceUser + "|" + format(MainEvent.RecordFinishDistance, "1.2f") + Units + "|[" + format(MainEvent.RecordFinishDistance, "1.2f") + Units + "]")
   RecordSummary.append("|||")
   RecordSummary.append("|||")

#  /********************************/
# /* Load distance trial records. */
#/********************************/
   RecordSummary.append("DISTANCE RACES|||")
   RecordSummary.append("|||")
   for Count in range(DistanceMenu.GetSize()):
      if DistanceMenu.GetItem(Count) != "BACK":
         MainEvent.LoadRecords(DistanceMenu.GetItem(Count).replace(".", "") + ".REC")
         RecordSummary.append(DistanceMenu.GetItem(Count) + "|" + MainEvent.RecordFinishTimeUser + "|" + str(MainEvent.RecordFinishTime).split(".")[0] + "|[" + str(MainEvent.RecordFinishTime).split(".")[0] + "]")
   RecordSummary.append("|||")
   RecordSummary.append("|||")

   return RecordSummary



#  /*******************************************/
# /* Configure Raspberry Pi GPIO interfaces. */
#/*******************************************/
RPi.GPIO.setwarnings(False)
RPi.GPIO.setmode(RPi.GPIO.BCM)

for Count in range(len(GPIO_PULSE_PINS)):
   if GPIO_PULSE_PINS[Count] != 0:
      RPi.GPIO.setup(GPIO_PULSE_PINS[Count], RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
      RPi.GPIO.add_event_detect(GPIO_PULSE_PINS[Count], RPi.GPIO.FALLING, callback=KeyPressCallback, bouncetime=100)

for Count in range(len(GPIO_KEYPAD_PINS)):
   RPi.GPIO.setup(GPIO_KEYPAD_PINS[Count], RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
   RPi.GPIO.add_event_detect(GPIO_KEYPAD_PINS[Count], RPi.GPIO.FALLING, callback=KeyPressCallback, bouncetime=200)


#  /***************************/
# /* Initialise application. */
#/***************************/
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.event.set_grab(True)
ThisSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
ThisVideoInfo = pygame.display.Info()
pygame.mouse.set_visible(False)

#  /********************************************/
# /* Create a surface to use as a background. */
#/********************************************/
ThisSurface.fill((0x7F, 0x7F, 0xFF))
Background = ThisSurface.copy()

#  /*********************************************************/
# /* Generate a unique set of random numbers for this run. */
#/*********************************************************/
random.seed(time.gmtime())


#  /*************************/
# /* Application variables. */
#/*************************/
ExitFlag = False
KeyPress = 0
RecordSummary = []

ThisUserEdit = UserEdit.UserEdit()
ThisDisplay = Display.Display(ThisSurface, MAX_CYCLES)
MainEvent = Event.Event()
PulseTimer = time.time()

ThisCyclist = 0
Cycles = []
CycleSort = []
for Count in range(MAX_CYCLES):
   CycleSort.append(Count)
   Cycles.append(Cycle.Cycle(Count, User.User(Count), MainEvent))
Cycles[ThisCyclist].LoadCycle()
Cycles[ThisCyclist].GetUser().LoadUser("")
for Count in range(len(Cycles)):
   if Count != ThisCyclist:
      Cycles[Count].GetUser().SwitchUnits(Cycles[ThisCyclist].GetUser().GetUnits())

MainMenu = Menu.Menu((""))
UserMenu = Menu.Menu((""))
TimeMenu = Menu.Menu((""))
DistanceMenu = Menu.Menu((""))
ConfigMenu = Menu.Menu((""))
PowerConfirmMenu = Menu.Menu((""))
ExitEventMenu = Menu.Menu((""))
BuildMenus(ThisCyclist)


#   /**************************************************/
#  /* Main application loop, this continues  forever */
# /* or until the shutdown menu item is selected.   */
#/**************************************************/
AppState = STATE_MAIN_MENU
StartDemoMode(ThisCyclist, Cycles)

# DEBUG: Simulate a person cycling for debug and development purposes.
if DEBUG == True:
   pygame.time.set_timer(EVENT_TIMER, 300)

while ExitFlag == False:
   time.sleep(PERIOD)

#  /************************************/
# /* Process application event queue. */
#/************************************/
   for ThisEvent in pygame.event.get():
#  /******************************************************************/
# /* If ptyhon has posted a QUIT message, flag to exit applicaiton. */
#/******************************************************************/
      if ThisEvent.type == pygame.QUIT:
         ExitFlag = True
      elif ThisEvent.type == EVENT_TIMER:
         Timer()

#  /*********************************************************/
# /* On timer period perform one frame of the application. */
#/*********************************************************/
      KeysPressed = pygame.key.get_pressed()
      for Count in range(len(KEYPAD_KEYS)):
         if KeysPressed[KEYPAD_KEYS[Count]]:
            KeyPress = GPIO_KEYPAD_PINS[Count]

#/******************************/
#/* Application state machine. */
#/******************************/

#  /**********************************/
# /* State actions for - Main menu. */
#/**********************************/
   if AppState == STATE_MAIN_MENU:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            MainMenu.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            MainMenu.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            if MainMenu.GetSelectedItem()[:5] == "USER:":
               Cycles[ThisCyclist].SaveCycle()
               Cycles[ThisCyclist].GetUser().SaveUser(Cycles[ThisCyclist].GetUser().GetName() + ".USR")
               AppState = STATE_USER_MENU
            elif MainMenu.GetSelectedItem() == "UNRESTRICTED":
               MainEvent.Start("UNRESTRICTED")
               AppState = STATE_EVENT
            elif MainMenu.GetSelectedItem() == "TIME RACE":
               AppState = STATE_TIME_MENU
            elif MainMenu.GetSelectedItem() == "DISTANCE RACE":
               AppState = STATE_DISTANCE_MENU
            elif MainMenu.GetSelectedItem() == "CONFIGURE":
               AppState = STATE_CONFIG_MENU
            elif MainMenu.GetSelectedItem() == "RECORDS":
               RecordSummary = []
               AppState = STATE_RECORDS
         KeyPress = 0
#  /**********************************/
# /* State actions for - User menu. */
#/**********************************/
   elif AppState == STATE_USER_MENU:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            UserMenu.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            UserMenu.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            if UserMenu.GetSelectedItem()[:5] == "USER:":
               ThisUserEdit.Set(UserEdit.UserEdit.TYPE_ALPHA_NUMERIC, Cycles[ThisCyclist].GetUser().GetName())
               AppState = STATE_EDIT_NAME
            elif UserMenu.GetSelectedItem()[:6] == "LEVEL:":
               ThisUserEdit.Set(UserEdit.UserEdit.TYPE_NUMERIC, str(Cycles[ThisCyclist].GetUser().GetLevel()))
               AppState = STATE_EDIT_LEVEL
            elif UserMenu.GetSelectedItem()[:6] == "UNITS:":
               NewUnits = Cycles[ThisCyclist].GetUser().SwitchUnits()
               for Count in range(len(Cycles)):
                  if Count != ThisCyclist:
                     Cycles[Count].GetUser().SwitchUnits(NewUnits)
               BuildMenus(ThisCyclist)
            elif UserMenu.GetSelectedItem()[:6] == "MUSIC:":
               Cycles[ThisCyclist].GetUser().SwitchPlayMusic()
               BuildMenus(ThisCyclist)
            elif UserMenu.GetSelectedItem() == "BACK":
               AppState = STATE_MAIN_MENU
         KeyPress = 0
#  /***********************************************/
# /* State actions for - Time trial events menu. */
#/***********************************************/
   elif AppState == STATE_TIME_MENU:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            TimeMenu.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            TimeMenu.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            if TimeMenu.GetSelectedItem() == "BACK":
               AppState = STATE_MAIN_MENU
            else:
               MainEvent.Start(TimeMenu.GetSelectedItem().replace(":", ""))
               AppState = STATE_EVENT
         KeyPress = 0
#  /**************************************************/
# /* State actions for - Time distance events menu. */
#/**************************************************/
   elif AppState == STATE_DISTANCE_MENU:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            DistanceMenu.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            DistanceMenu.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            if DistanceMenu.GetSelectedItem() == "BACK":
               AppState = STATE_MAIN_MENU
            else:
               MainEvent.Start(DistanceMenu.GetSelectedItem().replace(".", ""))
               AppState = STATE_EVENT
         KeyPress = 0
#  /*******************************************************/
# /* State actions for - Application configuration menu. */
#/*******************************************************/
   elif AppState == STATE_CONFIG_MENU:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            ConfigMenu.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            ConfigMenu.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            if ConfigMenu.GetSelectedItem()[:6] == "WHEEL:":
               ThisUserEdit.Set(UserEdit.UserEdit.TYPE_NUMERIC, str(Cycles[ThisCyclist].GetWheelDiameter()))
               AppState = STATE_EDIT_WHEEL
            elif ConfigMenu.GetSelectedItem()[:8] == "NETWORK:":
               Cycles[ThisCyclist].GetUser().SwitchNetworkStatus()
               BuildMenus(ThisCyclist)
            elif ConfigMenu.GetSelectedItem() == Cycles[ThisCyclist].GetUser().GetNetworkIP():
               ThisUserEdit.Set(UserEdit.UserEdit.TYPE_NUMERIC, str(Cycles[ThisCyclist].GetUser().GetNetworkIP()))
               AppState = STATE_EDIT_NET_IP
            elif ConfigMenu.GetSelectedItem()[:5] == "PORT:":
               ThisUserEdit.Set(UserEdit.UserEdit.TYPE_NUMERIC, str(Cycles[ThisCyclist].GetUser().GetNetworkPort()))
               AppState = STATE_EDIT_NET_PORT
            elif ConfigMenu.GetSelectedItem() == "POWER OFF":
               AppState = STATE_POWER_CONFIRM_MENU
            elif ConfigMenu.GetSelectedItem() == "BACK":
               Cycles[ThisCyclist].SaveCycle()
               Cycles[ThisCyclist].GetUser().SaveUser(Cycles[ThisCyclist].GetUser().GetName() + ".USR")
               AppState = STATE_MAIN_MENU
         KeyPress = 0
#  /***************************************************/
# /* State actions for - Shutdown confirmation menu. */
#/***************************************************/
   elif AppState == STATE_POWER_CONFIRM_MENU:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            PowerConfirmMenu.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            PowerConfirmMenu.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            if PowerConfirmMenu.GetSelectedItem() == "CANCEL":
               AppState = STATE_CONFIG_MENU
            elif PowerConfirmMenu.GetSelectedItem() == "POWER OFF":
               Cycles[ThisCyclist].SaveCycle()
               Cycles[ThisCyclist].GetUser().SaveUser(Cycles[ThisCyclist].GetUser().GetName() + ".USR")
               ExitFlag = True
         KeyPress = 0
#  /*****************************************************/
# /* State actions for - Event exit confirmation menu. */
#/*****************************************************/
   elif AppState == STATE_EXIT_EVENT_MENU:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            ExitEventMenu.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            ExitEventMenu.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            if ExitEventMenu.GetSelectedItem() == "CANCEL":
               AppState = STATE_EVENT
            elif ExitEventMenu.GetSelectedItem() == "EXIT EVENT":
               StartDemoMode(ThisCyclist, Cycles)
               AppState = STATE_MAIN_MENU
         KeyPress = 0
#  /*****************************************************************/
# /* State actions for - Display event record times and distances. */
#/*****************************************************************/
   elif AppState == STATE_RECORDS:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            AppState = STATE_MAIN_MENU
         KeyPress = 0
#  /******************************************/
# /* State actions for - Active user event. */
#/******************************************/
   elif AppState == STATE_EVENT:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            pygame.mixer.music.fadeout(5000)
            ExitEventMenu.SetSelection(0)
            AppState = STATE_EXIT_EVENT_MENU
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_LEFT_PIN]:
            MainEvent.Pause()
            if MainEvent.IsPaused():
               pygame.mixer.music.pause()
            else:
               pygame.mixer.music.unpause()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_RIGHT_PIN]:
            Cycles[ThisCyclist].GetUser().SwitchPlayMusic()
            if Cycles[ThisCyclist].GetUser().GetPlayMusic() == "OFF":
               pygame.mixer.music.fadeout(1000)
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
         KeyPress = 0
      elif MainEvent.GetState() == MainEvent.STATE_EVENT_RUNNING:
         if Cycles[ThisCyclist].GetUser().GetPlayMusic() == "ON":
            if pygame.mixer.music.get_pos() == -1:
               Track = random.randrange(len(MUSIC))
               if os.path.isfile("MUSIC/" + MUSIC[Track]):
                  pygame.mixer.music.load("MUSIC/" + MUSIC[Track])
                  pygame.mixer.music.play()
      elif MainEvent.GetState() == MainEvent.STATE_EVENT_OFF:
         pygame.mixer.music.fadeout(5000)
         Cycles[ThisCyclist].SaveCycle()
         Cycles[ThisCyclist].GetUser().SaveUser(Cycles[ThisCyclist].GetUser().GetName() + ".USR")
         StartDemoMode(ThisCyclist, Cycles)
         RecordSummary = []
         AppState = STATE_RECORDS
#  /***************************************/
# /* State actions for - Edit user name. */
#/***************************************/
   elif AppState == STATE_EDIT_NAME:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            ThisUserEdit.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            ThisUserEdit.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_LEFT_PIN]:
            ThisUserEdit.SelectLeft()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_RIGHT_PIN]:
            ThisUserEdit.SelectRight()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            Cycles[ThisCyclist].GetUser().LoadUser(ThisUserEdit.GetValue() + ".USR")
            Cycles[ThisCyclist].GetUser().SetName(ThisUserEdit.GetValue())
            BuildMenus(ThisCyclist)
            AppState = STATE_USER_MENU
         KeyPress = 0
#  /****************************************/
# /* State actions for - Edit user level. */
#/****************************************/
   elif AppState == STATE_EDIT_LEVEL:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            ThisUserEdit.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            ThisUserEdit.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_LEFT_PIN]:
            ThisUserEdit.SelectLeft()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_RIGHT_PIN]:
            ThisUserEdit.SelectRight()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            Cycles[ThisCyclist].GetUser().SetLevel(ThisUserEdit.GetValue())
            BuildMenus(ThisCyclist)
            AppState = STATE_USER_MENU
         KeyPress = 0
#  /*********************************************/
# /* State actions for - Edit user wheel size. */
#/*********************************************/
   elif AppState == STATE_EDIT_WHEEL:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            ThisUserEdit.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            ThisUserEdit.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_LEFT_PIN]:
            ThisUserEdit.SelectLeft()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_RIGHT_PIN]:
            ThisUserEdit.SelectRight()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            Cycles[ThisCyclist].SetWheelDiameter(ThisUserEdit.GetValue())
            BuildMenus(ThisCyclist)
            AppState = STATE_CONFIG_MENU
         KeyPress = 0
#  /************************************************/
# /* State actions for - Edit network IP address. */
#/************************************************/
   elif AppState == STATE_EDIT_NET_IP:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            ThisUserEdit.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            ThisUserEdit.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_LEFT_PIN]:
            ThisUserEdit.SelectLeft()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_RIGHT_PIN]:
            ThisUserEdit.SelectRight()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            Cycles[ThisCyclist].GetUser().SetNetworkIP(ThisUserEdit.GetValue())
            BuildMenus(ThisCyclist)
            AppState = STATE_CONFIG_MENU
         KeyPress = 0
#  /*************************************************/
# /* State actions for - Edit network port number. */
#/*************************************************/
   elif AppState == STATE_EDIT_NET_PORT:
      if KeyPress:
         if KeyPress == GPIO_KEYPAD_PINS[KEYPAD_UP_PIN]:
            ThisUserEdit.SelectUp()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_DOWN_PIN]:
            ThisUserEdit.SelectDown()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_LEFT_PIN]:
            ThisUserEdit.SelectLeft()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_RIGHT_PIN]:
            ThisUserEdit.SelectRight()
         elif KeyPress == GPIO_KEYPAD_PINS[KEYPAD_CENTER_PIN]:
            Cycles[ThisCyclist].GetUser().SetNetworkPort(ThisUserEdit.GetValue())
            BuildMenus(ThisCyclist)
            AppState = STATE_CONFIG_MENU
         KeyPress = 0


#  /***************************/
# /* Update cycle positions. */
#/***************************/
   PulseDiff = time.time() - PulseTimer
   for Count in range(len(Cycles)):
      if Count == ThisCyclist:
         ThisDisplay.SetRoadSpeed(0.5 / 50 * Cycles[Count].GetSpeed())
      if GPIO_PULSE_PINS[Count] == 0:
         Cycles[Count].VarySpeedInRange()
         Cycles[Count].Pulse(PulseDiff, Cycles[Count].GetSpeed())
      Cycles[Count].Period((ThisCyclist == Count))
   PulseTimer = time.time()

#  /**************************/
# /* Process event actions. */
#/**************************/
   MainEvent.Period()

#  /********************/
# /* Draw background. */
#/********************/
   ThisSurface.blit(Background, (0, 0))
#  /******************/
# /* Draw graphics. */
#/******************/
   ThisDisplay.Road(ThisSurface, ThisCyclist, Cycles, MainEvent)
   ThisDisplay.Cycles(ThisSurface, MainEvent, ThisCyclist, Cycles, CycleSort)
   ThisDisplay.Header(ThisSurface, ThisCyclist, Cycles, MainEvent, (AppState == STATE_EVENT))
   if AppState == STATE_EVENT:
      ThisDisplay.Event(ThisSurface, MainEvent)
   elif AppState == STATE_MAIN_MENU:
      ThisDisplay.Menu(ThisSurface, MainMenu)
   elif AppState == STATE_USER_MENU:
      ThisDisplay.Menu(ThisSurface, UserMenu)
   elif AppState == STATE_TIME_MENU:
      ThisDisplay.Menu(ThisSurface, TimeMenu)
   elif AppState == STATE_DISTANCE_MENU:
      ThisDisplay.Menu(ThisSurface, DistanceMenu)
   elif AppState == STATE_CONFIG_MENU:
      ThisDisplay.Menu(ThisSurface, ConfigMenu)
   elif AppState == STATE_POWER_CONFIRM_MENU:
      ThisDisplay.Menu(ThisSurface, PowerConfirmMenu)
   elif AppState == STATE_EXIT_EVENT_MENU:
      ThisDisplay.Menu(ThisSurface, ExitEventMenu)
   elif AppState == STATE_RECORDS:
      if len(RecordSummary) == 0:
         RecordSummaryStartFlag = True
         RecordSummary = LoadRecordSummary(ThisCyclist)
      ThisDisplay.Records(ThisSurface, RecordSummary, RecordSummaryStartFlag)
      RecordSummaryStartFlag = False
   elif AppState == STATE_EDIT_NAME:
      ThisDisplay.Edit(ThisSurface, ThisUserEdit)
   elif AppState == STATE_EDIT_LEVEL:
      ThisDisplay.Edit(ThisSurface, ThisUserEdit)
   elif AppState == STATE_EDIT_WHEEL:
      ThisDisplay.Edit(ThisSurface, ThisUserEdit)
   elif AppState == STATE_EDIT_NET_IP:
      ThisDisplay.Edit(ThisSurface, ThisUserEdit)
   elif AppState == STATE_EDIT_NET_PORT:
      ThisDisplay.Edit(ThisSurface, ThisUserEdit)

#  /*******************/
# /* Update display. */
#/*******************/
   pygame.display.flip()


#  /*************************************************/
# /* Close Raspberry Pi GPIO use before finishing. */
#/*************************************************/
RPi.GPIO.cleanup()

pygame.time.set_timer(EVENT_TIMER, 0)
pygame.mouse.set_visible(True)

