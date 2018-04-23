^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package camera_control_msgs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.0.10 (2016-04-12)
-------------------
* removed outdated 'SetBrightnessSrv.srv', 'SetExposureSrv.srv', and 'SetSleepingSrv.srv'
* 0.0.8
* added LICENSE.rst file
* Contributors: Magazino Version Daemon, Marcel Debout

0.0.7 (2016-03-29)
------------------
* BinningSrv is now implemented
* Contributors: Marcel Debout

0.0.6 (2016-03-17 12:51)
------------------------
* std_srvs not yet used
* Contributors: Marcel Debout

0.0.5 (2016-03-17 12:31)
------------------------
* removed unused dependencies and added missing one
* Contributors: Marcel Debout

0.0.4 (2016-03-15)
------------------
* Merge branch 'brightness_bug_fixing' of bitbucket.org:Magazino/camera_control_msgs
* removed suffix 'srv', old services marked as deprecated
* 0.0.3
* setBinning.srv not yet implemented, because it needs to close and reopen the camera
* added SetBinning.srv
* removed deprecated SequenceExposureTimes msgs
* added feedback to to SetBrightnessSrv, GrabImagesInterface should not provide the continuous mode, so removed it
* added comments, added brightness continuous functionallity to the set BrightnessSrv
* extended interface with gain, gamma and correct brightness handling
* Contributors: Magazino Version Daemon, Marcel Debout

0.0.3 (2016-02-08)
------------------
* Added Service to set the desired gain
* Contributors: Marcel Debout

0.0.2 (2016-01-21)
------------------
* Added SetBool service.
  I'd like to remove this srv file soon once a new version of the std_srvs
  package is released.
* Contributors: Markus Grimm

0.0.1 (2016-01-11)
------------------
* reset version information
* nice package.xml, making catkin lint happy
* removed GrabSequence.action, is now in GrabImages.action
* fixed merge conf
* new actions for grabbing trigger
* fied package name
* fixed package name in package.xml
* initial commit -> renaming from pylon_camera_msgs
* Contributors: Marcel Debout, Nikolas Engelhard, Ulrich Klank
