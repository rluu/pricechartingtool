#!/usr/bin/env python3
##############################################################################

import datetime
import pytz

##############################################################################

#timezone = pytz.timezone("US/Eastern")
eastern = pytz.timezone("US/Eastern")
central = pytz.timezone("US/Central")

# WWI broke out in 1914.  pg 7.
# Just "1914" is given.
# Actual breakout of war was July 28, 1914.
ww1BrokeOutPg7 = datetime.datetime(year=1914, month=7, day=28,
                                      hour=12, minute=0,
                                      tzinfo=eastern)

# US entered World War in 1917.   pg. 10
# Young Robert was 11 years old.  
usEnteredWorldWarPg10 = datetime.datetime(year=1917, month=4, day=6,
                                      hour=12, minute=0,
                                      tzinfo=eastern)

# June 9, 1919 (NYC?)
# Mr. K was in NYC many years ago.  pg. 64-65.
mrKInNYCPg64 = datetime.datetime(year=1919, month=6, day=9,
                                 hour=12, minute=0,
                                 tzinfo=eastern)

# Mr. K: Oil stocks high of November 3, 1919.
# pg. 64-65.
mrKOilStocksHighPg65 = datetime.datetime(year=1919, month=11, day=3,
                                         hour=12, minute=0,
                                         tzinfo=eastern)

# Mr. K: Oil stocks low of August 24, 1921.
# pg. 64-65.
mrKOilStocksLowPg65 = datetime.datetime(year=1921, month=8, day=24,
                                         hour=12, minute=0,
                                         tzinfo=eastern)


# SF Earthquake.
# pg. 1.
sfEarthquakePg1 = datetime.datetime(year=1906, month=4, day=18,
                               hour=5, minute=12,
                               tzinfo=eastern)

# RG birthday
# pg. 1.
rgBirthday1906Pg1 = datetime.datetime(year=1906, month=6, day=9,
                               hour=19, minute=20,
                               tzinfo=eastern)


# Marie Birthday Candidate. pg. 179, 197.
# [Using new moon.]
marieBirthdayCandidatePg179 = datetime.datetime(year=1926, month=10, day=6,
                               hour=17, minute=14,
                               tzinfo=eastern)

# Beautiful sunshiny.  Window.  Open arms.  Face.  Sherman. pg. 40
# [Using around sunset.]
windowPg40 = datetime.datetime(year=1926, month=10, day=23,
                               hour=17, minute=45,
                               tzinfo=central)

# Christmas 1926.  pg. 42.
christmas1926Pg42 = datetime.datetime(year=1926, month=12, day=25,
                                  hour=12, minute=0,
                                  tzinfo=central)

# Letter of commendation. pg. 43.
letterOfCommendationPg43 = datetime.datetime(year=1927, month=1, day=1,
                                         hour=12, minute=0,
                                         tzinfo=eastern)

# Letter from RG @ Texarkana to Mr. J.H.K.
letterRGTexarkanatoMrKpg62 = datetime.datetime(year=1927, month=1, day=15,
                                               hour=12, minute=0,
                                               tzinfo=eastern)

# Letter from Walter @ NYC.  pg. 63.
letterWalterInNYCPg63 = datetime.datetime(year=1927, month=1, day=12,
                                      hour=12, minute=0,
                                      tzinfo=eastern)

# Letter #2 from RG to Mr. K.  pg. 65.
letterRGtoMrK2Pg65 = datetime.datetime(year=1927, month=1, day=24,
                                   hour=12, minute=0,
                                   tzinfo=eastern)

# RG start on road to fame and fortune.  pg. 70
# [Using sunset]
rgRoadToFameAndFortunePg70 = datetime.datetime(year=1927, month=1, day=24,
                                   hour=17, minute=45,
                                   tzinfo=central)


# Marie's letter to RG.  pg. 71.
marieLetterToRgPg71 = datetime.datetime(year=1927, month=1, day=26,
                                        hour=12, minute=0,
                                        tzinfo=eastern)

# Future Cycles Article.  pg. 75
futureCyclesPg75 = datetime.datetime(year=1927, month=1, day=28,
                                 hour=12, minute=0,
                                 tzinfo=eastern)

# Outbreak of the World War in 1914.  pg. 80.
ww1OutbreakPg80 = datetime.datetime(year=1914, month=7, day=28,
                                     hour=12, minute=0,
                                     tzinfo=eastern)

# First non-stop flight from St. John's, Newfoundland, to Ireland. [pg. 87]
# June 1919.
# Actual flight was on June 14th, landing on June 15th, 1919.
# [Using June 14th, 1919].
nonStopFlightToIrelandPg87 = datetime.datetime(year=1919, month=6, day=14,
                                     hour=12, minute=0,
                                     tzinfo=eastern)

# Mr. K faith in RG. pg. 91.
mrKFaithInRgPg91 = datetime.datetime(year=1927, month=2, day=1,
                                     hour=12, minute=0,
                                     tzinfo=eastern)

