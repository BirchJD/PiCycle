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
#/* Menu class. Allow user to select menu items.                             */
#/****************************************************************************/


class Menu:
   def __init__(self, NewMenu):
#  /********************/
# /* Initialise menu. */
#/********************/
      self.ThisMenu = NewMenu
      self.Selected = 0


#/************************************/
#/* Set the text for the menu items. */
#/************************************/
   def SetMenu(self, NewMenu):
      self.ThisMenu = NewMenu


#/********************************/
#/* Return number of menu items. */
#/********************************/
   def GetSize(self):
      return len(self.ThisMenu)


#/***********************************/
#/* Return specific menu item text. */
#/***********************************/
   def GetItem(self, Item):
      return self.ThisMenu[Item]


#/*********************************/
#/* Return selected menu item ID. */
#/*********************************/
   def GetSelection(self):
      return self.Selected


#/******************************/
#/* Set selected menu item ID. */
#/******************************/
   def SetSelection(self, NewSelection):
      self.Selected = NewSelection


#/***************************************/
#/* Return the selected menu item text. */
#/***************************************/
   def GetSelectedItem(self):
      return self.ThisMenu[self.Selected]


#/*****************************************/
#/* Move the menu item selection to the   */
#/* item above the current selected item. */
#/*****************************************/
   def SelectUp(self):
      self.Selected -= 1
      if self.Selected < 0:
         self.Selected = self.GetSize() - 1


#/*****************************************/
#/* Move the menu item selection to the   */
#/* item below the current selected item. */
#/*****************************************/
   def SelectDown(self):
      self.Selected += 1
      if self.Selected >= self.GetSize():
         self.Selected = 0

