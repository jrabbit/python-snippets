import time
daynum=int(time.strftime('%j'))
year=int(time.strftime('%y'))
composite=(year*365)+daynum
def ordinal(n):
     if 10 <= n % 100 < 20:
         return str(n) + 'th'
     else:
        return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")
    #thanks http://stackoverflow.com/questions/739241/python-date-ordinal-output/739301#739301
print "It is the %s day since President Bush declared mission accomplished in Iraq, \
the %s day since he declared victory in the Afghanistan, \
and %s day of the Deepwater Horizon disaster in the Gulf."% (ordinal(composite - 1214), ordinal(composite - 1625), ordinal(composite - 3759))
#Composite dates - date of occurance for July 8th -- 2625 Iraq 2214 Afg 80 Oil
