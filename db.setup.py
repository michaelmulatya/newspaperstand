from core.models import Admin, Orders, Products, ProductLevel, ProductView, Users
from core import db
from datetime import datetime

db.create_all()
print('All tables created')

admin = Admin('Nur', 'Mohsin', 'mohsin@gmail.com', '01677876551', 'Dhaka', '$5$rounds=535000$w/MRBgS3SCDxMfkt$q.6o0T3/bF6wpch9ErkAuvOItlJeWq/hw5zgpEBOiY0', 'manager', '0');

db.session.add(admin)
db.session.commit()
print('Admin Created')
time = str(datetime(2012, 3, 3, 10, 10, 10))
print(time)
one = Orders(1, 'Kashmiri Chador', 1,'01609876543', 'mohsin@gmail.com','2018-09-22 03:03:36')
two = Orders(2, 'Kashmiri Chador', 1,'01609876543', 'mohsin@gmail.com','2018-09-22 03:03:36')
three = Orders(3, 'Kashmiri Chador', 1,'01609876543', 'mohsin@gmail.com','2018-09-22 03:03:36')
four = Orders(4, 'Kashmiri Chador', 1,'01609876543', 'mohsin@gmail.com','2018-09-22 03:03:36')
five = Orders(5, 'Kashmiri Chador', 1,'01609876543', 'mohsin@gmail.com','2018-09-22 03:03:36')
six = Orders(6, 'Kashmiri Chador', 1,'01609876543', 'mohsin@gmail.com','2018-09-22 03:03:36')
seven = Orders(7, 'Kashmiri Chador', 1,'01609876543', 'mohsin@gmail.com','2018-09-22 03:03:36')
eight = Orders(8, 'Kashmiri Chador', 1,'01609876543', 'mohsin@gmail.com','2018-09-22 03:03:36')
nine = Orders(9, 'Kashmiri Chador', 1,'01609876543', 'mohsin@gmail.com','2018-09-22 03:03:36')
ten = Orders(10, 'Kashmiri Chador', 1,'01609876543', 'mohsin@gmail.com','2018-09-22 03:03:36')

db.session.add_all([one, two, three, four, five, six, seven, eight, nine, ten])
db.session.commit()
print('Orders created')


# one = Products("Top Gear","FEB,2019",100,"Most wanted! 19 must have cars of 2019","United Kingdom","magazines","BBC","1st","BBC_Top_Gear_February2019_ UK.jpg","https://drive.google.com/open?id=1-viCrN_Hz--bTQZ5PEQOkCQTWB-HSTto")
# two = Products("Cosmopolitan",'MAR 2019',100,"Are our men in pain? , style Army","United Kingdom","magazines","Cosmopolitan-UK","1st","Cosmopolitan_March2019_ UK.jpg","https://drive.google.com/open?id=1JjvU0cB3TkqVl2upKatIPqG6s0o6eaz1")
# three = Products("Golf Digest",'MAR 2019',100,"School of Butch The best lessons of his life","USA","magazines","Golf Digest","1st","Golf_Digest_March_2019_USA.jpg","https://drive.google.com/open?id=1SIXwqCWN0HXkVt1pDUcO-GqBeMeiMo4K")
# four = Products("Mens Fitness","FEB 2019",100,"Change your Life in 2019","Australia","magazines","Mensfitnessmagazine.com","1st","MensFitness_February2019_AU.jpg","https://drive.google.com/open?id=1Yb6_rCMnG_6iIQmK5QtLF_btZljD4zVp")
# five = Products("SFX",'MAR 2019',100,"Marvel Past present and future","USA","magazines","sfx","1st","SFX_March_2019_UK.jpg","https://drive.google.com/open?id=17suk5SiToKHzbPFFj4GNRXolC67CGHBG")
# six = Products("Skin Deep",'MAR 2019',100,"The UK's Biggest and Best Selling Tattoo Magazine","United Kingdom","magazines","SKIN DEEP","1st","SkinDeep_March_2019_UK.jpg","https://drive.google.com/open?id=1nAMXapoumibLDIaGBgzl2HRg9-OcgW5S")
# seven = Products("Total Tattoos",'FEB 2019',100,"World Tattoo Industry Trade Show","United Kingdom","magazines","www.totaltattoo.co.uk","1st","TotalTattoo_February_2019_UK.jpg","https://drive.google.com/open?id=13KK3r4-iYM3V9G_7zTuVnMX28OzzOX6k")
# eight = Products("Wall Street Journal",'27-Jan-2019',100,"Three week Deal Halts Shutdown","USA","newspapers","wall street journal","1st","wallstreetjournal_20190126_TheWallStreetJournal.jpg","https://drive.google.com/open?id=1Z2FrrstrhwZNApZwQyfpm9MsHI1lwjDt")
# nine = Products("Wall Street Journal",'30-Jan-2019',100,"US Officials cite Alignment of Moscow, Beijing as threat","USA","newspapers","wall street journal","1st","wallstreetjournal_20190130_TheWallStreetJournal.jpg","https://drive.google.com/open?id=1EdGZB6p17pk38WZjoo4XNa84PyfD3I6F")
# ten = Products("Wall Street Journal",'31-Jan-2019',100,"Fed Signals Hold on Rate Increases","USA","newspapers","wall street Journal","1st","wallstreetjournal_20190131_TheWallStreetJournal.jpg","https://drive.google.com/open?id=1R9YhQl_RDff1hQWhTUUegeLpk0eOV-bp")
# eleven = Products("Wall Street Jornal Magazine",'Jan 2019',100,"Talents & Legends","USA","textbooks","wall street journal","1st","wallstreetjournalmag_20190119_TheWallStreetJournalMagazine.jpg","https://drive.google.com/open?id=1t48ce5JBwc-kKDTByai0wFpEtyJKK90F")
# twelve = Products("Bike","MAR 2019",100,"Britain Best selling Bike Magazine","United Kingdom","magazines","Bike Magazine","1st","Bike_March_2019.jpg","https://drive.google.com/open?id=1-viCrN_Hz--bTQZ5PEQOkCQTWB-HSTto")
# thirteen = Products("HackSpace","FEB 2019",100,"HackSpace magazine is the new monthly magazine for people who love to make things and those who want to learn.","USA","comics","https://hackspace.raspberrypi.org/","1st","HackSpace_February2019UK.jpg","https://drive.google.com/open?id=1-viCrN_Hz--bTQZ5PEQOkCQTWB-HSTto")
# fourteen = Products("Motor Trend",'MAR 2019',100,"2020 Supra The Legend returns with a Teutonic Twist","USA","magazines","Motor trend  ","1st","MotorTrend_March2019USA.jpg","https://drive.google.com/open?id=1-viCrN_Hz--bTQZ5PEQOkCQTWB-HSTto")
# fifteen = Products("Music Tech",'FEB 2019',100,"70  pro tips to improve your tracks today","United Kingdom","textbooks","musichtech","1st","MusicTech_February2019_ UK.jpg","https://drive.google.com/open?id=1-viCrN_Hz--bTQZ5PEQOkCQTWB-HSTto")
# sixteen = Products("OK Magazine",'FEB 2019',100,"Kourt's New diet","Australia","comics","OKMagazine","1st","OK!Magazine_February2019_ AU.jpg","https://drive.google.com/open?id=1-viCrN_Hz--bTQZ5PEQOkCQTWB-HSTto")
# seventeen = Products("OK Magazine",'FEB 2019',100,"Sandra's Miracle baby at 54","USA","magazines","OKmagazine","1st","OK!Magazine_February_2019_USA.jpg","https://drive.google.com/open?id=1-viCrN_Hz--bTQZ5PEQOkCQTWB-HSTto")
# eighteen = Products("The Economist",'JAN 2019',100,"Slowbalisation, the future of global commerce","USA","newspapers","theconomist","1st","The Economist_January_2019_ UK.jpg","https://drive.google.com/open?id=1-viCrN_Hz--bTQZ5PEQOkCQTWB-HSTto")
#
#
# db.session.add_all([one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen])
# db.session.commit()
# print('Products created')


