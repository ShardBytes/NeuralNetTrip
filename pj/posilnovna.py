skrinky = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False] #15 prázdnych skriniek

def vrat_cislo_skrinky():
    if (not skrinky[0]): #začiatok/koniec keď je voľno
        skrinky[0] = True
        return 0
    elif (not skrinky[len(skrinky) - 1]):
        skrinky[len(skrinky) - 1] = True
        return len(skrinky) - 1
    else:
        firstrememberindex = -1
        lastrememberindex = len(skrinky) - 2

        for i in range(1, len(skrinky) - 1):
            if not skrinky[i]:
                firstrememberindex = i
                break

        for i in range(1, len(skrinky) - 1):
            if skrinky[i]:
                lastrememberindex = i
                break

        if(firstrememberindex > lastrememberindex):
            return None #došli skrinky
        else:
            emptylocker = int((firstrememberindex + lastrememberindex) / 2)
            skrinky[emptylocker] = True
            return emptylocker



print(vrat_cislo_skrinky())
print(vrat_cislo_skrinky())
print(vrat_cislo_skrinky())
print(vrat_cislo_skrinky())
print(vrat_cislo_skrinky())
print(vrat_cislo_skrinky())
print(vrat_cislo_skrinky())
 #vráti None, keď nie je dostupná skrinka
 #unfinished, but no time