# Great victory.  pg. 92
# Saturday night.  [Using sunset.]
rgGreatVictoryPg92 = datetime.datetime(year=1927, month=2, day=5,
                                   hour=17, minute=20,
                                   tzinfo=eastern)

# Marie love of the heart of one little woman.  pg. 94.
# A.M. Morning.  [Using sunrise.]
marieHopePrayLoveOfHeartPg94 = datetime.datetime(year=1927, month=2, day=7,
                                             hour=7, minute=5,
                                             tzinfo=eastern)


# Cotton started up fast. pg. 94.
cottonStartedUpFastPg94 = datetime.datetime(year=1927, month=2, day=23,
                                        hour=12, minute=0,
                                        tzinfo=eastern)

# Cotton advanced to 14.80, RG progress. pg. 94.
# Connection to low level in January.
cottonAdvancePg94 = datetime.datetime(year=1927, month=3, day=2,
                                      hour=12, minute=0,
                                      tzinfo=eastern)

# No profit on cotton deal. pg. 95
noProfitMarieFaith400pg95 = datetime.datetime(year=1927, month=3, day=15,
                                              hour=12, minute=0,
                                              tzinfo=eastern)

# RG purchase of cotton with Marie's money. pg. 96
# Marie faith trade.
# Note: G.Saturn goes retrograde on this date.
marieFaithTradeCottonPurchasePg96 = datetime.datetime(year=1927, month=3, day=17,
                                            hour=12, minute=0,
                                            tzinfo=eastern)

# Flood started in Mississippi Valley.
floodStartedMississippiValleyPg96 = datetime.datetime(year=1927, month=4, day=20,
                                                  hour=12, minute=0,
                                                  tzinfo=eastern)

# St. Louis Birthday.  pg. 96.
stLouisBirthdayPg96 = datetime.datetime(year=1927, month=4, day=25,
                                    hour=12, minute=0,
                                    tzinfo=eastern)

# Fortune smiling on RG and Marie.  pg. 97.
fortuneSmilingPg97 = datetime.datetime(year=1927, month=4, day=30,
                                       hour=12, minute=0,
                                       tzinfo=eastern)

# Marie love and trust. pg. 97.
marieLoveAndTrustPg97 = datetime.datetime(year=1927, month=5, day=1,
                                          hour=12, minute=0,
                                          tzinfo=eastern)

# RG greatest week in RG's life up to that time. (week ending on this date). pg. 101
rgGreatestWeekUpToThatTimePg101 = datetime.datetime(year=1927, month=5, day=7,
                                                hour=12, minute=0,
                                                tzinfo=eastern)

# RG in Mr. K's private office, conference.  Saturday morning.  pg. 101.
# Fact: happy and faith.
# Reading about contemplated planes over Atlantic.
rgAndMrKConferencePrivateOfficePg101 = datetime.datetime(year=1927, month=5, day=7,
                                                    hour=5, minute=0,
                                                    tzinfo=eastern)

# RG arrives in Sherman, Marie meets him at the train.  Marie overjoyed at success.
# pg. 102
rgGreatestWeekUpToThatTimePg102 = datetime.datetime(year=1927, month=5, day=7,
                                                hour=18, minute=0,
                                                tzinfo=eastern)

# RG in Sherman, and Marie met him at the train.
# Marie overjoyed with RG's success.
# Saturday evening, May 7, 1927.
marieOverjoyedAtRGSuccessPg103 = datetime.datetime(year=1927, month=5, day=7,
                                                   hour=19, minute=0,
                                                   tzinfo=eastern)

# RG leaves Sherman for Texarkana, with Marie's promise.  pg. 103.
# Sunday afternoon.  Reads Bible Sunday night.
# [Using sunset.]
# RG hopes to build airplane outlined by Ezekiel.
mariesPromisePg103 = datetime.datetime(year=1927, month=5, day=8,
                                       hour=19, minute=0,
                                       tzinfo=eastern)

# Now was the time to start buying wheat and corn.
# pg. 103.
timeToStartBuyingWheatAndCornPg103 = datetime.datetime(year=1927, month=5, day=19,
                                                  hour=12, minute=0,
                                                  tzinfo=eastern)

# RG buys corn for Marie's account.
# pg. 103.
# RG tells Mr. K he figured wheat and corn were now going to have a big advance.
rgBuysCornForMariesAccountPg103 = datetime.datetime(year=1927, month=5, day=20,
                                                  hour=12, minute=0,
                                                  tzinfo=eastern)

# Lindbergh passed over Ireland early that morning.
# [Using sunrise].
# pg. 105.
lindberghOverIrelandPg105 = datetime.datetime(year=1927, month=5, day=21,
                                   hour=4, minute=40,
                                   tzinfo=eastern)