one = ProductLevel(1, 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no')
two = ProductLevel(2, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no')
three = ProductLevel(3, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes')
four = ProductLevel(4, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no')
five = ProductLevel(5, 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no')
six = ProductLevel(6, 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no')
seven = ProductLevel(7, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no')
eight = ProductLevel(8, 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no')
nine = ProductLevel(9, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no')
ten = ProductLevel(10, 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no')
eleven = ProductLevel(14, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no')
twelve = ProductLevel(12, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no')
thirteen = ProductLevel(13, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes')
fourteen = ProductLevel(15, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no')
fifteen = ProductLevel(16, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'no')
sixteen = ProductLevel(17, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no')
seventeen = ProductLevel(18, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no')
eighteen = ProductLevel(19, 'no', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no')
nineteen = ProductLevel(20, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no')
twenty = ProductLevel(21, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'no')

db.session.add_all([one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen,
                    fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty])
db.session.commit()
print('product levels created')


one = ProductView(9, 9, '2018-09-22 02:19:30')
two = ProductView(9, 7, '2018-09-27 02:47:43')
three = ProductView(9, 12, '2018-09-22 03:20:59')
four = ProductView(9, 10, '2018-09-29 03:07:11')
five = ProductView(9, 5, '2018-09-22 03:19:19')
six = ProductView(9, 8, '2018-09-21 15:57:50')
seven = ProductView(9, 6, '2018-09-22 02:12:54')
eight = ProductView(9, 1, '2018-09-22 03:03:36')

db.session.add_all([one, two, three, four, five, six, seven, eight])
db.session.commit()

print('product view data populated')


one = Users('Mukul', 'mukul@gmail.com', 'mukul',
            '$5$rounds=535000$6PJhbzFlfJbcQbza$FbrPa3qqk1RJ5MSffRLO6LrQJXbgO8SudFuBpNf.wR7', '', '2018-07-23 14:09:14', '0', 'yes')
two = Users('Nur Mohsin', 'mohsin@gmail.com', 'mohsin', '$5$rounds=535000$EnLkwqfGWGcWklRL$q9PbYw/TVXSzs.QpgUouZ3.6BzaPG2eLHkTyv.Qx80D', '123456789022', '2018-07-21 06:47:57', '1', 'yes')
three = Users('Nur Mohsin', 'khan@gmail.com', 'khan', '$5$rounds=535000$wLKTQexvPQHueUsK$aFrFUXBHjrrAH61EFiYgj8cZECaaz8y6S5XS/zkkHw9', '', '2018-09-07 09:02:35', '0', 'yes')
four = Users('Robin', 'robin@gmail.com', 'robin', '$5$rounds=535000$uiZc/VCwwa3XCTTe$Ec.JOjy4GkjpAXHtAvGt6pSc6KszajHgcyZy8v6Ivk1', '', '2018-07-26 12:36:57', '0', 'yes')
five = Users('Sujon', 'sujon@yahoo.com', 'sujons', '$5$rounds=535000$aGykDT1yrocgTaDt$p2dDAMDz9g3N6o/Jj7QJY9B6NnMlUot.DCq/LOsCS13', '89345793753', '2018-09-08 13:58:36', '0', 'yes')

db.session.add_all([one, two, three, four, five])
db.session.commit()
print( ' Users created')