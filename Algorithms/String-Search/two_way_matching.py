'''
    Naive Two way String-Matching implementation for searching matches in a string 
    Paper: Maxime Crochemore and Dominique Perrin, 1991. Two-way string-matching. J. ACM 38, 3 (July 1991), 650-674
'''

import pdb

def pre_process_max_suffix(p):
    n = len(p)
    ms = -1
    j = 0
    k = 1
    pos = 1
    while j + k < n:
        a = p[ms+k]
        b = p[j+k]
        if(ord(b) < ord(a)):
           j = j + k
           k = 1
           pos = j-ms
        elif (ord(b) == ord(a)):
            if k == pos:
                j = j + pos
                k = 1
            else:
                k = k +1 
        else: #(ord(b) > ord(a)):
            ms = j
            j = ms + 1
            k = 1
            pos = 1
    return ms,pos

def pre_process_max_suffix_tilde(p):
    n = len(p)
    ms = -1
    j = 0
    k = 1
    pos = 1
    while j + k < n:
        a = p[j+k]
        b = p[ms+k]
        if(ord(b) < ord(a)):
           j = j + k
           k = 1
           pos = j-ms
        elif (ord(b) == ord(a)):
            if k == pos:
                j = j + pos
                k = 1
            else:
                k = k +1 
        else: #(ord(b) > ord(a)):
            ms = j
            j = ms + 1
            k = 1
            pos = 1
    return ms,pos

'''
    Critical factorization, we divide the string X in X_l and X_r.
    where the period and the local period converge.
    period => x[i] = x[i+p]
    local period => How much do I have to enlarge a string from a position so that X_l equal X_r
    or a part of it e.g., AB AB 
                            2 -> since AB == AB
                          ABC DEF
                             6 -> since  (DEF)ABC == DEF(ABC)
    l, is the index of the last char of X_l e.g., page 656 at the ACM paper
                G C A G A G A G
Local Period:    3 7 7 2 2 2 2
Period : 7
l = 1
X_l = GC ; X_r = AGAGAG
or
X_l = GCA ; X_r = GAGAG

                A M A Z O N I 
Local Period:    2 7 7 7 7 7 
Period : 7
l = 1
X_l = AM ; X_r = AZONI
or
X_l = AMA ; X_r = ZONI
or
X_l = AMAZ ; X_r = ONI

As we are using max suffix, X_l = AMA, X_r = ZONI

                A B A A B A A
Local Period:    2 3 1 3 3 1
Period : 3
l = 1
X_l = AB; X_r = AABAA

'''

def critical_factorization(p):
    l_1,p_1 = pre_process_max_suffix(p)
    l_2,p_2 = pre_process_max_suffix_tilde(p)
    pdb.set_trace()
    if(l_1 >= l_2):
        return l_1,p_1
    else:
        return l_2,p_2


def search_two_way(t, pattern):
    n = len(pattern)
    l, p = critical_factorization(pattern) 
    s1 = pattern[0:l+1]
    s2 = pattern[l+1:l+p+1]
    is_suffix = s2.endswith(s1);
    P = []
    if l < n/2 and is_suffix: 
        pos = 0
        s = -1
        while pos + n <= len(t):
            i = max(l,s) + 1 # get the index of X_r
            while i < n and pattern[i] == t [pos + i]:
                i = i + 1
            if i < n:
                pos = pos + max(i-l,s-p+1)
                s = -1
            else: # check the left part of the word
                j = l
                while j > s and pattern[j] == t[pos+j]:
                    j = j -1
                if j <= s:
                   P.append(pos)
                pos = pos + p
                s = n - p - 1
        return P
    else:
        q = max(l, n-l) + 1
        pos = 0
        while pos + n <= len(t):
            i = l+1
            while i < n and pattern[i] == t[pos + i]:
                i = i + 1
            if i < n:
                pos = pos + i - l
            else:
                j = l
                while j > -1 and pattern[j] == t[pos+j]:
                    j = j -1
                if j == -1:
                    P.append(pos)
                pos = pos + q
        return P

