from csv import *
import numpy as np
import matplotlib.pyplot as plt

## matrix structure ##
##              0    1    2
##              good soso bad
## 0 = index[0] 5    7    8
## 1 = index[1] 3    2    10
## 2 = index[2] 4    2    32
## 3 = index[3] 3    12   1
## 


plt.rcParams['font.family'] ='AppleGothic'
plt.rcParams['axes.unicode_minus'] =False

def transpose(m):
    row = len(m)
    col = len(m[0])
    mt = [[0]*row for i in range(col)]
    for i in range(row):
        for j in range(col):
            mt[j][i] = m[i][j]
    return(mt)


with open("선곡.csv", 'r', encoding="utf-8") as work:
    rdr = reader(work)
    for i, line in enumerate(rdr):
        if i == 0:
            index = line[2:]
            numberofRow = len(line)
            m = [[0,0,0] for i in range(numberofRow-2)]
        else:
            for j, word in enumerate(line):
                if j == 0 or j ==  1:
                    continue
                assert word != '', "입력되지 않은 항목이 존재합니다"

                if word == 'good':
                    m[j-2][0] += 1
                elif word == 'soso':
                    m[j-2][1] += 1
                elif word == 'bad':
                    m[j-2][2] += 1
    mTransed = transpose(m)

y = np.arange(len(index))  # 레이블 위치
width = 0.25  # 막대의 너비

# 막대 그래프 그리기
fig, ax = plt.subplots()
rects1 = ax.barh(y + width, mTransed[0], width, label='good', color='green')
rects2 = ax.barh(y, mTransed[1], width, label='soso',color='orange')
rects3 = ax.barh(y - width, mTransed[2], width, label='bad',color='red')

# 그래프 제목 및 라벨 설정
ax.set_title('선곡 결과')
ax.set_ylabel('노래')
ax.set_xlabel('Values')
ax.set_yticks(y)
ax.set_yticklabels(index)
ax.legend()

# 그래프 표시
plt.show()
