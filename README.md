# Overview

The idea of Kids Calendar is fair simple. I want to create a calendar based on their schools calendar days (rotation day, encore day, etc.) and their assignments. 
For example, Jane may have Music in Day A, Art in Day B, Library in Day C and Joe may have Spanish and Library in Day A, Music and Engineering in Day B and so on.
Users can subscribe to kids calendar on their apps (phones, laptops etc) and follow kids agenda easily.

# Technical design
System is based on Python and AWS and do the following:
* pulls school calendar from specified location
* use settings to assign specific day activities for specific day for every kid
* update kids calendar
* update kids settings
* support schedule for regular updates

It's pretty developer oriented now and all changes can be done via config files and Python code (both logic and deployment that's defined in AWS CDK)