# RG Red Letter Day.  RG WAITed in the telegraph office until 5 pm.
# Fired enthusiasm.
# pg. 105.
rgRedLetterDayPg105 = datetime.datetime(year=1927, month=5, day=21,
                                   hour=17, minute=0,
                                   tzinfo=eastern)

# RG dream on train to Sherman, with lightest heart.  Happy.  Dream to be realized.
# Money for plans on great airplane.  Lindbergh's flight.
# Marie welcomed him with enthusiasm and open arms.  
# Ezekiel plane, eagle, with wheel within wheel, would one day become a reality..
# Sunset.
# pg. 107-108.
rgLightestHeartPg108 = datetime.datetime(year=1927, month=5, day=28,
                                   hour=19, minute=10,
                                   tzinfo=eastern)

# Robert and Marie went to Dallas (from Sherman).
# Planned when ready to elope, Marie would leave from Dallas on the Sunshine Special.  pg. 110.
rgAndMarieInDallasPg110 = datetime.datetime(year=1927, month=5, day=29,
                                       hour=12, minute=0,
                                       tzinfo=eastern)

# Robert and Marie return to Sherman (from Dallas), Sunday afternoon.  pg. 111.
rgAndMarieReturnToShermanPg111 = datetime.datetime(year=1927, month=5, day=29,
                                       hour=19, minute=15,
                                       tzinfo=eastern)

# RG with Marie at Sherman (Monday forenoon)
# pg. 111.
rgAndMarieInShermanPg111 = datetime.datetime(year=1927, month=5, day=30,
                                       hour=9, minute=0,
                                       tzinfo=eastern)

# RG says goodbye to Marie and started back from Sherman to Texarkana.
# From that time on, RG counted the minutes in anticipation of the
# great happiness of the following Sunday, when they would married in
# St. Louis.
# [using sunset]
# pg. 111.
rgSaysGoodbyeToMariePg111 = datetime.datetime(year=1927, month=5, day=30,
                                       hour=19, minute=15,
                                       tzinfo=eastern)

# RG started early to Mr. K's office.  Last day in the office.  Tuesday morning.
# [using sunrise]
# pg. 106,112.
rgLastDayInMrKOfficePg112 = datetime.datetime(year=1927, month=5, day=31,
                                       hour=4, minute=30,
                                       tzinfo=eastern)

# RG figured according to cycle theory cotton and wheat and corn top for a reaction.
# pg. 112.
rgCycleTheoryPg112 = datetime.datetime(year=1927, month=6, day=1,
                                       hour=12, minute=0,
                                       tzinfo=eastern)

# RG told Mr. K Saturday morning he was going to buy wheat and corn,
# b/c he was getting ready to go away that afternoon.
# Mr. K. New York exchange for wedding present.
# Mr. Made back money from Oil losses 1919.
# RG to have everything in cash and ready to make a new start after the honeymoon.
# pg. 113.
rgMrKWeddingPresentPg113 = datetime.datetime(year=1927, month=6, day=4,
                                        hour=6, minute=0,
                                        tzinfo=eastern)

# RG was so happy that he called Marie over the long-distance phone, and told her of his great success in the market in wheat [war?]
# Marie making arrangements to go to Dallas and leave from Dallas that afternoon on Sunshine Special.
# He was to keep everything quiet about elopment, father might stop her.
# RG quiet about resigning from Mr. K.
# [No exact time] [using 2 pm].
# pg. 114.
rgCallsMarieOverLongDistanceBcSuccessPg114 = \
                                    datetime.datetime(year=1927, month=6, day=4,
                                                          hour=14, minute=0,
                                                          tzinfo=eastern)

# RG walked into railroad station at Texarkana and buys ticket for St. Louis with reservation on the Sunshine Speical.
# pg. 115.
rgRailroadStationAtTexarkanaTicketPg115 = \
                                        datetime.datetime(year=1927, month=6, day=4,
                                          hour=19, minute=0,
                                          tzinfo=eastern)

# RG heart in throat.  Sunshine special late on Saturday night. [Unknown exact time]
# pg. 116.
rgHeartInThroatPg116 = datetime.datetime(year=1927, month=6, day=4,
                                         hour=20, minute=0,
                                         tzinfo=eastern)

# RG and Marie talk about plans until after midnight on Sunshine Special.
# pg. 116.
# [Using 12:30 am]
rgMariePlansOnSunshineSpecialPg116 = datetime.datetime(year=1927, month=6, day=5,
                                         hour=0, minute=30,
                                         tzinfo=eastern)

# RG arose early and dressed, hurried back to Marie's car on Sunshine Special.
# 8 o'clock.
# pg. 118
searchForMariePg118 = datetime.datetime(year=1927, month=6, day=5,
                                        hour=8, minute=0,
                                        tzinfo=eastern)

