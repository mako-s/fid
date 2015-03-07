# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 19:32:41 2015

@author: m_sonoda
"""

import random
import math
import sys

class fid:
    def __init__(self, bit_s):
        ##### 1 #####
        bit_len = len(bit_s)
        large_block_length = pow(int(math.log(bit_len,2)),2)
        large_block_num = bit_len / large_block_length
        large_rank_line_s = [0]
        for i in range(large_block_num):
            hoge = 0
            for j in range(0+i*large_block_length,large_block_length+i*large_block_length):
                hoge = hoge + bit_s[j]
            large_rank_line_s.append(hoge)
    
        large_rank_line = [(0,0)]
        for i in range(1,len(large_rank_line_s)):
            large_rank_line.append((i*large_block_length,sum(large_rank_line_s[:i+1])))
        ##### 2 #####
        small_block_length = int(math.log(bit_len,2))/2
        small_block_num = large_block_length / small_block_length
        small_rank_line = []
        hogehoge=0
        for i in range(large_block_num):
            small_rank_line.append(((i*large_block_length),0))
            for j in range(small_block_num):
               for k in range(0+j*small_block_length,small_block_length+j*small_block_length):
                   hogehoge = hogehoge + bit_s[k+i*large_block_length]
               small_rank_line.append((i*large_block_length + k,(hogehoge)))
            hogehoge = 0         
        ##### 3 #####    
        bit_table = []
        for i in range(pow(2,small_block_length)):
            binary = format(i,'b').zfill(small_block_length)
            binary_list = list(binary)
            foo = 0
            for j in range(len(binary_list)):
                foo = foo + int(binary_list[j])
            bit_table.append((foo,binary))
        self.auxiliary_data = (large_rank_line,small_rank_line,bit_table)
        self.bit_s = bit_s
        self.small_block_length = small_block_length
        return
        
    def rank1(self, index):
        if index > len(self.bit_s):
            print '*Oops!*'
            sys.exit()
        for i in range(len(self.auxiliary_data[0])):
            if index < self.auxiliary_data[0][i][0]:
                break
        large_rank_value = self.auxiliary_data[0][i-1][1]
        bit_tmp = index - self.auxiliary_data[0][i-1][0]
        if bit_tmp == 0:
            return self.auxiliary_data[0][i-1][0]
            
        s_range = (i-1) * len(self.auxiliary_data[1])/self.small_block_length
        for j in range(s_range,s_range + len(self.auxiliary_data[1])/self.small_block_length):
            if index <= self.auxiliary_data[1][j][0]:
                if index == self.auxiliary_data[1][j][0]:
                    return self.auxiliary_data[1][j][0]
                break

        small_rank_value = self.auxiliary_data[1][j-1][1]
        small_bit_tmp = index - self.auxiliary_data[1][j-1][0]
        small_bit_s = map(str,self.bit_s[self.auxiliary_data[1][j-1][0]:self.auxiliary_data[1][j-1][0]+self.small_block_length]) 
        mask_bit_s = small_bit_s[0:small_bit_tmp] 
        bar = ['0']
        foobar = bar*(len(small_bit_s)-len(mask_bit_s))
        mask_bit_s = mask_bit_s + foobar
        mask_bit_b = "".join(mask_bit_s)
    
        for i in range(len(self.auxiliary_data[2])):
            if mask_bit_b == self.auxiliary_data[2][i][1]:
                rank_value = large_rank_value + small_rank_value + self.auxiliary_data[2][i][0]
                return rank_value
    
    def select1(self, value):
        if value > len(self.bit_s):
            print '*Oops!*'
            sys.exit()
        for i in range(len(self.auxiliary_data[0])):
            if value <= self.auxiliary_data[0][i][1]:
                break
        
        if value > self.auxiliary_data[0][i][1]:
            print '*Out of range value*'
            return 
        
        bit_tmp = value - self.auxiliary_data[0][i-1][1]
        if bit_tmp == 0:
            return self.auxiliary_data[0][i-1][0]
        s_range = (i-1) * len(self.auxiliary_data[1])/self.small_block_length
    
        for j in range(s_range,s_range + len(self.auxiliary_data[1])/self.small_block_length):
            if bit_tmp <= self.auxiliary_data[1][j][1]:
                if bit_tmp == self.auxiliary_data[1][j][1]:
                    return self.auxiliary_data[1][j][0]
                break
        
        small_select_value = bit_tmp - self.auxiliary_data[1][j-1][1] 
        baz = 0

        for select_value in range(self.auxiliary_data[1][j-1][0]+1,self.auxiliary_data[1][j-1][0]+self.small_block_length+1):
            baz = baz + self.bit_s[select_value]
            if baz == small_select_value:
                select_value = select_value + 1
                return select_value 
    
    def rank0(self, index):
        if index > len(self.bit_s):
            print '*Oops!*'
            sys.exit()
        rank0_value = index - fid.rank1(self,index)
        return rank0_value
        
    def select0(self, value):
        if value > len(self.bit_s):
            print '*Oops!*'
            sys.exit()
        index = value
        for i in range(len(self.auxiliary_data[0])):
            if index < self.auxiliary_data[0][i][0] - self.auxiliary_data[0][i][1]:
                break
        
        if value > self.auxiliary_data[0][i][1]:
            print '*Out of range value*'
            return   
        
        bit_tmp0 = value - (self.auxiliary_data[0][i-1][0] - self.auxiliary_data[0][i-1][1])
        if bit_tmp0 == 0:
            return self.auxiliary_data[0][i-1][0]
        
        s_range = (i-1) * len(self.auxiliary_data[1])/self.small_block_length
        hoge = self.auxiliary_data[1][s_range][0]
        
        for j in range(s_range,s_range + len(self.auxiliary_data[1])/self.small_block_length):
            if bit_tmp0 <= (self.auxiliary_data[1][j][0] - hoge) - self.auxiliary_data[1][j][1]:
                if s_range == self.auxiliary_data[1][j-1][0]:
                    small_select_value = bit_tmp0 - ((self.auxiliary_data[1][j-1][0] + 1 - hoge) - self.auxiliary_data[1][j-1][1])
                break
            else:
                small_select_value = bit_tmp0 - ((self.auxiliary_data[1][j][0] - hoge) - self.auxiliary_data[1][j][1])    
        
        baz = 0
        for select_value in range(self.auxiliary_data[1][j-1][0]+1,self.auxiliary_data[1][j-1][0]+self.small_block_length+1):
            baz = baz + (self.bit_s[select_value] ^ 1)
            if baz == small_select_value:
                select_value = select_value + 1
                print 'select_value = %s' % select_value
                return select_value 
        
def main():
    bit_s = []
    for i in range(256):
        bit_s.append(random.randint(0,1))

    #print bit_s    
    f = fid(bit_s)
    #f.rank1(700)
    #f.select1(20)
    f.rank0(70)
    #f.select0(70)
    
if __name__ == "__main__":
    main()