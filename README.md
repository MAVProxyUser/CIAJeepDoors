# CIA Jeep Doors [dot] py
[Riding in a Jeep without doors will make you look at the brand in a whole new way!](https://getjerry.com/insights/riding-jeep-without-doors-will-make-you-look-brand-whole-new-way)<br>
*Jeeps are quite popular vehicles with a devoted following. One of the reasons for this is that some models of Jeeps allow you to ride with the doors and roof off, which is a rather unique feature among vehicles. However, this may carry some safety risks. 
Read on to find out more about what riding in a roof-less, door-less Jeep entails.*

* [What is this?](#what-is-this)
* [Why?](#why)
   * [Why else?!](#why-else)
* [TLDR; How do I use this!?](#tldr-how-do-i-use-this)
   * [Background](#background)
   * [Remote ID inception in the US via 'notice of proposed rulemaking' (NPRM)](#remote-id-inception-in-the-us-via-notice-of-proposed-rulemaking-nprm)
   * [Standard Remote ID UA Performance Requirements in the Final Ruling](#standard-remote-id-ua-performance-requirements-in-the-final-ruling)
   * [Major Changes from Proposed Rule to Final Rule](#major-changes-from-proposed-rule-to-final-rule)
   * [Comments opposing remote identificaton](#comments-opposing-remote-identificaton)
   * [Minimum Performance Requirements](#minimum-performance-requirements)
* [Additional insight](#additional-insight)
* [DJI specific commentary](#dji-specific-commentary)
* [Credits](#credits)
* [Should I contact someone about this?](#should-i-contact-someone-about-this)
   * [Will DJIFlySafe team help?](#will-djiflysafe-team-help)

# What is this? 
A tool to disable DJI Aeroscope Remote ID broadcasts & simultaneously demonstrate vendor non-compliance in DJI Remote ID performance requirements. The name happens to be an anagram of "DJI AeroScope".

So, what happens when a vendor has fallen out of compliance with FAA performance remote ID requirements? How about when an end user accidentally, or on purpose shows that a vendors performance requirements are inadequate? 

Is there a punishment, or consequence? Anything to worry about at all? 

# Why? 
Flying a DJI branded drone with the Aeroscope branded Remote ID tracking still fully enabled can be like riding in a jeep with no doors, or poorly secured doors! It sure is lots of fun, but can be perhaps a bit risky at times. You may want to consider shutting those doors up securely before going on an excursion! At the very least make sure they are shut properly if you do leave the doors on!

![Secure The Jeep Doors](https://github.com/MAVProxyUser/CIAJeepDoors/raw/main/SecureTheJeepDoors.gif)

Think of the doors on a jeep as being akin to a compliance mechanism for FAA. The FAA wants you to roll around with your doors completely off, or at a minimum unlocked, and open. 

## Why else?!
Privacy, ["REMOTE ID DOES VIOLATE THE FOURTH AMENDMENT"](https://jrupprechtlaw.com/racedayquads-llc-v-faa-lawsuit-challenging-drone-remote-identification-regulations/). 

*There were all sorts of shocking things that happened behind the scenes with this rulemaking such as multiple secret meetings the FAA with outside parties which were intentionally kept out of the public eye and were never fully disclosed on the record.*

[The United States Court of Appeals for the DC Circuit, Race Day Quads Oral Arguments](https://www.youtube.com/watch?v=pfxJRoHOfsw&t=4470s)
[![Privacy concerns](http://img.youtube.com/vi/pfxJRoHOfsw/0.jpg)](https://www.youtube.com/watch?v=pfxJRoHOfsw)<br>

[Petitioner's Brief](https://jrupprechtlaw.com/wp-content/uploads/2021/03/19-Brennan-and-RDQ-Opening-Brief.pdf)<br>
[Petitioner’s Addenda](https://jrupprechtlaw.com/wp-content/uploads/2021/08/19-Brennan-and-RDQ-Opening-Brief-Addenda.pdf)<br>
[RaceDayQuads Reply Brief](https://jrupprechtlaw.com/wp-content/uploads/2021/10/Reply-Brief.pdf)<br>

[Ultimate Guide to Remote Identification: Part 89, Lawsuits, Shocking Secrets, & More!](https://jrupprechtlaw.com/remote-identification/)

# TLDR; How do I use this!? 
People have been privately taking advantage of the DUML commands to [manipulate DJI AeroScope Remote ID status](https://github.com/jan2642/DUMLrub/blob/0e06bec4f8600a0b2214f8132b8de360047f019c/FlightController.rb#L396) for a number of years. Commands have been [openly discussed](https://dji-rev.com/dji-rev/pl/egxt1knyw3r68rawsfa5487nja) recently on the OG Mattermost server. 

[./comm_serialtalk.py](https://github.com/o-gs/dji-firmware-tools/blob/master/comm_serialtalk.py) ```/dev/ttyACM0 -a 2 -t 1000 -r 0300 -s 3 -i 218 -x 0500000000```

The command above is fairly simple. The most complex part of it is [understanding the privacy flag bits](https://github.com/MAVProxyUser/CIAJeepDoors/blob/main/CIAJeepdoors_1.3/CIAJeepDoors.py#L188). 

```
parser.add_argument('-p', '--privacy', type=str, default='',
            help='provide privacy flags\n'
            '.......x  Show/Hide serial number\n'
            '......x.  Show/Hide state like position, roll, yaw, imu data, ...\n'
            '.....x..  Show/Hide ReturnToHome position\n'
            '....x...  Show/Hide droneID\n'
            '...x....  Show/Hide flight purpose\n'
            '..x.....  Show/Hide UUID\n'
            '.x......  Show/Hide Pilot Position\n'
            'x.......  Show/Hide Unknown\n'
            '\n'
            '00000000 Will disable all broadcasts\n'
            '11111111 Will enable all broadcasts\n'
            '\n')
```

Both ./comm_serialtalk.py and CIAJeepDoors.py should be run from the root of the [OG DJI Firmware Tools](https://github.com/o-gs/dji-firmware-tools/) repo. 

As you can see from the *CIA Jeep Doors* python script the string of 0's in the comm_serialtalk.py command that has been privately circulating quite simply disables all the options in the broadcast, and disables it all together. There are in fact multiple options that can be applied to the AeroScope Remote ID broadcast, each enabling, or disabling some of the data that is shared. 

## Background

The [UAS Remote Identification Overview](https://www.faa.gov/uas/getting_started/remote_id/) as presented by the FAA outlines the status quo for upcoming Remote ID laws for the United States, set to be enforced 
starting in September '22. It is important to understand how these rulings came to be, and to reiterate concerns brought up during the initial rulemaking. Additionally it is important to know what ramifications exist for violation of the 
rulings, if any. Specifically on the part of manufacturers that have performance requirement minimum standards to meet. 

Several other countries have simultaneously created Remote ID requirements for UAS in parallel to the US rulings, this writeup will however specifically focus on US rullings. If you are interested in other implementations the European UAS standard is a 
great place to start, please take a look at: [Introduction to the European UAS digital Remote ID Technical Standard](https://asd-stan.org/wp-content/uploads/ASD-STAN_DRI_Introduction_to_the_European_digital_RID_UAS_Standard.pdf).

## Remote ID inception in the US via 'notice of proposed rulemaking' (NPRM)

During the initial rulemaking phases a number of concerns, and suggestions were put forth by the stakeholders tasked with advising the FAA on Remote ID. Many of those comments are extrapolated below, please make sure you read the surrounding context of each comment. 

[U.S. DOT FAA National Policy New Requirements for Registering and Marking Small Unmanned Aircraft](https://www.faa.gov/documentlibrary/media/notice/n_8900.338.pdf)<br>
December 22, 2015<br>
*The FAA recognizes the potential value remote identification would have to public safety and the safety of the National Airspace System(NAS). Accordingly,the UAS-ID ARC will inform the FAA on available technologies for remote identification and tracking, shortfalls in available standards, and make recommendations for how remote identification may be implemented.*

*The UAS-ID ARC will consist of members from the attached list of aviation community and industry member organizations, manufacturers, researchers, and standards bodies who are involved in the promotion of UAS, the production of UAS, and security 
issues surrounding the operation of UAS. FAA and other Agency subject matter experts may be requested to participate and provide technical support to ARC members.*

[U.S. DOT FAA ARC UAS Identification and Tracking Aviation Rulemaking Committee](https://www.faa.gov/regulations_policies/rulemaking/committees/documents/media/UAS_ID_and_Tracking_ARC_Charter_Membership.pdf)<br> 
May 04, 2017<br>
*The UAS-ID ARC will develop and submit to the FAA a recommendation report by September 30, 2017*

[UAS Identification and Tracking (UAS ID) Aviation Rulemaking Committee (ARC) ARC Recommendations Final 
Report](https://www.faa.gov/regulations_policies/rulemaking/committees/documents/media/UAS%20ID%20ARC%20Final%20Report%20with%20Appendices.pdf)<br> 
September 30, 2017<br>
*The full UAS-ID ARC met on June 21-23, 2017, and July 18-19, 2017, for the purpose of education and information gathering. The full UAS-ID ARC met again on August 16-17, 2017, and September 7-8, 2017, for the purpose of discussions and 
deliberations.*

*The ARC recommends that, regardless of which option for applicability the FAA chooses, the following UAS be exempt from remote ID and tracking requirements:
...
UAS that are exempted from ID and tracking requirements by the FAA (e.g., for the purposes of law enforcement, security or defense, or under an FAA waiver).*

*Apply the remote ID and tracking requirements to the remote pilot, not to the manufacturer of the UAS.*

*Require manufacturers to label their products to indicate whether they are capable of meeting applicable remote ID and tracking requirements. If a product is labeled as capable of meeting remote ID and tracking requirements, such capabilities 
must be enabled by default and the manufacturer must not present the user with an option to turn off the ID and tracking.*

*The ARC recommends a set of minimum data requirements for remote ID and tracking of UAS. (Sec 6.5, p. 39) The following types of data related to the UA or associated control station must be made available:
...
Identifying information of the UAS owner and remote pilot: This information would not be broadcast or published, but would be available from the PII System
...
Information available to designated public safety and airspace management officials: Access to personally identifiable (PII) information should be limited to public safety officials and similarly regulated public safety entities, including 
airspace management officials.
...
Information available to the FAA and certain identified Federal, State, and local agencies: All relevant tracking data should be retained for a reasonable period of time to allow public safety officials and other authorized users to have access to 
information critical to investigations.*

*The ARC recommends that the United States government be the sole keeper of any PII collected or submitted in connection with new UAS ID and tracking requirements.*

*The ARC recommends that the remote ID and tracking system include reasonable accommodations to protect the operational security of certain governmental UAS operations, consistent with accommodations provided to governmental operations in the 
manned space*

*Disclosure of Operationally Sensitive Information – Owner/operators may view negatively the loss of control of information associated with their flight operations. Even without disclosure of PII, the widespread availability of operational 
sensitive information (e.g., time, location, duration, flight frequency) could have an impact on an owner/operator’s perceived privacy and/or commercial interests. The holding of such information by a third party may be concerning to some UAS 
owner/operators, whereas some may prefer it. If broad operational data is available, it may be archived and mined for information which could be perceived as detrimental to the owner/operator. Even if access to such information is limited to 
public safety officials or through use agreements, the perception may be detrimental to the willingness to comply.*

*WG1 also considered whether each technology solution contains the following security measures:
Spoofing Security –A mechanism is in place that would make it more difficult for mischievous/malicious electronic intervention.
Tamper Proof – A mechanism is in place that would make it more difficult for mischievous/malicious physical intervention.*


## Standard Remote ID UA Performance Requirements in the Final Ruling
The final ruling has a number of performance requirements, but the ones listed below are particularly of interest to users seeking to evade AeroScope, or other Remote ID solutions. 

[Executive Summary Final Rule on Remote Identification of Unmanned Aircraft - Part 89](https://www.faa.gov/sites/faa.gov/files/2021-08/RemoteID_Executive_Summary.pdf)<br>
December 28, 2020

*Design and Production Rules for Manufacturers: A person designing or producing a standard UA or broadcast module must show that the UA or broadcast module met the performance requirements of the rule by following an FAA-accepted means of compliance.*

*Highlights of Standard Remote ID UA Performance Requirements: UA must self-test so UA cannot takeoff if Remote ID is not functioning. Remote ID cannot be disabled by the operator*

## Major Changes from Proposed Rule to Final Rule
*Network-based / Internet transmission requirements have been eliminated.*

[DOT FAA 14 CFR Parts 1, 11, 47, 48, 89, 91, and 107 Remote Identification of Unmanned Aircraft](https://www.faa.gov/sites/faa.gov/files/2021-08/RemoteID_Final_Rule.pdf)<br>
*SUMMARY: This action requires the remote identification of unmanned aircraft. The remote identification of unmanned aircraft in the airspace of the United States will address safety, national security, and law enforcement concerns regarding the further integration of these aircraft into the airspace of the United States, laying a foundation for enabling greater operational capabilities.*

*A person can operate a standard remote identification unmanned aircraft only if: (1) it has a serial number that is listed on an FAA-accepted declaration of compliance; (2) its remote identification equipment is functional and complies with the requirements of the rule from takeoff to shutdown; (3) its remote identification equipment and functionality have not been disabled*

*The FAA had not foreseen or accounted for many of these challenges when it proposed using the network solution and USS framework. After careful consideration of these challenges, informed by public comment, the FAA decided to eliminate the requirement in this rulemaking to transmit remote identification messages through an Internet connection to a Remote ID USS.*

## Comments opposing remote identificaton
*The FAA received a multitude of comments opposing remote identification. Many of the commenters opposed the concept, as a whole, while others expressed opposition to specific aspects, concepts, or proposed in the NPRM.*

One particularly interesing one is listed below from DJI. 

*DJI Technology, Inc. commented on its view that the NPRM reflected a fundamental change in philosophy, specifically that Americans cannot be trusted to act responsibly or in compliance with regulations. In addition, they stated the requirement raises technical challenges regarding design, application, and upgrades. They also noted potential legal liability concerns with the shift of responsibilities from the pilot to the manufacturer.*

The FAA also directly addressed an elephant in the room in one of their responses. 

*The FAA envisioned the UAS would have tamper-resistant design features to hinder the ability to make unauthorized changes to the remote identification equipment or messages.*

## Minimum Performance Requirements 
*Those requirements related to the control station location, automatic connection to a Remote ID USS, time mark, self-testing and monitoring, tamper resistance, connectivity, error correction, interference considerations, message transmission, message element performance requirements, and cybersecurity.*

[Federal Register/Vol. 86, No. 10 Remote Identification of Unmanned Aircraft](https://www.govinfo.gov/content/pkg/FR-2021-01-15/pdf/2020-28948.pdf)<br>

One interesting discussion centering around minimum standards comes from the discussion on *In-Flight Loss of Remote Identification Broadcast, and how to handle it*.

*Both standard remote identification unmanned aircraft and remote identification broadcast modules must continuously monitor their performance while in use and provide an indication if the remote identification equipment is not functioning properly. If the remote identification equipment provides an indication of failure or malfunction during flight, the unmanned aircraft operator must land the unmanned aircraft as soon as practicable.*

*The FAA expects that means of compliance will stipulate that only equipment failures or malfunctions would trigger a notification to the operator that the unmanned aircraft was no longer broadcasting the message elements.*

*Qualcomm Incorporated stated that a secure UAS should respond to a tamper event by noting the event and/or ceasing to operate.*

# Additional insight

[Federal Civil Aviation Programs: In Brief](https://sgp.fas.org/crs/misc/R42781.pdf)<br>
Updated January 22, 2021<br>
*In January 2021, FAA also issued regulations requiring all UAS to either equip with remote identification capabilities or limit flights to remain within FAA-recognized identification areas under visual line of sight. In general, remote identification will require continuous broadcast of identification, location, and performance data from takeoff until system shutdown. Newly manufactured UAS will need to meet FAA standards for remote identification equipage by September 16, 2022, while all UAS operators will need to comply with remote identification operational requirements by September 16, 2023. Existing UAS not manufactured with remote identification capabilities will be either required to be retrofitted with remote identification broadcast modules or limited to operations within FAA-recognized identification areas. Under FAA’s implementation plan, a network of approved remote identification service suppliers would track location and identification information transmitted from drones in real-time and provide UAS traffic management services to drone operators. The fee structure for such services is yet to be determined. The implementation of remote identification is seen as a step toward fully integrating a wider range of beyond-visual-line-of-sight operations, such as drone package delivery and remote infrastructure monitoring, into the national airspace system*

Concerns [Submitted on Behalf of the News Media Coalition](https://www.spj.org/pdf/ldf/comments-of-news-media-coalition-uas-rid.pdf)<br>
*The Coalition, however, is concerned that the proposed rules constitute impermissible government surveillance of a journalist’s drone operations in violation of the First Amendment. Therefore, the Coalition urges the FAA to exempt newsgatherers operating drones in Class G airspace from compliance with any remote ID requirements by establishing an “accredited news representative” designation that ensures there will not be impermissible government surveillance of journalists. In the event the FAA does not exempt journalists from these requirements, the Coalition urges the FAA to reconsider key elements of its Remote ID NPRM.*

[FAA’s Compliance and Enforcement Approach for Drones Could Benefit from Improved Communication and Data](https://www.gao.gov/assets/gao-20-29.pdf)<br>
*most law enforcement stakeholders GAO met with (9 of 11) stated that officers may not know how to respond to UAS incidents or what information to share with FAA*

![Examples](https://github.com/MAVProxyUser/CIAJeepDoors/raw/main/GAO-20-29-ExamplesOnUnsageUAS.png)

[AMA A Better Final Rule for Remote Identification of UAS](https://mobile.reginfo.gov/public/do/eoDownloadDocument?pubId=&eodoc=true&documentID=7281)<br>
*The FAA failed to identify any existing safety or security issues with the operations of traditional model aircraft in its proposed remote identification regulatory regime.*

[COMMENTS OF THE ASSOCIATION FOR UNMANNED VEHICLE SYSTEMS INTERNATIONAL](https://downloads.regulations.gov/FAA-2020-1086-0025/attachment_1.pdf)<br>
*The FAA Should Recognize Clear Encryption and Tamper Resistance Standards as a Baseline for Compliance.*

# DJI specific commentary 

[DJI Proposes Electronic Identification Framework For Small Drones](https://www.dji.com/newsroom/news/dji-proposes-electronic-identification-framework-for-small-drones)<br>
*DJI understands that accountability is a key part of responsible drone use, and we have outlined a proposal that balances the privacy of drone operators with the legitimate concerns authorities have about some drone operations,” said Brendan Schulman, DJI Vice President of Policy and Legal Affairs. “This is another example of how the UAS industry is innovating solutions to emerging concerns, and we look forward to working with other stakeholders on how to implement the best possible system.*

*Last year, the United States Congress directed the U.S. Federal Aviation Administration (FAA) to develop approaches to remotely identifying the operators and owners of unmanned aircraft, and set deadlines for doing so over the next two years. DJI has outlined a concept in which each drone would transmit its location as well as a registration number or similar identification code, using inexpensive radio equipment that is already on board many drones today and that could be adopted by all manufacturers.*

["What's In a Name?" A Call for a Balanced Remote Identification Approach](https://www.dropbox.com/s/v4lkyr2kdp8ukvx/DJI%20Remote%20Identification%20Whitepaper%203-22-17.pdf?dl=0)<br>
*No other technology is subject to mandatory industry-wide tracking and recording of its use, and we strongly urge against making UAS the first such technology. The case for such an Orwellian model has not been made*

[UAS REMOTE ID USE THE RADIO YOU HAVE - Walter stockwell](https://www.icao.int/Meetings/UAS2017/Documents/Walter%20Stockwell_Stream%20A.pdf)<br>

[DroneEnable UTM – Registration, identification and tracking talk at ICAO](https://www.youtube.com/watch?v=uP6KIVuJsjU&t=1148s)<br>

[DJI Demonstrates ‘Drone License Plate’ Technology And Drone Pilot Knowledge Quiz](https://www.dji.com/newsroom/news/dji-demonstrates-drone-license-plate-technology-and-knowledge-quiz)<br>

[DJI Introduces Voluntary Flight Identification Options For Drone Pilots](https://www.dji.com/newsroom/news/dji-introduces-voluntary-flight-identification-options-for-drone-pilots)<br>

[Understanding DJI’s AeroScope Solution by Brendan Schulman](https://static1.squarespace.com/static/589e20c9197aea0415f0e930/t/5a25969de2c4831af40e12e0/1512412829908/DJI+Response+to+D13.PDF)<br>
*Concerns about spoofing: Registration and ID solutions do not seek to stop the “bad actors” who will find ways to operate outside the system, just as a license plate system does not do anything to prevent people from removing, forging, covering, or stealing and swapping license plates. We have also heard from safety and security agencies that the goal for remote ID is to have a high percentage of drones identified, with an expectation that some drones will never be identified. Second, to “jailbreak” a drone via software hacking is both a violation of DJI terms of use (because it compromises safety features) and also beyond the capabilities or interest of the vast majority of drone users. Those who would spoof their identification information in the face of a legal requirement would likely buy a non-ID-compliant brand or self-built drone anyway. Moreover, other remote ID solutions that allow drone users to provide ID information into a system will also be susceptible to some risk of spoofing, perhaps on a system-wide basis.*

# Credits
This software is based on the work of the DJI OG's (Formerly on Slack, now on [Mattermost](https://dji-rev.com/dji-rev/channels/town-square)). Specific thanks to the giant's whom this work stands on the shoulders of: [jan2642](https://github.com/jan2642), [freaky123](https://github.com/fvantienen), [bin4ry](https://github.com/Bin4ry/), and others. After root access was provided to the DJI product line, a number of OG's assisted in understanding the DUML protocol, disassembling the flight controller binaries, and making DUML based tools to adjust the Drone ID paramaters within the flight controller. Without the team effort, these tools would not exist. 

# Should I contact someone about this? 
Maybe? Call 844-FLY-MY-UA or email UASHelp@faa.gov? We aren't sure how compliance is handled for vendor performance requirements. 

[FAA Contacts for Law Enforcement](https://www.faa.gov/uas/public_safety_gov/contacts/)

## Will DJIFlySafe team help? 
DJI should create a process by wich Remote ID can be disabled for individuals with appropriate exemptions, or whom live in countries in which no Remote ID rules exist. This should be handled via the standard [DJI unlock interface](https://fly-safe.dji.com/unlock/unlock-request/list). Please reach out to [DJI FLySafe team](https://twitter.com/DJIFlySafe) and ask for help facilitating this request. Try emailing Flysafe@dji.com