# Marie's mysterious letter, written by her hand.
# pg. 120.
marieMysteriousLetterPg120 = datetime.datetime(year=1927, month=6, day=5,
                                               hour=3, minute=0,
                                               tzinfo=eastern)

# RG boards local airplane for Silver Springs and arrived in the afternoon.
# It was a fitting setting for the scene.  Beautiful, sunshine. [pg. 257].
#
# Sunday morning about 10 o'clock.
# [Unknown which date this is for.  Using 1927-06-05 10:00 am.]
# 
rgAirplaneToSilverSpringPg257_candidate1 = datetime.datetime(year=1927, month=6, day=5,
                                                     hour=10, minute=0,
                                                     tzinfo=eastern)

# Nearly 12 o'clock noon.
# pg. 123
nearlyNoonUnionStationClockPg123 = datetime.datetime(year=1927, month=6, day=5,
                                                     hour=11, minute=40,
                                                     tzinfo=eastern)

# Noon at St. Louis.  Trust in the word of god.
# pg. 123.
noonUnionStationClockPg123 = datetime.datetime(year=1927, month=6, day=5,
                                               hour=12, minute=0,
                                               tzinfo=eastern)

# RG troubled and discouraged.  Heart sad.
# 12:45 pm
# pg. 124.
rgTroubledAndDiscouragedHeartSadPg124 = datetime.datetime(year=1927, month=6, day=5,
                                   hour=12, minute=45,
                                   tzinfo=eastern)

# Time appointed to wait.  1:00 pm.
# pg. 125.
rgTimeAppointedToWaitPg125 = datetime.datetime(year=1927, month=6, day=5,
                                   hour=13, minute=0,
                                   tzinfo=eastern)

# Hopeless to wait.  Marie gone away or an accident.
# Secret confided.
# After 1:30 pm.
# pg. 131.
rgHopelessToWaitSecretConfidedPg131 = datetime.datetime(year=1927, month=6, day=5,
                                          hour=13, minute=30,
                                          tzinfo=eastern)

# Heart heavy, shock.  S.E. Kiser.
# After 6 pm.
# pg. 133-137.
rgHeartHeavyShockRingPg133 = datetime.datetime(year=1927, month=6, day=5,
                                          hour=18, minute=0,
                                          tzinfo=eastern)


# Sun thru window of east window.  Light breakfast.
# Morning. [using sunrise.]
# Little book on bed.
# pg. 137-139.
sunThruWindowOfHotelPg137 = datetime.datetime(year=1927, month=6, day=6,
                                          hour=4, minute=30,
                                          tzinfo=eastern)

# Looking for word received.  Fact of baggage.  Prayer to universal power.
# Strength, word gives comfort and consolation.
# Sign of money.  Need.
# About 8'oclock that night.
# pg. 140-144.
prayerToUniversalPowerSignNeedPg140 = datetime.datetime(year=1927, month=6, day=6,
                                          hour=20, minute=0,
                                          tzinfo=eastern)

# RG bought the evening paper and looked over the financial page.  RG
# still holding Right Aeroplane stock which he had bought at 31 on May
# 21, the day that Captain Lindbergh completed his successful flight
# to Paris.  He figured he could make a great fortune by buying Right
# Aeroplane stock and holding it for eyasr and at the same time
# selling MM short.  Fact that he was making money on RA stock
# encouraged him to work on his own plane.
# [using sunset]
# pg. 146.
rgHoldingRAFactPg146 = datetime.datetime(year=1927, month=6, day=6,
                                                 hour=19, minute=20,
                                                 tzinfo=eastern)

# Mr. K on the wire.  Mr. K's voice.
# WARNING: Timestamp could be Monday June 6, 1927 or Tuesday June 7, 1927, because jump in the timeline.
# About 8:15 telephone rang.
# pg. 147.
mrKOnTelephoneWireJune6Pg147 = datetime.datetime(year=1927, month=6, day=6,
                                                 hour=20, minute=15,
                                                 tzinfo=eastern)
mrKOnTelephoneWireJune7Pg147 = datetime.datetime(year=1927, month=6, day=7,
                                                 hour=20, minute=15,
                                                 tzinfo=eastern)

# Opening on Tuesday morning.  Buy cotton, wheat and sell Major
# Motors.  Early breakfast, bought news paper and read all about the
# receptions being planned for COlonel Lindbergh and again the wish
# stole into his heart and the hope was revived that in some way Marie
# might be with him when Lindbergh arrived in NY.
# pg. 152.
# [Using sunrise.]
openingOnTuesdayMorningJune7Pg152 = datetime.datetime(year=1927, month=6, day=7,
                                                 hour=4, minute=30,
                                                 tzinfo=eastern)

# Letter from Mr. and Mrs. Stanton from Texarkana to Planters Hotel in St. Louis.
# Deeply grieved.  Believe us.
# pg. 153.
# No timestamp given.  [using noon.]
stantonsDeepLetterToRGAtPlantersPg153 = datetime.datetime(year=1927, month=6, day=6,
                                                 hour=12, minute=0,
                                                 tzinfo=eastern)

