1 LET A = 1
2 LET B = 2
3 GOSUB 30
4 LET A = 2
5 LET B = 2
6 GOSUB 30
7 LET A = 2
8 LET B = 1
9 GOSUB 30
10 GOTO 9999
30 IF A = B THEN 100 
40 IF A > B THEN 80
50 PRINT A;" LESS THAN ";B
60 RETURN
70
80 PRINT A;" GREATER THAN ";B
90 RETURN
95
100 PRINT A;" EQUALS ";B
110 RETURN
9999 END