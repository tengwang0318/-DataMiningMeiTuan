from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt

xiaozhai = ['佛伦萨·古典火炉披萨', '蘑菇爱上饭', '珍味林饺子馆', '巷子火锅', '千家粗粮王',
            '猫堂小站猫咪主题馆', 'CoCo都可', '福气焖锅烤肉', '5号酒馆', '82°C魔力焖锅',
            '小肥羊', '长安大牌档之长安集市', '泰熙家', '大自在火锅', '拉菲达牛排自助',
            '猫咪餐厅', '京御煌三汁焖锅', '赵家腊汁肉', '米多多烘焙屋', '瑞可爺爺的店',
            '阿姨奶茶专卖', '百富烤霸', '三姊妹香辣土豆片夹馍', '小哥过桥米线',
            '太食獸泰式茶餐厅', '和記丸子専買', '0057香辣虾',
            'M12铁板餐厅', '重庆鸡公煲',
            '洪氏嗨捞·新派猪肚鸡'
            ]
hangtiancheng = ['辣条印象', '福临北京烤鸭', '味都西饼店', '刘大饼香辣土豆片夹馍', '韩味坊牛排自助',
                 '星期八工坊', '红透天自助涮烤', '和福顺养生焖锅', '臻膳轩自助涮烤城',
                 '李想大虾火锅花园',
                 '欧味轩艺术蛋糕', '王府臻品火锅', '艾米客蛋糕', '红透天自助涮烤',
                 '川渝小渔哥', '面道'
                 ]
xiaozhai_words = []
hangtiancheng_words = []
for word in xiaozhai:
    xiaozhai_words.append(jieba.cut(word))
for word in hangtiancheng:
    hangtiancheng_words.append(jieba.cut(word))
res_xiaozhai = ""
res_hangtiancheng = ""
for i in range(len(xiaozhai_words)):
    res_xiaozhai += ("/" + "/".join(xiaozhai_words[i]))
for i in range(len(hangtiancheng_words)):
    res_hangtiancheng += ("/" + "/".join(hangtiancheng_words[i]))
w1 = WordCloud(font_path="simsun.ttf", background_color='white')
w1.generate(res_xiaozhai)
w1.to_file('小寨附近餐饮店铺词云图.png')

w2 = WordCloud(font_path="simsun.ttf", background_color='white')
w2.generate(res_hangtiancheng)
w2.to_file("航天城附近餐饮店铺词云图.png")
