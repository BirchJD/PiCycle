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
#/* User edit class. Allow user to modify data.                              */
#/****************************************************************************/


class UserEdit:
#/***************************/
#/* Define class constants. */
#/***************************/
   TYPE_ALPHA_NUMERIC = 0
   TYPE_NUMERIC = 1

   ALPHA_NUMERIC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789"
   NUMERIC = "0123456789"


   def __init__(self):
#  /****************************/
# /* Initialise value editor. */
#/****************************/
      self.EditType = self.TYPE_ALPHA_NUMERIC
      self.ChrSet = self.ALPHA_NUMERIC
      self.EditOffset = 0
      self.EditValue = ""
      self.CharacterOffset = 0


#/**********************************/
#/* Configure a new value to edit. */
#/**********************************/
   def Set(self, NewEditType, NewEditValue):
      self.EditType = NewEditType
      if self.EditType == self.TYPE_ALPHA_NUMERIC:
         self.ChrSet = self.ALPHA_NUMERIC
      elif self.EditType == self.TYPE_NUMERIC:
         self.ChrSet = self.NUMERIC

      self.EditOffset = 0
      self.EditValue = NewEditValue
      self.CharacterOffset = self.ChrSet.find(self.EditValue[self.EditOffset])


#/************************************************/
#/* Get the currently selected character offset. */
#/************************************************/
   def GetOffset(self):
      return self.EditOffset


#/*************************/
#/* Get the edited value. */
#/*************************/
   def GetValue(self):
      return self.EditValue


#/***************************************************/
#/* Scroll up for the currently selected character. */
#/***************************************************/
   def SelectUp(self):
      self.CharacterOffset += 1

      if self.CharacterOffset >= len(self.ChrSet):
         self.CharacterOffset = 0
      self.EditValue = self.EditValue[:self.EditOffset] + self.ChrSet[self.CharacterOffset] + self.EditValue[self.EditOffset + 1:]


#/*****************************************************/
#/* Scroll down for the currently selected character. */
#/*****************************************************/
   def SelectDown(self):
      self.CharacterOffset -= 1
      if self.CharacterOffset < 0:
         self.CharacterOffset = len(self.ChrSet) - 1
      self.EditValue = self.EditValue[:self.EditOffset] + self.ChrSet[self.CharacterOffset] + self.EditValue[self.EditOffset + 1:]


#/*************************************************************************/
#/* Select the character to the left of the currently selected character. */
#/*************************************************************************/
   def SelectLeft(self):
      self.EditOffset -= 1
      if self.EditOffset < 0:
         self.EditOffset = len(self.EditValue) - 1
      while self.ChrSet.find(self.EditValue[self.EditOffset]) == -1:
         self.EditOffset -= 1
         if self.EditOffset < 0:
            self.EditOffset = len(self.EditValue) - 1
      self.CharacterOffset = self.ChrSet.find(self.EditValue[self.EditOffset])


#/**************************************************************************/
#/* Select the character to the right of the currently selected character. */
#/**************************************************************************/
   def SelectRight(self):
      self.EditOffset += 1
      if self.EditOffset >= len(self.EditValue):
         self.EditOffset = 0
      while self.ChrSet.find(self.EditValue[self.EditOffset]) == -1:
         self.EditOffset += 1
         if self.EditOffset >= len(self.EditValue):
            self.EditOffset = 0
      self.CharacterOffset = self.ChrSet.find(self.EditValue[self.EditOffset])

