# 19968 40908
import re

ZH_RATE = 0.70

def zhdetect_multi( tweets ):
    ans = 0.0000
    cnt = 0
    for tweet in tweets:
        cnt += 1
        if tweet[ 'lang' ] == 'zh':
            ans += 1.000
        else: # fix twitter's own language detect
            tr = zhdetect.zhdetect( tweet[ 'text' ] )
            ans += tr
    if cnt > 0:
        ans /= float( cnt )
    if ans >= ZH_RATE:
        return True
    return False

def zhdetect( rs ):

    HTTP_SUB_REGEX = re.compile('(https?://[\S]+)')
    EN_WORDS_SUB_REGEX = re.compile('(\w+)')
    PUNCT_CHAR_SUB = re.compile(r'(\s+)|(\number+)|([\!\@\#\$\%\^\&\*\(\)\_\+\-\=\<\>\?\/\:\"\'\;\|\\]+)')
    if isinstance( rs , unicode ):
        s = rs
    else:
        s = rs.decode('utf-8')
    s = HTTP_SUB_REGEX.sub( '', s )
    s = PUNCT_CHAR_SUB.sub( '', s )

    tot_chr = len( EN_WORDS_SUB_REGEX.findall( s ) )
    s = EN_WORDS_SUB_REGEX.sub( '', s )
    #print s
    
    zh_chr = 0
    for c in s:
        tot_chr += 1
        if 19968 <= ord( c ) <= 40908:
            zh_chr += 1
    if tot_chr != 0:
        rate = float( zh_chr ) / float( tot_chr )
        print s, zh_chr, tot_chr, rate
        return rate
