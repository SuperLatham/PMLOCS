import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import re

print("カードパックNoを半角で入力して、Enterを押して下さい")
no = input()
print("カードパック名を入力して、Enterを押して下さい")
pack = input()
print("「少し待て」")

card_name_list = []
card_link_list = []
card_type_list = []
card_class_list = []
card_rarity_list = []
card_cv_list = []
card_atk_list = []
card_life_list = []
card_skill_list = []
card_description_list = []
card_atk_evo_list = []
card_life_evo_list = []
card_skill_evo_list = []
card_description_evo_list = []
card_kind_list = []
card_cost_list = []

card_cost_0_list = []
card_cost_1_list = []
card_cost_2_list = []
card_cost_3_list = []
card_cost_4_list = []
card_cost_5_list = []
card_cost_6_list = []
card_cost_7_list = []
card_cost_8_list = []
card_cost_9_list = []
card_cost_10_list = []

for classID in range(9):
    getUrl = 'https://shadowverse-portal.com/cards?clan%5B0%5D=' + str(classID) + '&format=3&card_set%5B0%5D=100' + no + '&lang=ja' #対象URL
    html = requests.get(getUrl)
    soup = BeautifulSoup(html.content, "html.parser")
    for card_name in soup.find_all(class_ = "el-card-visual-name"):
        card_name_list.append(card_name.text)
    for card_link in soup.find_all(class_ = "el-card-visual-content"):
        card_link_list.append(card_link.get("href"))


for cost in range(11):
    for classID in range(9):
        searchUrl = "https://shadowverse-portal.com/cards?clan[]=" + str(classID) + "&card_set[]=100" + no + "&cost[]=" + str(cost) + "&lang=ja"
        search_html = requests.get(searchUrl)
        seach_soup = BeautifulSoup(search_html.content, "html.parser")
        for search_name in seach_soup.find_all(class_ = "el-card-visual-name"):
            if cost == 0:
                card_cost_0_list.append(search_name.text)
            elif cost == 1:
                card_cost_1_list.append(search_name.text)
            elif cost == 2:
                card_cost_2_list.append(search_name.text)
            elif cost == 3:
                card_cost_3_list.append(search_name.text)
            elif cost == 4:
                card_cost_4_list.append(search_name.text)
            elif cost == 5:
                card_cost_5_list.append(search_name.text)
            elif cost == 6:
                card_cost_6_list.append(search_name.text)
            elif cost == 7:
                card_cost_7_list.append(search_name.text)
            elif cost == 8:
                card_cost_8_list.append(search_name.text)
            elif cost == 9:
                card_cost_9_list.append(search_name.text)
            else:
                card_cost_10_list.append(search_name.text)

for i in card_name_list:
    if i in card_cost_0_list:
        card_cost_list.append("0")
    elif i in card_cost_1_list:
        card_cost_list.append("1")
    elif i in card_cost_2_list:
        card_cost_list.append("2")
    elif i in card_cost_3_list:
        card_cost_list.append("3")
    elif i in card_cost_4_list:
        card_cost_list.append("4")
    elif i in card_cost_5_list:
        card_cost_list.append("5")
    elif i in card_cost_6_list:
        card_cost_list.append("6")
    elif i in card_cost_7_list:
        card_cost_list.append("7")
    elif i in card_cost_8_list:
        card_cost_list.append("8")
    elif i in card_cost_9_list:
        card_cost_list.append("9")
    else:
        card_cost_list.append("10")

for i in card_link_list:
    cardUrl = "https://shadowverse-portal.com" + i + "?lang=ja"
    card = requests.get(cardUrl)
    soup = BeautifulSoup(card.content, "html.parser")
    card_atk_temp = []
    card_life_temp = []
    for card_type in soup.select("ul.card-info-content > li:nth-of-type(1) > span:nth-of-type(2)"):
        card_type_list.append(card_type.text.replace("\r\n", ""))
    for card_class in soup.select("ul.card-info-content > li:nth-of-type(2) > span:nth-of-type(2)"):
        card_class_list.append(card_class.text.replace("\r\n", ""))
    for card_rarity in soup.select("ul.card-info-content > li:nth-of-type(3) > span:nth-of-type(2)"):
        card_rarity_list.append(card_rarity.text.replace("レア", "").replace("\r\n", ""))
    for card_cv in soup.select("ul.card-info-content > li:nth-of-type(6) > span:nth-of-type(2)"):
        card_cv_list.append(card_cv.text.replace("\r\n", ""))
    for card_skill in soup.select("ul.card-main-list > li:nth-of-type(1) > p.card-content-skill"):
        for card_skill_br in card_skill.select("br"):
            card_skill_br.replace_with("~~")
        card_skill_list.append(card_skill.text.replace("\r\n", ""))
    for card_description in soup.select("ul.card-main-list > li:nth-of-type(1) > p.card-content-description"):
        for card_description_br in card_description.select("br"):
            card_description_br.replace_with("~~")
        card_description_list.append(card_description.text.replace("\r\n", ""))
    if i[11] == "1":
        card_kind_list.append("フォロワー")
        for card_atk in soup.find_all(class_ ="is-atk"):
            card_atk_temp.append(card_atk.text.replace("\r\n", ""))
        card_atk_list.append(card_atk_temp[0])
        card_atk_evo_list.append(card_atk_temp[1])
        for card_life in soup.find_all(class_ ="is-life"):
            card_life_temp.append(card_life.text.replace("\r\n", ""))
        card_life_list.append(card_life_temp[0])
        card_life_evo_list.append(card_life_temp[1])
        for card_skill_evo in soup.select("ul.card-main-list > li:nth-of-type(2) > p.card-content-skill"):
            for card_skill_evo_br in card_skill_evo.select("br"):
                card_skill_evo_br.replace_with("~~") 
            card_skill_evo_list.append(card_skill_evo.text.replace("\r\n", "").replace("\n", " "))
        for card_description_evo in soup.select("ul.card-main-list > li:nth-of-type(2) > p.card-content-description"):
            for card_description_evo_br in card_description_evo.select("br"):
                card_description_evo_br.replace_with("~~")
            card_description_evo_list.append(card_description_evo.text.replace("\r\n", ""))
    elif i[11] == "3":
        card_kind_list.append("アミュレット")
        card_atk_list.append("")
        card_atk_evo_list.append("")
        card_life_list.append("")
        card_life_evo_list.append("")
        card_skill_evo_list.append("")
        card_description_evo_list.append("")
    elif i[11] == "4":
        card_kind_list.append("スペル")
        card_atk_list.append("")
        card_atk_evo_list.append("")
        card_life_list.append("")
        card_life_evo_list.append("")
        card_skill_evo_list.append("")
        card_description_evo_list.append("")
    
