PiCycle
=======

Static exercise bicycle using a Raspberry Pi computer and this Python source
code to provide an experience to make exercise on a static bicycle more
pleasant and motivating.

Place the following line at the end of the /home/pi/.bashrc file to
automatically start the application at boot up:

/home/pi/Desktop/PiCycle/PiCycle.sh

The application can also be started manually by running the PiCycle.py script.

The file PiCycle.pdf contains the circuit diagram required. The circuit is
very basic, containing just five press switches with current limiting
resistors. Plus a reed switch, which is placed next to the rear wheel of
the bicycle, and a magnet placed on a spoke at a position which will
trigger the reed switch on each rotation. Is it best to place the reed
switch and magnet as far up a spoke, close to the tyre as possible, as this
will help prevent the possibility of erroneous triggers.


Keys
----

 ------------------------------------------------------
|CONTEXT | Menu       | Edit        | In Event         |
|--------|------------|-------------|------------------|
|UP      |Select Up   |Increment    |                  |
|DOWN    |Select Down |Decrement    |                  |
|LEFT    |            |Select Left  |Pause/Resume Event|
|RIGHT   |            |Select Right |Music On/Off      |
|ENTER   |Select Item |Commit       |Exit Event        |
 ------------------------------------------------------



TODO
----
Implement network pelaton feature across multi networked users.
User graphic overlap order when multi lapped.



Application Files
-----------------

MUSIC             - Directory containing MP3 music files which can be played
                    during exercise.

SOUND             - Application sound effects.
   brake.wav      - Sound to play before starting, count down 3.
   ready.wav      - Sound to play ready for starting, count down 2.
   go.wav         - Sound to play at start, count down 1.
   lap.wav        - Sound to play when completing each lap.
   last-lap.wav   - Sound to play when completing the penultimate lap.
   finish.wav     - Sound to play when crossing the finish line.

GRAPHIC           - Application graphic files.
   cyclist0.png   - Competitor cyclist graphic.
   cyclist1.png   - Competitor cyclist graphic.
   cyclist2.png   - Competitor cyclist graphic.
   cyclist3.png   - Competitor cyclist graphic.
   cyclist4.png   - Competitor cyclist graphic.
   cyclist5.png   - Competitor cyclist graphic.
   cyclist6.png   - Competitor cyclist graphic.
   cyclist7.png   - Competitor cyclist graphic.
   cyclist8.png   - Competitor cyclist graphic.
   tree.png       - Tree graphic.
   lap_flag.png   - Lap line flags.
   finish_flag.png - Finish line flags.

EVENTS            - Application event definitions.

CYCLE             - Application static cycle definitions.
   CYCLE.CYC      - Static bicycle properties.

USERS             - Application user definitions.

USER_EVENT        - Application user achievements per event type.

GNU-GeneralPublicLicense.txt - Open Source license.
README.TXT        - This document.
PiCycle.pdf       - Circuit diagram.
PiCycle.sh        - Application start up shell script.
PiCycle.py        - Main application initialisation and start script.
Menu.py           - Application menu class.
User.py           - Application user class.
UserEdit.py       - Application user editing class.
Cycle.py          - Application cycle class.
Event.py          - Application event class.
Display.py        - Application display class.



Class Hierarchy
---------------

            -------------                    --------------
           | Display.py  |                  | UserEdit.py  |
           | ThisDisplay |                  | ThisUserEdit |
            -------------\                  /--------------
                          \                /
                           \              /
         ----------         \------------/         -----------
        | Menu.py  | <----- | PiCycle.py | -----> | Event.py  |
        | MainMenu |         ------------         | MainEvent |
         ----------               |                -----------
             |                    V
         ----------          ------------          -----------
        | Menu.py  |        | Cycle.py   | -----> | User.py   |
        | UserMenu |        | User Cycle |         -----------
         ----------          ------------
             |                    |
         ----------          ------------          -----------
        | Menu.py  |        | Cycle.py   | -----> | User.py   |
        | TimeMenu |        | Opponent 1 |         -----------
         ----------          ------------
             |                    |
     --------------          ------------          -----------
    | Menu.py      |        | Cycle.py   | -----> | User.py   |
    | DistanceMenu |        | Opponent 2 |         -----------
     --------------          ------------
             |                    |
       ------------          ------------          -----------
      | Menu.py    |        | Cycle.py   | -----> | User.py   |
      | ConfigMenu |        | Opponent 3 |         -----------
       ------------          ------------
             |                    |
 ------------------          ------------          -----------
