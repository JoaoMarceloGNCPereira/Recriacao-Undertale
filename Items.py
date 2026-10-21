
class Backpack:
    def __init__(self, listItems=[]):
        self.listItems = listItems

    def addItem(self, item):
        self.listItems.append(item)

    def removeItem(self, item):
        self.listItems.remove(item)

    def printList(self):
        for item in self.listItems:
            print(item)


# =======================
#         ITEMS
# =======================

# The durability of an item goes from 0 - 1
# Also, the rarity goes from 0 - 1, and it can be used as a multiplier for the item stats

class Item:
    def __init__(self, name: str, price: int, totalDurability: float, currentDurability: float, rarity: float, description: str):
        self.name = name
        self.price = price
        self.totalDurability = totalDurability
        self.currentDurability = currentDurability
        self.rarity = rarity
        self.description = description

    def printStats(self):
        print(self.name)
        print(self.price)
        print(self.currentDurability, "/", self.totalDurability)
        print(self.rarity)
        print(self.description)


class Potion(Item):
    def __init__(self, name: str, price: int, totalDurability: float, currentDurability: float,
                 rarity: float, description: str, pointsCure: int, pointsStrength: int, pointsDefense: int):
        super().__init__(name, price, totalDurability, currentDurability, rarity, description)
        self.pointsCure = pointsCure
        self.pointsStrength = pointsStrength
        self.pointsDefense = pointsDefense

    def printStats(self):
        super().printStats()
        print(self.pointsCure, "/", self.pointsStrength, "/", self.pointsDefense)




class Weapon(Item):
    def __init__(self, name: str, price: int, totalDurability: float, currentDurability: float,
                 rarity: float, description: str, damageMax: float, damageMin: float,
                 chanceHit: float, chanceCritical: float, damageMultiplier: float):
        super().__init__(name, price, totalDurability, currentDurability, rarity, description)
        self.damageMax = damageMax
        self.damageMin = damageMin
        self.chanceHit = chanceHit
        self.chanceCritical = chanceCritical
        self.damageMultiplier = damageMultiplier

    def printStats(self):
        super().printStats()
        print(self.damageMin, "-", self.damageMax)
        print(self.chanceHit, "-", self.chanceCritical)
        print(self.damageMultiplier)


# ===================
#   Items Creator
# ===================


class ItemsCreator:

    def createItem(self, name: str, price: int, totalDurability: float, currentDurability: float, rarity: float, description: str):
        NewItem = Item(name, price, totalDurability, currentDurability, rarity, description)
        return NewItem


    def createPotion(self, type: str, price: int, rarity: float, pointsCure=0, pointsStrength=0, pointsDefense=0):
        if type.lower() == "healing":
            newPotion = Potion("Potion of Healing", price, 1, 1, rarity,
                               "A formidable drink that heals your wounds", 10, 0, 0)
        elif type.lower() == "strength":
            newPotion = Potion("Potion of Strength", price, 1, 1, rarity,
                               "Somehow you feel stronger after drinking it", 0, 10, 0)
        elif type.lower() == "defense":
            newPotion = Potion("Potion of Defense", price, 1, 1, rarity,
                               "You feel as strong as an armored knight", 0, 0, 10)
        elif type.lower() == "special":
            newPotion = Potion("Special Potion", price, 1, 1, rarity,
                               "It is a mix of all potions", pointsCure, pointsStrength, pointsDefense)
        else:
            newPotion = Potion("Potion of Nothing", price, 1, 1, rarity, "I actually think its just old and plain water", 1, 0, 0)

        return newPotion


    def createSword(self, name: str, price: int, currentDurability: float,
                 rarity: float, description: str, damageMax: float, damageMin: float):
        newSword = Weapon(name, price, 1, currentDurability, rarity, description,
                        damageMax, damageMin, chanceHit=0.9, chanceCritical=0.1, damageMultiplier=2)
        return newSword

    def createBow(self, name: str, price: int, currentDurability: float,
                 rarity: float, description: str, damageMax: float, damageMin: float):
        newBow = Weapon(name, price, 1, currentDurability, rarity, description,
                        damageMax, damageMin, chanceHit=0.7, chanceCritical=0.2, damageMultiplier=3)
        return newBow


    def createMagicStaff(self, name: str, price: int, currentDurability: float,
                 rarity: float, description: str, damageMax: float, damageMin: float):
        newBow = Weapon(name, price, 1, currentDurability, rarity, description,
                        damageMax, damageMin, chanceHit=0.8, chanceCritical=0.5, damageMultiplier=1.5)
        return newBow


item_creator = ItemsCreator()
espada = item_creator.createSword("espada dos macho", 12, 1, 1, "espada boa demaizi", 20, 10)
espada.printStats()

pocao = item_creator.createPotion("healing", 11, 1)
item = item_creator.createItem("jujubas", 11, 1, 1, 1, "boas")

backback = Backpack()
backback.addItem(item)
backback.addItem(pocao)
backback.addItem(espada)
for i in backback.listItems:
    i.printStats()