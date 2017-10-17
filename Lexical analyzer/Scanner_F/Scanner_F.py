# -*- coding: utf-8 -*-

'''
author: Wang Meng
shcool: SWPU
date: 17/10/2017
DFA by Python
'''''

import math

class DFA:

    Token_Type = [                      #记号的类别
        'ORIGIN','SCALE','ROT','IS','TO',   #保留字
        'STEP','DRAW','FOR','FROM',         #保留字
        'T',                                #参数
        'ID',                               #标识符（无用）
        'SEMICO','L_BRACKET','R_BRACKET','COMMA',   #分隔符()
        'PLUS','MINUS','MUL','DIV','POWER',     #运算符
        'FUNC',                             #函数
        'CONST_ID',                         #数值常数
        'ERRTOKEN',                         #错误单词
        # 'NONTOKEN'                          #表示词法分析结束
    ]
    TokenTab = [                        #符号表
    ['CONST_ID',  "PI",		3.1415926,	None],
    ['CONST_ID',  "E",		2.71828,	None],
    #语言中惟一的变量
    ['T',				"T",			0.0,		None],
    #语言允许用的数学函数名(函数原型放在 math.h 中)
    ['FUNC',		"sin",		0.0,		math.sin],
    ['FUNC',		"cos",		0.0,		math.cos],
    ['FUNC',		"tan",		0.0,		math.tan],
    ['FUNC',		"log",			0.0,	math.log],
    ['FUNC',		"exp",		0.0,		math.exp],
    ['FUNC',		"sqrt",		0.0,	    math.sqrt],
    #语句关键字
    ['ORIGIN',	"ORIGIN",	0.0,		None],
    ['SCALE',		"SCALE",	0.0,		None],
    ['ROT',			"ROT",		0.0,		None],
    ['IS',			"IS",			0.0,		None],
    ['FOR',			"FOR",		0.0,		None],
    ['FROM',		"FROM",		0.0,		None],
    ['TO',			"TO",			0.0,		None],
    ['STEP',		"STEP",		0.0,		None],
    ['DRAW',		"DRAW",		0.0,		None]
     ]

    print("记号类别    字符串    常数值    函数指针\n")
    print("________________________________________\n")


    def __init__(self, file_object):
        self.file_object = file_object #文件路径
        self.line_number = 0 #读取到第几行
        self.state = 0 #自动转换机的状态值

        #初始化记号属性
        self.type = ''
        self.lexeme = ''
        self.value = None
        self.func = None

    def isKeyWords(self, char): #判断字符串是否为保留字
        flag = 0
        for token in self.TokenTab:
          if char == token[1]:
              self.type = token[0]
              self.lexeme = token[1]
              self.value = token[2]
              self.func = token[3]
              flag = 1
        if flag == 0:
            self.type = 'ERRTOKEN'


    def Scanner(self):

        #读取每行
        for line in self.file_object:
            line = line.strip('\n')     #去掉每行句尾的换行符
            self.line_number +=1    #每读一行加一
            line_length = len(line)  #算出每行的长度，方便遍历
            i = 0                   #字符的index
            temp_string = ''        #临时字符串

         #读取每个字符
            while i < line_length:
                # 初始化记号属性
                self.type = ''
                self.lexeme = ''
                self.value = None
                self.func = None

                ch = line[i]

                #Comment
                if ch == '/':
                    temp_string = ch    #暂存ch字符
                    ch = line[i + 1]        #ch向前多读一个字符
                    if ch == temp_string: #//
                        while i < line_length:      #读取此行剩下的所有字符
                            # ch = line[i]
                            i += 1
                    else:                  #/
                        self.type = 'DIV'
                        self.lexeme = '/'
                elif ch == '-':
                    temp_string = ch  # 暂存ch字符
                    ch = line[i + 1]  # ch向前多读一个字符
                    if ch == temp_string:  # --
                        while i < line_length:  # 读取此行剩下的所有字符
                            # ch = line[i]
                            i += 1
                    else:               #-
                        self.type = 'MINUS'
                        self.lexeme = '-'

                #空格
                elif ch.isspace():
                    i += 1
                    continue  #直接跳过空格 开始读取下一个字符

                #乘号
                elif ch == '*':
                    temp_string = ch    #暂存当前ch
                    ch = line[i + 1]    #ch向前多读一个字符
                    if ch == temp_string:   #**
                        self.type = 'POWER'
                        self.lexeme = '**'
                    else:                   #*
                        self.type = 'MUL'
                        self.lexeme = '*'

                #逗号
                elif ch == ',':
                    self.type = 'COMMA'
                    self.lexeme = ','

                #分号
                elif ch == ';':
                    self.type = 'SEMICO'
                    self.lexeme = ';'

                #左括号
                elif ch == '(':
                    self.type = 'L_BRACKET'
                    self.lexeme = '('

                #加号
                elif ch == '+':
                    self.type = 'PLUS'
                    self.lexeme = '+'

                #右括号
                elif ch == ')':
                    self.type = 'R_BRACKET'
                    self.lexeme = ')'

                #letter
                elif ch.isalpha():
                    temp_string = ch
                    i += 1
                    ch = line[i]
                    while ch.isalpha() or ch.isdigit():
                        temp_string = temp_string + ch
                        i += 1
                        ch = line[i]

                    self.isKeyWords(temp_string)
                    i -= 1  # 多读了一位符号

                #digit
                elif ch.isdigit():
                    temp_string = ch
                    i += 1
                    ch = line[i]
                    while ch.isdigit():
                        temp_string += ch
                        i += 1
                        ch = line[i]
                    if ch == '.':   #浮点数
                        temp_string += ch
                        i += 1
                        ch = line[i]
                        while ch.isdigit():
                            temp_string += ch
                            i += 1
                            ch = line[i]
                        self.type = 'CONST_ID'
                        self.value = float(temp_string)
                    else:
                        self.type = 'CONST_ID'
                        self.value = int(temp_string)
                    i = i - 1 #多读了一位符号

                #ERRTOKEN
                else:
                    self.type = 'ERRTOKEN'

                if self.type == 'CONST_ID': #常数
                    print(self.type + ' '*12 + str(self.value))
                if self.type == 'FUNC': #函数
                    print(self.type + ' '*4 + self.lexeme + ' '*4 +str(self.func))
                else:
                    if self.type != 'CONST_ID':
                        print(self.type + ' '*4 + self.lexeme)

                #读取下一个字符
                i += 1
            #读取下一行
            self.line_number += 1

if __name__ == '__main__':
    file_object = open("/Users/Faiz/PycharmProjects/Scanner/test.txt")
    dfa = DFA(file_object)
    dfa.Scanner()
    file_object.close()


