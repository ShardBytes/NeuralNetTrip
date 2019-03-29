def je_mozna_stavba(pocetKociek):
    if(pocetKociek < 2):
        return False
        
    pouzitekocky = 0
    poschodie = 1
    while(pocetKociek != pouzitekocky):
        pouzitekocky += poschodie * 2
        poschodie += 1

        if pouzitekocky > pocetKociek:
            return False

    return True

for i in range(0, 50):
    print("S ", i, " kockami: ", je_mozna_stavba(i))