df = pd.DataFrame({"link": card_link_list,
                   "kind": card_kind_list,
                   "type": card_type_list,
                   "class": card_class_list,
                   "cost": card_cost_list,
                   "reality": card_rarity_list,
                   "cv": card_cv_list,
                   "atk": card_atk_list,
                   "life": card_life_list,
                   "skill": card_skill_list,
                   "description": card_description_list,
                   "atk_evo": card_atk_evo_list,
                   "life_evo": card_life_evo_list,
                   "skill_evo": card_skill_evo_list,
                   "description_evo": card_description_evo_list,
                   },
                   index = card_name_list)
df = df.astype("str")

follower_template = open("follower.txt", "r", encoding = "UTF-8").read()
spell_template = open("spell.txt", "r", encoding = "UTF-8").read()
amulet_template = open("amulet.txt", "r", encoding = "UTF-8").read()
today = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
os.makedirs("{0}_{1}_{2}/ニュートラル".format(no, pack, today))
os.makedirs("{0}_{1}_{2}/エルフ".format(no, pack, today))
os.makedirs("{0}_{1}_{2}/ロイヤル".format(no, pack, today))
os.makedirs("{0}_{1}_{2}/ウィッチ".format(no, pack, today))
os.makedirs("{0}_{1}_{2}/ドラゴン".format(no, pack, today))
os.makedirs("{0}_{1}_{2}/ネクロマンサー".format(no, pack, today))
os.makedirs("{0}_{1}_{2}/ヴァンパイア".format(no, pack, today))
os.makedirs("{0}_{1}_{2}/ビショップ".format(no, pack, today))
os.makedirs("{0}_{1}_{2}/ネメシス".format(no, pack, today))

keyword_list = ["ファンファーレ", "ラストワード", "進化時", "攻撃時", "守護", "疾走", "潜伏", "必殺", "ドレイン", "覚醒", "復讐", "スペルブースト", "カウントダウン", "ネクロマンス", "土の秘術", "突進", "交戦時", "エンハンス", "リアニメイト", "葬送", "共鳴", "チョイス", "アクセラレート", "直接召喚", "結晶", "ユニオンンバースト", "渇望", "狂乱", "融合", "連携", "操縦", "奥義", "解放奥義", "公開"]
keyword_pattern = r"(%s)" % "|".join(keyword_list)
type_list = ["レヴィオン", "財宝", "土の印", "マナリア", "アーティファクト",  "機械", "自然"]
type_pattern = r"(%s)" % "|".join(type_list)
type_royal_list = ["指揮官", "兵士"]
type_royal_pattern = r"(%s)" % "|".join(type_royal_list)

for card_name in card_name_list:
    if df.at[card_name, "kind"] == "フォロワー" :
        template = follower_template
    elif df.at[card_name, "kind"] == "スペル" :
        template = spell_template
    elif df.at[card_name, "kind"] == "アミュレット" :
        template = amulet_template
    card_type = re.sub(type_pattern, r"''[[\1>タイプ:\1]]''", df.at[card_name, "type"])
    card_type = re.sub(type_royal_pattern, r"''[[\1>タイプ:指揮官/兵士]]''", card_type)
    template_edited = template.replace("name", card_name).replace("no", no).replace("class", df.at[card_name, "class"]).replace("cost", df.at[card_name, "cost"]).replace("reality", df.at[card_name, "reality"]).replace("type", card_type).replace("pack", pack).replace("cv", df.at[card_name, "cv"]).replace("atk_evo", df.at[card_name, "atk_evo"]).replace("life_evo", df.at[card_name, "life_evo"]).replace("skill_evo", df.at[card_name, "skill_evo"]).replace("description_evo", df.at[card_name, "description_evo"]).replace("atk", df.at[card_name, "atk"]).replace("life", df.at[card_name, "life"]).replace("skill", df.at[card_name, "skill"]).replace("description", df.at[card_name, "description"])
    template_edited = re.sub(keyword_pattern, r"''[[\1]]''", template_edited)
    card_page = open("./{0}_{1}_{2}/{3}/{4}.txt".format(no, pack, today, df.at[card_name, "class"], card_name), "x")
    card_page.write(template_edited)
    card_page.close()

print("『ターゲット撃破』「勝ち勝ちー！」")