| Menu.py          |        | Cycle.py   | -----> | User.py   |
| PowerConfirmMenu |        | Opponent 4 |         -----------
 ------------------          ------------
             |                    |
    ---------------          ------------          -----------
   | Menu.py       |        | Cycle.py   | -----> | User.py   |
   | ExitEventMenu |        | Opponent 5 |         -----------
    ---------------          ------------
                                  |
                             ------------          -----------
                            | Cycle.py   | -----> | User.py   |
                            | Opponent 6 |         -----------
                             ------------
                                  |
                             ------------          -----------
                            | Cycle.py   | -----> | User.py   |
                            | Opponent 7 |         -----------
                             ------------
                                  |
                             ------------          -----------
                            | Cycle.py   | -----> | User.py   |
                            | Opponent 8 |         -----------
                             ------------




Application States
------------------

                        --------------------------
                       | >>>>>>>>>> END <<<<<<<<< |      ---------------------
                       | STATE_POWER_CONFIRM_MENU |     | STATE_EDIT_NET_PORT |
                        --------------------------\      ---------------------
                                                   \               |
         -----------------                          \-------------------
        | STATE_USER_MENU |                         | STATE_CONFIG_MENU |
         -----------------\                         /-------------------
         |            |    \                       /    |           |
 -----------------    |     \                     /     |   ------------------
| STATE_EDIT_NAME |   |      \                   /      |  | STATE_EDIT_WHEEL |
 -----------------    |       \-----------------/       |   ------------------
                      |       | >>>> START <<<< |       |
        ------------------    | STATE_MAIN_MENU |\   -------------------
       | STATE_EDIT_LEVEL |   /-----------------\ \ | STATE_EDIT_NET_IP |
        ------------------   /    /       |      \ \ -------------------
                            /    /        |       \ \
                           /    /         |        \ \------------------------
                          /    /          |         \                         |
        -----------------/    /    ---------------   \---------------------   |
       | STATE_TIME_MENU |    \   | STATE_RECORDS |  | STATE_DISTANCE_MENU |  |
        -----------------\     \   ---------------   /---------------------   |
                          \     \         A         /                         |
                           \     \        |        /                          |
                            \     \       |       /                           |
                             \     \      |      /                            |
                              \-----------------/                             |
                              |   STATE_EVENT   |                             |
                               -----------------                              |
                                       |                                      |
                            -----------------------                           |
                           | STATE_EXIT_EVENT_MENU |--------------------------
                            -----------------------





                        -------------
                       | STATE_EVENT |
                        -------------
                              |
                              V
                      -----------------
                     | STATE_EVENT_OFF |
                      -----------------
                              |
                              V
                     -------------------
                    | STATE_EVENT_START |
                     -------------------
                              |
                              V
                     -------------------
                    | STATE_EVENT_BRAKE |<---------------
                     -------------------                 |
                              |                          |
                              V                          |
                     -------------------     -------------------------
                    | STATE_EVENT_READY |-->| STATE_EVENT_FALSE_START |
                     -------------------     -------------------------
                              |
                              V
                     -------------------
                    |  STATE_EVENT_GO   |
                     -------------------
                              |<------------------------
                              V                         |
                    ---------------------     --------------------
                   | STATE_EVENT_RUNNING |-->| STATE_EVENT_PAUSED |
                    ---------------------     --------------------
                              |
                              V
                    --------------------
                   | STATE_EVENT_FINISH |
                    --------------------
                       |             |
                       V             V
            ---------------       -----------------------
           | STATE_RECORDS |     | STATE_EXIT_EVENT_MENU |
            ---------------       -----------------------

