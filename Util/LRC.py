from Util.Log import Logger
from Util.SerialComm import send_serial


def calLRC(self, txt):
    self.txt = txt
    print('전송받은 데이터:' + self.txt)
    sum = 0
    # 시리얼 통신 전송값 초기화
    data = []
    # 선두문자 ':'
    data.append(0x3A)
    # 입력값 프레임 단위로 나누어 더하기 (Dec)
    for i in range(len(self.txt)):
        # 입력값 아스키코드로 변환하여 리스트에 추가
        data.append(ord(self.txt[i]))
        # LRC 구하기 위한 과정
        if i % 2 == 0:
            sum = sum + int(self.txt[i:i + 2], 16)
    # LRC 구하기 과정 - XOR
    xorSum = bin(0b11111111 ^ sum)
    # print(xorSum)
    lrc = format(int(xorSum, 2) + 1, 'X')
    # LRC 마지막 두글자만 허용
    lrcstr = lrc[-2]+lrc[-1]
    print('lrc:' + lrcstr)
    # LRC 아스키코드로 변환하여 리스트 추가
    data.append(ord(lrc[-2]))
    data.append(ord(lrc[-1]))
    # 송신창에 나타날 최종 코드
    result = ':' + txt + lrcstr + '[CR][LF]'
    print(result)
    # 종단문자 리스트에 추가
    data.append(0x0D)
    data.append(0x0A)
    print(data)
    # 입력데이터 송신
    send_serial(data)
    if self.saveBtn.isChecked():
        Logger.info('Tx : '+result)
    return result