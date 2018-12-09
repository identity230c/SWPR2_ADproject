# 카드 리스트를 호출하고, 이미지와 매칭시키기 위한 함수 정의하는 모듈

listOfCard = []
for s in ['spades', 'heart', 'club', 'diamond']:
    for i in 'A23456789JQK':
        tmp = s + i
        listOfCard.append(tmp)
    tmp = s + "10"
    listOfCard.append(tmp)

# 이미지 - 카드리스트를 연결하는 함수
domain = lambda x : "CardImage/" + x + ".png"