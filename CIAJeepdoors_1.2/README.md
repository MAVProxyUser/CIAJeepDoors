# CIA Jeep Doors

* [How-to](#how-to)
* [Verification](#verification)
* [Gotchas](#gotchas)
* [Issues](#issues)

# How-to

This code expects to be run from the root of the [dji-firmware-tools](https://github.com/o-gs/dji-firmware-tools) repo. 

Git clone [dji-firmware-tools](https://github.com/o-gs/dji-firmware-tools.git)

Copy CIAJeepdoors_1.2/CIAJeepDoors.py to dji-firmware-tools folder

Run it! 

# Verification
These tools were tested alongside both an [SDR](https://github.com/proto17/dji_droneid) and an [AeroScope mobile unit](https://twitter.com/Bin4ryDigit/status/1512785076932726791) by [Bin4ry](https://twitter.com/Bin4ryDigit/status/1512785088743890952) & other OG's against DJI EnhancedWifi, and DJI Occusync. LightBridge has yet to be verified, but should handle the same way.  A variety of drone models have been tested. Recent fixes have been applied to allow use with [M300](https://www.dji.com/matrice-300) series (for big boys). 

# Gotchas
If your drone makes use of [DJI FLy app](https://apps.apple.com/us/app/dji-fly/id1479649251), please beware that the Apple iOS version will reset the privacy bits when it is used. You will likely want to use [Android](https://service-adhoc.dji.com/download/app/android/3b03cb95-bc4b-4b62-b4ab-9cf977d77309) instead.  
[Please only use Android DJI Fly, the iOS version will reset the privacy bits](https://github.com/MAVProxyUser/CIAJeepDoors/blob/main/CIAJeepdoors_1.2/CIAJeepDoors.py#L256)

# Issues
Please [submit any issues via GitHub](https://github.com/MAVProxyUser/CIAJeepDoors/issues), do not Bug OG's on Mattermost. 


