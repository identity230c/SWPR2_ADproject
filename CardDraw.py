# 카드를 뽑는 모듈

from random import choice
from matchingCard import listOfCard

class CardDraw:
    def __init__(self):
        self.deckReset()

    def deckReset(self):
        self.cardList = listOfCard[:]

    def chooseCard(self):
        ret = choice(self.cardList)
        self.cardList.remove(ret)
        return ret