# Letter from RG to friends Mr. and Mrs. Stanton, from St. Louis to Texarkana.
# Friends, sorrow, extend help in time of sorrow.  Trouble brings friends.
# No timestamp given, [using noon.]
# pg. 154.
letterRgToStantonsPg154 = datetime.datetime(year=1927, month=6, day=7,
                                                 hour=12, minute=0,
                                                 tzinfo=eastern)

# Newspapers were out.  Cotton and wheat advanced.
# Gods of good fortune and finance smiling.
# Goddess of Love frowning.  Must have patience.
# After 3 o'clock.
# pg. 156.
newspapersWereOutPg156 = datetime.datetime(year=1927, month=6, day=7,
                                   hour=15, minute=0,
                                   tzinfo=eastern)

# Day waning, sunset, sadness.  RG firmly resolved to carry out his
# intention to place personal notice in the papers the following day.
# [using sunset, Tuesday evening].
# pg. 156, 148, 152.
sunsetDayWaningSadnessPg156 = datetime.datetime(year=1927, month=6, day=7,
                                                hour=19, minute=20,
                                                tzinfo=eastern)

# RG arose early on Wednesday morning, June 8, hastened to the
# newspaper offices and placed the personal notices to appear the
# following day.When he returned to his hotel, for the first time
# since Sunday, he thought of his birthday, June 9, when he would be
# 21 years of age.  Great hope came to mind that she would be his
# birthday present.  Sudden inspiration.  Surprise of his life.
# [Using sunrise]
# pg. 157.
personalNoticesPlacedPg157 = datetime.datetime(year=1927, month=6, day=8,
                                   hour=4, minute=30,
                                   tzinfo=eastern)

# RG had light supper and read over marie poems.  Shell broken.
# RG went to sleep to dream of his birthday.
# [using sunset.]
# pg. 159-160.
rgDreamsOfHisBirthdayPg160 = datetime.datetime(year=1927, month=6, day=8,
                                               hour=19, minute=20,
                                               tzinfo=eastern)

# RG's 21st birthday [1927].  Arose early.  RG secured the morning papers and
# saw his personal notices.  Added name of hotel and telephone number.
# Last disappointment in his love affairs, this birthday to be a turning point.
# On this birthday, he was worth $30,000.
# [Marie's promise G.Sun @ 47 to RG birthday G.Sun @ 77 = 30 deg elapsed.]
# pg. 161.
# [using sunrise.]
rgBirthday1927Pg161 = datetime.datetime(year=1927, month=6, day=9,
                                   hour=4, minute=30,
                                   tzinfo=eastern)

# Around 11 or 12, Marie would either come to the hotel or some news
# of her would be received.
# pg. 162.

# Mind reverted back to Sunday watching clock at Union station, hoping
# and waiting.  RG restless and anxious.
# 11 o'clock [am Thursday, June 9, 1927]
# pg. 162.
clockAt11OnRGBirthdayMindRevertPg162 = datetime.datetime(year=1927, month=6, day=9,
                                   hour=11, minute=0,
                                   tzinfo=eastern)

# Clock struck 12 on RG's birthday.  No news of Marie.
# pg. 162.
clockAt12OnRGBirthdayPg162 = datetime.datetime(year=1927, month=6, day=9,
                                   hour=12, minute=0,
                                   tzinfo=eastern)

# A few minutes after 12 on RG's birthday.  Messenger boy with
# telegram from Walter.
# pg. 162.
clockAfter12OnRGBirthdayPg162 = datetime.datetime(year=1927, month=6, day=9,
                                   hour=12, minute=10,
                                   tzinfo=eastern)

# A little later in the day, RG received a long telegram from Mr. K,
# congratulating him on his birthday, and offering words of
# encouragement, also telling RG that he expected to leave Texarkana
# on Friday night, June 10th and arrive in St. Louis some time int eh
# morning, and that RG should be ready to start with him to NY, as he
# wanted to be there when lindbergh arrived.  RG received another
# telegram from his mother congratulating him on his birthday and
# wishing him every success and happiness.
#
# These messages were encouraging but it was now 2 o'clock.
# pg. 163.
rgBeganToBeDisappointedOverHopefulPg163 = datetime.datetime(year=1927, month=6, day=9,
                                   hour=14, minute=0,
                                   tzinfo=eastern)

# At close of another day of disappointment. [pg. 166-167] [close of June 9, 1927]
# Birthday passing, hopes for the present blasted.
# pg. 171.  Great disappointment was hopes for Marie on that day were blasted.
# pg. 171.  RG bought evening newspapers and looked over the Financial Page, cotton wheat and corn advanced.
# pg. 171.  RG birthday been a success financially, 21st birthday found him on top of the world.
#
# [using sunset]
rgBoughtEveningNewsPaperLookedOverFinancialPagePg171 = datetime.datetime(year=1927, month=6, day=9,
                                   hour=19, minute=20,
                                   tzinfo=eastern)

