# Player Class

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.properties = []
        self.location = 0
        self.numDoubles = 0
        self.jail = False
        self.jailFreeCard = False
        self.jailRolls = 0
        self.inGame = True

    def canPay(self,amount):
        """ Verifies whether player can pay fee charged """

        hasProperties = (len(self.properties) != 0)

        if(self.money > amount):
            print(f"{self.name} paid {amount}")
            self.money -= amount
            return True
        elif(hasProperties):
            # Check whether any properties are not mortgaged in order to obtain funds
            # for prop in self.properties:
            pass
        # else:
            # print(f"Game Over for {p.name}")
            # p.inGame = False

