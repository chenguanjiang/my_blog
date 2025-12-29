
tags_str = '潇洒 哇哈哈 无敌 慢慢 零零 看看 噢噢 周末 大哥 可爱 表情'

for tag in tags_str.split():
    print(tag)

print ([tag.strip()[0] for tag in tags_str.split()])