# Coming morning [morning of June 10, 1927], meet the future with a smile,
# face it with hope. [pg. 169-170].
#
# RG called to see Madam Cleo early in the morning.  She said he had
# gone thru a great sorrow, but his sweetheart would return to him in
# a few days.  RG felt more hopeful and returned to his hotel, hoping
# to get some news of Marie.  Calculations showed wheat and cotton
# should be top for a reaction, so he wired broker in NY to sell.
# pg. 172.
# [using sunrise]
rgSeesMadamCleoPg172 = datetime.datetime(year=1927, month=6, day=10,
                                   hour=4, minute=35,
                                   tzinfo=eastern)

# Telegram from Mr. K to RG says Mr. K is leaving Texarkana on the
# Sunshine Special tonight [Friday June 10, 1927], to arrive at
# St. Louis Saturday morning [June 11, 1927].
#
# [using sunset.]
# pg. 179.
mrKLeavingOnSunshineSpecialPg179 = datetime.datetime(year=1927, month=6, day=10,
                                   hour=19, minute=20,
                                   tzinfo=eastern)


# Mr. K arrival in St. Louis Saturday morning [June 11, 1927].
# 'Sometime in the morning'.
# [using sunrise].  
# pg. 179, 163.
mrKStLouisArrivalPg179 = datetime.datetime(year=1927, month=6, day=11,
                                   hour=4, minute=30,
                                   tzinfo=eastern)


# Mr. K arrived and RG met him at Union Station in St. Louis.
# Only an hour to wait.
# RG ready to leave immediately for NY.  [pg. 179].
# On train to NY, they talked of RG's plans. [pg. 181]
# RG is doer. RG must work for joy.  [pg. 181]
#
# [using 1 hour after sunrise].
# pg. 180-181.
mrKAndRgAtUnionStationStLouisCandidate1Pg180 = datetime.datetime(year=1927, month=6, day=11,
                                   hour=5, minute=30,
                                   tzinfo=eastern)
mrKAndRgAtUnionStationStLouisCandidate2Pg180 = datetime.datetime(year=1927, month=6, day=11,
                                   hour=10, minute=0,
                                   tzinfo=eastern)


# RG first arrival in NYC with Mr. K, met by train by Walter.
# Afternoon of June 12, [1927].
# After arrival they went to Hotel Vanderbilt.  RG and Walter to chat alone. [pg. 185.]
# [using 4 pm.]
# pg. 184-185.
rgFirstArrivalNYCPg184 = datetime.datetime(year=1927, month=6, day=12,
                                      hour=16, minute=0,
                                      tzinfo=eastern)

# Mr. K returned to hotel and after dinner told RG he wanted to have a
# confidential chat with his son, Walter.  RG decided to go ut for a
# walk and see the city.  When they were alone, Walter and his father
# had a long talk with Robert.  Help RG get interested in his work so
# that he will forget about Marie.  Love is the greatest thing in the
# world.
# [using sunset]
# pg. 186
mrKAndWalterTalkAboutRGPg186 = datetime.datetime(year=1927, month=6, day=12,
                                      hour=19, minute=25,
                                      tzinfo=eastern)

# Lindbergh triumphant march up Broadway.
# 'Arose early'.  Monday, June 13, [1927].
# Great day for Lindbergh, and great day for RG,
# because it encouraged his hope for the day.
# [using sunrise]
# pg. 187
lindberghMarchUpBroadwayPg187 = datetime.datetime(year=1927, month=6, day=13,
                                      hour=4, minute=30,
                                      tzinfo=eastern)

# OneForAllPlay.  That night.  
# [using sunset].
# pg. 187
oneForAllPlayPg187 = datetime.datetime(year=1927, month=6, day=13,
                                      hour=19, minute=20,
                                      tzinfo=eastern)

# Time Factor Discovery.
# pg. 197.
timeFactorDiscoveryPg197 = datetime.datetime(year=1927, month=6, day=19,
                                      hour=12, minute=0,
                                      tzinfo=eastern)

# Major Motors: Pyramid, start an advance.
# pg. 197.
majorMotorsPyramidPg197 = datetime.datetime(year=1927, month=6, day=30,
                                 hour=12, minute=0,
                                 tzinfo=eastern)

# 69 Wall Street.
# [using noon].
# pg. 217.
wallStreet69Pg217 = datetime.datetime(year=1927, month=7, day=16,
                                 hour=12, minute=0,
                                 tzinfo=eastern)

# 1928 Presidential Election Forecast.
# [using noon.]
# pg. 218.
presElectionForecastPg218 = datetime.datetime(year=1927, month=7, day=20,
                                 hour=12, minute=0,
                                 tzinfo=eastern)

