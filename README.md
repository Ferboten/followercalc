A World of Warcraft Garrison Follower Calculator

This calculator will read in a list of missions and followers, and output the  
teams for every mission with the highest chance of success. It also solves the  
optimization problem of finding the minimum number of followers required to  
achieve the highest chance of success on every mission specified. This allows  
the user to prioritize which followers to upgrade first, as well as freeing up  
roster space for other followers.

It is possible to achieve a 100% success chance on a mission without countering  
all of its threats, provided that your followers have beneficial traits.

This represents a very early version of the calculator and is a little  
"rougher" to use than is envisioned. There is a possibility of this being  
converted into a WoW addon if there is enough support.

How to use:  
After entering in mission and follower data in the appropriate files, simply  
run the followers.py file using Python 2.7 from the command line, or your  
favorite IDE.

The missions file (default is missions.txt):  
This file specifies the missions you wish to optimize for. Each line specifies  
one mission, and the mission parameters are separated by commas. The parameters  
and their order are as follows:

Name - Used to identify the mission for readability.  
Level - Between 90 and 100.  
Item level - Use 0 if the mission has no item level.  
Environment - The Mission Type (Plains, Ogre, etc) as specified in the mission  
    panel.  
Length - The mission length in hours (without Epic Mount).  
Base Success - The success chance of the mission without any followers (some  
    have 0%, some have 50%, 100%, etc.)  
Slots - The number of followers that the mission requires.  
Mechanics - The threats that the mission presents to be countered. These must  
    be spelled and capitalized exactly, and are each separated by a semi-colon  
    (;) and not by a comma.
    
The followers file (default is followers.txt):  
This file specifies every follower (including the inactive ones) in your  
garrison. Each line specifies one follower, with the follower parameters  
separated by commas. The parameters and their order are as follows:  

Name - The name of the follower  
Race - The race of the follower  
Level - The level of the follower (I suggest simply setting this to 100 in  
    order to determine whether a low level follower will be useful).  
Item Level - The item level of the follower (As above, I suggest setting this  
    to 655 or higher in order to determine if the follower will be useful).  
Counters - The threats that this follower can counter. Note that the threats  
    themselves are listed and not the associated ability. Multiple threats  
    must be separated by a semi-colon (;) and not by a comma.  
Traits - The followers traits are listed here separated by semi-colons. Use the  
    exact wording of the traits from the follower pane in-game. The Dancer  
    trait goes here and not under counters, as it will not fully counter the  
    Danger Zones mechanic.