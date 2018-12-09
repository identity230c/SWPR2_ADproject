from CardDraw import CardDraw

class Logic:
    def __init__(self):
        self.playerCard = []
        self.dealerCard = []
        self.playerNum = 0
        self.dealerNum = 0
        self.playerMoney = 100
        self.pool = 0
        self.deck = CardDraw()

    def drawCard(self):
        # 플레이어의 카드를 뽑는 메서드

        # 카드를 뽑고
        newCard = self.deck.chooseCard()
        self.playerCard.append(newCard)

        # 계산
        self.playerNum = self.cardSum(self.playerCard)

        # 죽으면 die
        if self.playerNum > 21:
            # 죽었다는 것을 알리기위해 "D"를 붙임
            newCard = newCard + "D"
            self.die()

        # 리턴
        return newCard

    def cardSum(self, cardList):
        sum = 0
        for i in cardList:
            if i[-1] in ['0', 'J', 'Q', 'K']:
                sum += 10
            elif i[-1].isdigit():
                sum += int(i[-1])
            elif i[-1] == 'A':
                sum += 1
        return sum

    def die(self):
        # 판돈 만큼 플레이어 돈 빼기
        self.playerMoney -= self.pool
        self.pool = 0

    def setPool(self, pool):
        self.pool = pool

    def endGame(self):
        # 딜러의 카드 뽑기 여부를 결정

        self.dealerNum = self.cardSum(self.dealerCard)

        # while 딜러 카드가 16 이하
        if self.dealerNum <= 16:
            # 딜러 카드 뽑기
            newCard = self.deck.chooseCard()
            self.dealerCard.append(newCard)
            self.dealerNum += self.cardSum([newCard])

        # 딜러와 플레이어 카드 비교
            # 플레이어가 블랙잭이면 플레이어 2배
            # 플레이어가 지면 건 만큼 돈을 잃고 이기면 건 만큼 돈을 얻음
            # 무승부면 돈은 그대로
        result = 0
        if self.playerNum == 21:
            result = 2
            self.playerMoney += self.pool*2
        elif self.dealerNum > 21 or self.playerNum > self.dealerNum:
            result = 1
            self.playerMoney += self.pool
        elif self.playerNum < self.dealerNum:
            result = -1
            self.playerMoney -= self.pool

        # 판돈 초기화
        self.pool = 0

        # 결과 반환
        return (result, self.dealerCard)

    def hit(self):
        # 게임을 새로 시작했으니 카드 리스트 초기화
        self.deck.deckReset()

        # 딜러카드 2개 뽑기
        # 플레이어 카드 2개 뽑기
        # playernum과 Card 갱신(dealer도 마찬가지)
        self.dealerCard = []
        self.playerCard = []
        self.playerNum = 0
        self.dealerNum = 0
        for i in range(2):
            self.dealerCard.append(self.deck.chooseCard())
            self.playerCard.append(self.deck.chooseCard())

        self.playerNum += self.cardSum(self.playerCard)
        self.dealerNum += self.cardSum(self.dealerCard)

        # 딜러의 카드 2개 / 플레이어 카드 2개 리턴(순서쌍이나 리스트)
        dealerPLayerCards = ([self.dealerCard, self.playerCard])
        return dealerPLayerCards

    def getPlayerStatus(self):
        status = "플레이어의 돈 = {}\n배팅한    돈 = {}".format(self.playerMoney, self.pool)
        return status

    def setPool(self, pool):
        self.pool += pool

    def getMoney(self):
        return self.playerMoney - self.pool

    def remainMoney(self):
        return not self.playerMoney > 0
