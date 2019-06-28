"""
我输入第一行文字和y值，剩下的行文字的行y差值。
[["业水级辣他家肉强内少意点元烤入大得看友气餐门修值",39],["同找底喜赞两真道较做香这度因朋你觉可儿近超五油如小果性现老食尝",64]]
"""
li = [["度内两客再式别老的放成上常可重甜西理分嫩要家",39],["非当挺口近前行了没辣场本总到荐哈差买牛太号料午串油打对心",64],["整等板想无啊给串粉定口接己行号置十酸调正边块",100],["跟很东棒高过汤错像价环态分面装店本奶满打中完又位花后其全菜式非适没评特爱手太",122]]
def get_xy(li,inde=19,jianju=14):
    """
    :param li:文字和行高
    :param inde: 第一行起始行高（大众点评我今天看的是26）
    :param jianju: 每个文字的间距，这个目前看来是固定值（大众点评看是14间距）
    :return:
    """
    result = {}
    for index,i in enumerate(li):
        # 第一行
        if index == 0:
            a = get_dic(i, jianju, inde)
            # for a in get_dic(i, jianju, inde):
            result.update(a)
        else:
            gao = i[1]-li[index-1][1]
            inde = inde + gao
            a = get_dic(i, jianju, inde)
            result.update(a)
    print(result)
    return result

def get_dic(i,jianju,inde):
    d = {}
    d[inde] = {}
    for index1, wenzi in enumerate(i[0]):
            x = jianju * index1
            # y = inde
            d[inde][x] = wenzi
            # dic = dict(name=wenzi, x=x, y=y)
    return d

if __name__ == '__main__':
    li = [["业水级辣他家肉强内少意点元烤入大得看友气餐门修值",39],["同找底喜赞两真道较做香这度因朋你觉可儿近超五油如小果性现老食尝",64],["整等板想无啊给串粉定口接己行号置十酸调正边块",100],["跟很东棒高过汤错像价环态分面装店本奶满打中完又位花后其全菜式非适没评特爱手太",122]]
    get_xy(li)