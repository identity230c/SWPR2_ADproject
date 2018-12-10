import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QToolButton, QTextEdit, QSlider, QLCDNumber
from PyQt5.QtGui import QPixmap
from Logic import Logic
from matchingCard import domain

class ImageLabel(QLabel):
    # Label이 이미지를 출력할 수 있도록하는 클래스
    def __init__(self, imageName):
        super().__init__()
        pix = QPixmap(imageName)
        self.setPixmap(pix)
        self.resize(pix.width(), pix.height())

class Button(QToolButton):
    # 버튼 클래스
    def __init__(self, name, callback):
        super().__init__()
        self.setText(name)
        self.clicked.connect(callback)

class Graphic(QWidget):
    def __init__(self):
        super().__init__()

        # 게임을 불러옴
        self.game = Logic()

        # 전체 설정
        self.setWindowTitle("BalckJack")
        self.setGeometry(300, 300, 500, 500)
        mainLayout = QGridLayout()

        # 딜러, 플레이어 패 레이아웃 설정
        dealerBar = QLabel()
        dealerBar.setText("Dealer Bar")
        self.dealerLayout = QHBoxLayout()
        self.dealerLayout.addStretch(1)

        playerBar = QLabel()
        playerBar.setText("Player Bar")
        self.playerLayout = QHBoxLayout()
        self.playerLayout.addStretch(1)

        # 메인레이아웃에 배치
        mainLayout.addWidget(dealerBar , 0,0, 1,2)
        mainLayout.addLayout(self.dealerLayout, 1,0, 1,2)
        mainLayout.addWidget(playerBar, 2,0, 1,2)
        mainLayout.addLayout(self.playerLayout, 3,0, 1,2)

        # 상황판 배치
        self.statusBox = QTextEdit()
        self.statusBox.setReadOnly(True)
        self.statusBox.setFixedSize(1200,100)
        mainLayout.addWidget(self.statusBox, 4,0, 1,2)

        # 슬라이더 LCD 배치
        self.poolSlider = QSlider(Qt.Horizontal)
        self.poolSlider.setRange(0, self.game.getMoney())
        self.poolSlider.setSingleStep(1)
        poolLCD = QLCDNumber()
        self.poolSlider.valueChanged.connect(poolLCD.display)
        sliderLayout = QGridLayout()
        sliderLayout.addWidget(self.poolSlider, 1, 0)
        sliderLayout.addWidget(poolLCD, 0, 0)
        mainLayout.addLayout(sliderLayout, 5, 0)

        # 버튼 배치
        buttonLayout = QGridLayout()
        self.raiseButton = Button('Raise', self.raiseEvent)
        self.dieButton = Button('Die', self.dieEvent)
        self.stayButton = Button('Stay', self.stayEvent)
        self.hitButton = Button('Hit', self.hitEvent)
        buttonLayout.addWidget(self.raiseButton, 0,0)
        buttonLayout.addWidget(self.stayButton, 0,1)
        buttonLayout.addWidget(self.dieButton, 1,0)
        buttonLayout.addWidget(self.hitButton, 1,1)
        mainLayout.addLayout(buttonLayout, 5,1)

        # 전체 설정
        self.setLayout(mainLayout)
        self.show()

        # 게임 시작
        self.hitEvent()

    def raiseEvent(self):
        # raise버튼 눌리면 연결

        # setPool호출 -> 건 돈 전달
        self.game.setPool(self.poolSlider.value())

        # draw호출
        ret = self.game.drawCard()

        # 마지막 글자가 D면 21이 넘어가 게임이 끝난 상태
        if ret[-1] == "D":
            # 버튼 종료
            self.buttonSwith(False)

            self.playerLayout.addWidget(ImageLabel(domain(ret[:-1])))
            self.statusBox.setText("21이 넘어갔습니다. \
            \n플레이어 : {}\n딜러 : {}" \
            .format(self.game.playerNum, self.game.dealerNum))

            # 게임이 종료되었는지 확인
            if self.game.remainMoney():
                self.gameOver()
        else:
        # 그렇지 않으면 카드를 화면에 추가
            self.playerLayout.addWidget(ImageLabel(domain(ret)))
            self.poolSlider.setRange(0, self.game.getMoney())
            self.statusBox.setText(self.game.getPlayerStatus() \
            + "\n플레이어 : {}\n딜러 : {}" \
            .format(self.game.playerNum, self.game.dealerNum))

    def dieEvent(self):
        # die버튼 눌리면 연결

        # 버튼부터 끄기
        self.buttonSwith(False)

        # 라운드 정지 판정
        self.statusBox.setText("다이하셨습니다.")
        self.game.die()

        # 돈을 다 잃으면 정지
        if self.game.remainMoney():
            self.gameOver()

    def stayEvent(self):
        # stay버튼 눌리면 연결

        # 판돈 보내기
        self.game.setPool(self.poolSlider.value())

        # endGame 메서드 호출
        result, dealerCards = self.game.endGame()

        # 딜러의 카드 배치
        for card in dealerCards[2:]:
            self.dealerLayout.addWidget(ImageLabel(domain(card)))

        # 결과에 따른 메시지 출력
        if result == 2:
            self.statusBox.setText("블랙잭! 2배로 받습니다.")
        elif result == 1:
            self.statusBox.setText("이기셨습니다. 판돈만큼 받습니다.")
        elif result == 0:
            self.statusBox.setText("비기셨습니다. 돈은 그대로 유지됩니다.")
        else:
            self.statusBox.setText("지셨습니다. 판돈만큼 잃습니다.")
        self.statusBox.append(self.game.getPlayerStatus())

        self.buttonSwith(False)

    def hitEvent(self):
        # hit 버튼 눌리면 연결
        # 카드 패 모두 지우기
        for i in reversed(range(self.dealerLayout.count())):
            try:
                self.dealerLayout.itemAt(i).widget().deleteLater()
            except:
                pass
        for i in reversed(range(self.playerLayout.count())):
            try:
                self.playerLayout.itemAt(i).widget().deleteLater()
            except:
                pass
        # hit 메서드 호출
        cards = self.game.hit()

        # 카드 추가
        self.dealerLayout.addWidget(ImageLabel(domain(cards[0][0])))
        self.dealerLayout.addWidget(ImageLabel(domain(cards[0][1])))
        self.playerLayout.addWidget(ImageLabel(domain(cards[1][0])))
        self.playerLayout.addWidget(ImageLabel(domain(cards[1][1])))

        # 버튼 키기
        self.buttonSwith(True)

        # 상태바 슬라이더 정리
        self.statusBox.setText("게임을 시작합니다.")
        self.statusBox.append(self.game.getPlayerStatus())
        self.poolSlider.setRange(0, self.game.getMoney())

    def gameOver(self):
        # 남은 돈이 없으면 호출
        # 버튼 다 끄기
        self.buttonSwith(False)
        self.hitButton.setEnabled(False)

        self.statusBox.setText("남은 돈이 없습니다.")

    def buttonSwith(self, boolean):
        # 코드 반복 방지를 위한 버튼 키고끄는 메서드
        self.raiseButton.setEnabled(boolean)
        self.dieButton.setEnabled(boolean)
        self.stayButton.setEnabled(boolean)
        self.hitButton.setEnabled(not boolean)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Graphic()
    sys.exit(app.exec_())