if __name__ == "__main__":
#    p = 'GCAGAGAG'
    #p = 'ABAABAA'
    #p = 'AMAZONIA'
    #p = 'AAA' 

    p = '0c5b8f279a64baabbe3400000800450005dc41bb40003f067f43ac100001c0a808641451a468fcae454ec839eaa48010020099ce00000101080aabbe4332af25f32e74fdbb775d6f7dd3a2aa2f0feefce436e601fca0d0b135ccd48229d3cf57a043545bbbb1ca38846ce2b47bd0b060079661033731b46cfd88ee265bbe7dfb01d156bc8320f4078dd7bb08a76c68ae02c9b139fa65a5f7ed941e48529b43536d9910f0ba04f747dbb34f831fb8312181e35b7c4800733694917ee62dc23a9a5b4a8a154e815c2a34acad5364de75e5c1d0610ad0d5406566be4b9380852ddccfb7f11e394e486dfaf5c15ed336439506a59fd67adf3be09d87741e0ca1fadc59ebfa923942ff3337c0910af6d59ffc7a3ed3f41d0ed4bb9548d9a2ead37e43be78d5f8bad42bf195bdfb8b929b880cd95b00f769d4b2ff1d8ba1075e1f4a1c971f1451f3404288fd3d148fd89c9bb2f79ba9606f5b5f8ce60093441fdd60b6fc7507f0b54978b2878c415f28dc111f77ba80e615df73fbe0063fffe4a0b6e015bdd0ca07497c8ed5bdedfe99ff1d10b99df6cf7d69ca5d700a5c54aa1234bfd00589d74e056523c252215b513f6b0bdc61da59cba4b63bae138f5825c317f5c8a0cc16a5313a67845bc2d59a2de0778fbad05a5f87950d9a2466bfe77db5b01e81c6c3b3002b375ced0cf61bed6daaa73e0406c599145fbd7a1ea4f7d35415551bd9081b043f77f14b6e0c38dbb6e019bae6de53fa3d10745cb56c2f098184245a8c405ecbb75017255c4f01132f1acd16f9211036318592e6f1c2f0724614cdd3542b9e0c7bb531d80532eb344db84a46d95b7c0be00ff1d1d1e14317f610ea4a3c8956b73e888f43ba7a780733c24d0c1dca17fdd909ceaaea12c1e022ac2b5e3581167309a5b7c4202fcb53f1195f0fe3770cbc80db666aed274b0fd3766e08f7847c012933c54962909c53a9fc628c736f48f34aae5d37d6a846a91eb4b216382e176261dcabc36c4816164479a2b7e8ebaa329907696fb0af19ce64cbe49cf9fbfe5ad7aa1d44f2335a36acfced94e797c6819e2ff04edf091d43d401dfcdfdde27d48844187a7872b0246f9db956347fd7d2afc8218ed13ed1a63fb0733c8e9b1116df2990579c407c0bdd356111b439e4630105f1d243c2788273ecbf0187d01866f9a8be95e93aa0c66f02d8233bbc873cc1780e043b8786ae7345affa15c7600f701ea45958451fc747f7eb82b372be74eacc782553ffd3c64483c05a4a2169ba3f0d139852335f992a4a1bdebcd952a7a6cbccf9caa0c00e2380686da1d128e1df3b79316ed8cb9923e677dfc0c9866694535f5ef31f6d16a0d58341a7ab2286e79bb7557482ee97696576292ffd8fc350ee22430e8f59ae64dcef0b88'
   
    l, p3 = critical_factorization(p) 
    print 'p2 len = ' + str(len(p)) +  ' l = ' + str(l) + ' p = ' + str(p3)
 


    #t = 'AAAMAZONIAAIABBABABRQMYOAABBBBABABYOSGBBGTVBHABBABABSUJKSKKHKJAMAZONZONABBAMAZONIAABBABABABAYAMAZONIARQMYOIUHKJHJHSDASDASDNIAURTOAMAZONIAAABBABABNLK'
    #t = 'AAADERFTYAAAHSWEEAAA' 
    #t = 'AIABBABABRQMYOAABBBBABABYOSGBBGTVBHGCAGAGAGABBABABSUJKSKKHKJABBABBABABABAYRQMYOIUHKJHJHSDASDASDNNLK'



    t = '67efbad0c5b8f279a64baabbe3400000800450005dc41bb40003f067f43ac100001c0a808641451a468fcae454ec839eaa48010020099ce00000101080aabbe4332af25f32e74fdbb775d6f7dd3a2aa2f0feefce436e601fca0d0b135ccd48229d3cf57a043545bbbb1ca38846ce2b47bd0b060079661033731b46cfd88ee265bbe7dfb01d156bc8320f4078dd7bb08a76c68ae02c9b139fa65a5f7ed941e48529b43536d9910f0ba04f747dbb34f831fb8312181e35b7c4800733694917ee62dc23a9a5b4a8a154e815c2a34acad5364de75e5c1d0610ad0d5406566be4b9380852ddccfb7f11e394e486dfaf5c15ed336439506a59fd67adf3be09d87741e0ca1fadc59ebfa923942ff3337c0910af6d59ffc7a3ed3f41d0ed4bb9548d9a2ead37e43be78d5f8bad42bf195bdfb8b929b880cd95b00f769d4b2ff1d8ba1075e1f4a1c971f1451f3404288fd3d148fd89c9bb2f79ba9606f5b5f8ce60093441fdd60b6fc7507f0b54978b2878c415f28dc111f77ba80e615df73fbe0063fffe4a0b6e015bdd0ca07497c8ed5bdedfe99ff1d10b99df6cf7d69ca5d700a5c54aa1234bfd00589d74e056523c252215b513f6b0bdc61da59cba4b63bae138f5825c317f5c8a0cc16a5313a67845bc2d59a2de0778fbad05a5f87950d9a2466bfe77db5b01e81c6c3b3002b375ced0cf61bed6daaa73e0406c599145fbd7a1ea4f7d35415551bd9081b043f77f14b6e0c38dbb6e019bae6de53fa3d10745cb56c2f098184245a8c405ecbb75017255c4f01132f1acd16f9211036318592e6f1c2f0724614cdd3542b9e0c7bb531d80532eb344db84a46d95b7c0be00ff1d1d1e14317f610ea4a3c8956b73e888f43ba7a780733c24d0c1dca17fdd909ceaaea12c1e022ac2b5e3581167309a5b7c4202fcb53f1195f0fe3770cbc80db666aed274b0fd3766e08f7847c012933c54962909c53a9fc628c736f48f34aae5d37d6a846a91eb4b216382e176261dcabc36c4816164479a2b7e8ebaa329907696fb0af19ce64cbe49cf9fbfe5ad7aa1d44f2335a36acfced94e797c6819e2ff04edf091d43d401dfcdfdde27d48844187a7872b0246f9db956347fd7d2afc8218ed13ed1a63fb0733c8e9b1116df2990579c407c0bdd356111b439e4630105f1d243c2788273ecbf0187d01866f9a8be95e93aa0c66f02d8233bbc873cc1780e043b8786ae7345affa15c7600f701ea45958451fc747f7eb82b372be74eacc782553ffd3c64483c05a4a2169ba3f0d139852335f992a4a1bdebcd952a7a6cbccf9caa0c00e2380686da1d128e1df3b79316ed8cb9923e677dfc0c9866694535f5ef31f6d16a0d58341a7ab2286e79bb7557482ee97696576292ffd8fc350ee22430e8f59ae64dcef0b88'


    positions = search_two_way(t,p)
    for p in positions:
        print 'Pattern found at position = ' + str(p)

