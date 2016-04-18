#!/usr/bin/python
#coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

pathCai = "emotions_xiaotingcai.csv"
pathShen = "emotions_xuanshen.csv"
pathTian = "emotions_boyangtian.csv"
pathYe = "emotions_qiuyangye.csv"

inputCai = open(pathCai, 'r')
inputShen = open(pathShen, 'r')
inputTian = open(pathTian, 'r')
inputYe = open(pathYe, 'r')
diffFile = open('emotion_diff.txt', 'w+')

# insert each line into list
rowsCai=tuple(inputCai)
rowsShen=tuple(inputShen)
rowsTian=tuple(inputTian)
rowsYe=tuple(inputYe)
# close input file
inputCai.close()
inputShen.close()
inputTian.close()
inputYe.close()

same_dict={}
same_dict['positive']=[]
same_dict['negative']=[]
same_dict['neutral']=[]
# shen and cai
for i in range(1, 400):
	textCai=rowsCai[i].rstrip().split(',')
	textShen=rowsShen[i].rstrip().split(',')
	if not textCai[3]==textShen[3]:
		result=textCai[0]+','+textCai[3]+','+textShen[3]+'\n'
		diffFile.write(result)
	# same classification
	else:
		if textCai[3]=='positive':
			same_dict['positive'].append(textCai[0]+','+textCai[3])
		elif textCai[3]=='negative':
			same_dict['negative'].append(textCai[0]+','+textCai[3])
		else:
			same_dict['neutral'].append(textCai[0]+','+textCai[3])		
# tian and ye		
for i in range(400, 816):
	textTian=rowsTian[i].rstrip().split(',')
	textYe=rowsYe[i].rstrip().split(',')
	if not textTian[3]==textYe[3]:
		result=textTian[0]+','+textTian[3]+','+textYe[3]+'\n'
		diffFile.write(result)
	# same classification		
	else:
		if textCai[3]=='positive':
			same_dict['positive'].append(textTian[0]+','+textTian[3])
		elif textCai[3]=='negative':
			same_dict['negative'].append(textTian[0]+','+textTian[3])
		else:
			same_dict['neutral'].append(textTian[0]+','+textTian[3])
for key in same_dict:
	print key + '\n'
	print u'\n'.join(same_dict[key])				
diffFile.close()		