# Just before christmas.
# pg. 222
# [Using 1927-12-24]
justBeforeChristmasPg222 = datetime.datetime(year=1927, month=12, day=24,
                                             hour=12, minute=0,
                                             tzinfo=eastern)

# A few days before Christmas 1927.
# pg. 223
# [Using 1927-12-21, which is 441 CD from 1926-10-06 and 361 CD from 1926-10-23]
aFewDaysBeforeChristmasPg223 = datetime.datetime(year=1927, month=12, day=21,
                                                 hour=12, minute=0,
                                                 tzinfo=eastern)

# Mother to see RG in NY soon after the new year.
# Sights of the city, good for health.
# Soon after the new year.
# [WARNING: Unsure of actual date.]
motherInNYPg224 = datetime.datetime(year=1928, month=1, day=3,
                                    hour=12, minute=0,
                                    tzinfo=eastern)


# RG birthday.  1928.
rgBirthday1928 = datetime.datetime(year=1928, month=6, day=9,
                                   hour=12, minute=0,
                                   tzinfo=eastern)

# RG flight to Paris.
rgFlightToParisPg240 = datetime.datetime(year=1929, month=2, day=2,
                                   hour=18, minute=0,
                                   tzinfo=eastern)

# Robert Gordon and Lady Bersford in Sebring.  [pg. 267]
# March 27, [1929].
rgLadyBersfordInSebringPg267 = datetime.datetime(year=1929, month=3, day=27,
                                    hour=12, minute=0,
                                    tzinfo=eastern)

# RG birthday dinner and celebration.  1929.
rgBirthday1929 = datetime.datetime(year=1929, month=6, day=9,
                                   hour=12, minute=0,
                                   tzinfo=eastern)

# Marriage of Walter and Edna
walterEdnaMarriage = datetime.datetime(year=1929, month=6, day=24,
                                       hour=12, minute=0,
                                       tzinfo=eastern)

# Los Angeles battle: "In the middle of May" [pg. 279].
# LA surrendered on June 14.
losAngeles = datetime.datetime(year=1930, month=5, day=14,
                               hour=12, minute=0,
                               tzinfo=eastern)

# Attack on St. Louis started.
# Early part of August 1931.
# [WARNING: unknown exact date.  Using August 8, 1931.]
attackOnStLouisStartedPg315 = datetime.datetime(year=1931, month=8, day=8,
                                      hour=12, minute=0,
                                      tzinfo=eastern)

# France first attack on England and Germany. [pg. 318].
franceAttackOnEnglandGermany1_Pg318 = datetime.datetime(year=1931, month=9, day=6,
                                      hour=12, minute=0,
                                      tzinfo=eastern)


# Chicago. White flag.  [pg. 320, 322]
# October 3, [1931], 10 a.m.  Sun rose.  
chicagoWhiteFlag_10am_Pg322 = datetime.datetime(year=1931, month=10, day=3,
                                          hour=10, minute=0,
                                          tzinfo=eastern)

# Detroit #1.  Radium Ray.  [pg. 345]
# November 24, [1931], Just before 10 o'clock [pm].
detroit1_RadiumRay_10pm_Pg345 = datetime.datetime(year=1931, month=11, day=24,
                                          hour=22, minute=0,
                                          tzinfo=eastern)

# Detroit #1.   [pg. 347-348]
# November 24, [1931] night, waiting till after 12 o'clock [am], which would actually be November 25, 1931.
detroit1_12am_Pg347 = datetime.datetime(year=1931, month=11, day=25,
                                          hour=0, minute=0,
                                          tzinfo=eastern)

# Detroit #2.   [pg. 349]
# December 7, 1931, 3 o'clock in afternoon. 
detroit2_3pm_Pg349 = datetime.datetime(year=1931, month=12, day=7,
                                          hour=15, minute=0,
                                          tzinfo=eastern)

# Detroit #2.   [pg. 350]
# December 7, 1931, About 5 o'clock. 
detroit2_5pm_Pg350 = datetime.datetime(year=1931, month=12, day=7,
                                          hour=17, minute=0,
                                          tzinfo=eastern)

# Detroit #2.   [pg. 352]
# December 8, 1931, morning.  Newspapers thruout the US carried big headlines.
# Fact of turn of war.  
detroit2_5pm_Pg350 = datetime.datetime(year=1931, month=12, day=7,
                                          hour=17, minute=0,
                                          tzinfo=eastern)


# MAM motor.  pg. 353.
mamMotorPg353 = datetime.datetime(year=1931, month=12, day=25,
                                      hour=12, minute=0,
                                      tzinfo=eastern)

# MAM first flight.  pg. 354.
mamFirstFlightPg354 = datetime.datetime(year=1932, month=1, day=1,
                                      hour=12, minute=0,
                                      tzinfo=eastern)

# France again attacks England and Germany. [pg. 357].
franceAttackOnEnglandGermany2_Pg357 = datetime.datetime(year=1932, month=4, day=1,
                                      hour=12, minute=0,
                                      tzinfo=eastern)

# Battle of Boston.  [pg. 358]
# June 6th [1932].
battleOfBostonPg358 = datetime.datetime(year=1932, month=6, day=6,
                                        hour=12, minute=0,
                                        tzinfo=eastern)

# New York City.  [pg. 361-365]
# 8 o'clock on the evening of June 8th, [1932].  [pg. 361]
nycGiganticAttack_8pm_Pg361 = datetime.datetime(year=1932, month=6, day=8,
                                      hour=20, minute=0,
                                      tzinfo=eastern)
# Combined attack at 10 o'clock that night. [June 8, 1932].  [pg. 361]
nycGiganticAttack_10pm_Pg361 = datetime.datetime(year=1932, month=6, day=8,
                                      hour=22, minute=0,
                                      tzinfo=eastern)
# About 10 minutes after 10 o'clock. [June 8, 1932].  [pg. 362]
nycGiganticAttack_1010pm_Pg362 = datetime.datetime(year=1932, month=6, day=8,
                                      hour=22, minute=10,
                                      tzinfo=eastern)
# About 12 o'clock. [June 9, 1932].  [pg. 365.]
# Triangle form.
nycGiganticAttack_12am_Pg365 = datetime.datetime(year=1932, month=6, day=9,
                                      hour=0, minute=0,
                                      tzinfo=eastern)

# At 12:30 [am., June 9, 1932].  [gp. 366].
nycGiganticAttack_1230am_Pg366 = datetime.datetime(year=1932, month=6, day=9,
                                      hour=0, minute=30,
                                      tzinfo=eastern)

# President lands on Mammouth Building in NY. [pg. 375.]
# About 4 am.
presidentOnMammouthBuilding_4am_Pg375 = datetime.datetime(year=1932, month=6, day=9,
                                      hour=4, minute=0,
                                      tzinfo=eastern)



# RG birthday.  1932.
rgBirthday1932 = datetime.datetime(year=1932, month=6, day=9,
                                   hour=12, minute=0,
                                   tzinfo=eastern)

# Colonel Edna Kennelworth went to Washington. [pg. 383]
# July 2, [1932]
colonelEdnaKennelworthInWashingtonPg383 = datetime.datetime(year=1932, month=7, day=2,
                                    hour=12, minute=0,
                                    tzinfo=eastern)

# Battle of Washington [pg. 383].
# July 4, [1932].
battleOfWashingtonPg383 = datetime.datetime(year=1932, month=7, day=4,
                                    hour=12, minute=0,
                                    tzinfo=eastern)

# RG's 7 days: SCG sailed away in the MAM.  [pg. 393]
# 7 a.m. on July 21st [1932].
rgSevenDays_7am_Pg393 = datetime.datetime(year=1932, month=7, day=21,
                                    hour=7, minute=0,
                                    tzinfo=eastern)

# RG's 7 days: In a little over 3 hours, he was over London.  [pg. 393-394]
# Exact time not given, but using math it would be:
# [10:00 a.m. on July 21st 1932].
rgSevenDays_10am_Pg393 = datetime.datetime(year=1932, month=7, day=21,
                                    hour=10, minute=0,
                                    tzinfo=eastern)

# All cities of in the world where SCG had destroyed buildings were heard from.
# [pg. 403]
# August 4, 1932.
allCitiesInWorldWhereSCGDestroyedBuildingsHeardFromPg403 = datetime.datetime(year=1932, month=8, day=4,
                                    hour=12, minute=0,
                                    tzinfo=eastern)

# Peace Conference [pg. 407]
# About 10 A.M. on August 30th [1932].  The conference convened.
peaceConference_10am_Pg407 = datetime.datetime(year=1932, month=8, day=30,
                                    hour=10, minute=0,
                                    tzinfo=eastern)
# Peace Conference [pg. 407]
# About 11 A.M. on August 30th [1932].  All officials were seated.
# Shortly after, SCG escorted by the President of the US, General Walter Walter Kennelworth and his wife General Edna Kennelworth arrived.
peaceConference_11am_Pg407 = datetime.datetime(year=1932, month=8, day=30,
                                    hour=11, minute=0,
                                    tzinfo=eastern)
# Peace Conference [pg. 415]
# Late in the evening. [August 30, 1932].
# Exact time not given, so using: [7 pm].
peaceConference_lateEvening_Pg415 = datetime.datetime(year=1932, month=8, day=30,
                                    hour=19, minute=0,
                                    tzinfo=eastern)

# Time after discovery of America
# pg. 371.
# October 1932.
timeAfterDiscoveryOfAmerica = datetime.datetime(year=1932, month=10, day=15,
                                                hour=12, minute=0,
                                                tzinfo=eastern)

