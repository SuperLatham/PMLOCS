# -*- coding: utf-8 -*-
import datetime
import os
import re
import PySimpleGUI as sg
import subprocess

ver = "3.1.2"

sg.theme("Dark Blue 3")

with open("keyword.txt", "r", encoding = "UTF-8") as keyword: #外部ファイルからキーワード能力を読み込みlistに変換
  keyword_list = keyword.read().split(",")
keyword_pattern = r"(%s)" % "|".join(keyword_list)
with open("type.txt", "r", encoding = "UTF-8") as type: #外部ファイルからタイプを読み込みlistに変換
  type_list = type.read().split(",")
type_pattern = r"(%s)" % "|".join(type_list)
type_royal_list = ["指揮官", "兵士"] #ロイヤルの兵士・指揮官のみwikiのページ名が特殊なので別処理
type_royal_pattern = r"(%s)" % "|".join(type_royal_list)

layout_kind = [
  [sg.Radio("フォロワー", 1, key = "-FOLLOWER-", default = True)],
  [sg.Radio("スペル", 1, key = "-SPELL-")],
  [sg.Radio("アミュレット", 1, key = "-AMULET-")]
]

layout = [
    [sg.Text("パメラ犯す")],
    [sg.Text("カードパックNo", size = (15, 1)), sg.InputText("21", size = (20, 1), key = "-PACK_NO-")],
    [sg.Text("カードパック名", size = (15, 1)), sg.InputText("リナセント・クロニクル", size = (20, 1), key = "-PACK_NAME-")],
    [sg.Text("カード名", size = (15, 1)), sg.InputText("", size = (20, 1), key = "-CARD_NAME-")],
    [sg.Text("コスト", size = (15, 1)), sg.InputText("", size = (20, 1), key = "-COST-")],
    [sg.Text("クラス", size = (15, 1)), sg.Combo(("エルフ", "ロイヤル", "ウィッチ", "ドラゴン", "ネクロマンサー", "ヴァンパイア", "ビショップ", "ネメシス", "ニュートラル"), size = (20, 1), key = "-CLASS-")],
    [sg.Text("レアリティ", size = (15, 1)), sg.Combo(("ブロンズ", "シルバー", "ゴールド", "レジェンド"), size = (20, 1), key = "-REALITY-")],
    [sg.Text("タイプ", size = (15, 1)),sg.Combo(("-", "兵士", "指揮官", "レヴィオン", "財宝", "土の印", "マナリア", "アーティファクト", "機械", "自然"), default_value = "-", size = (20, 1), key = "-TYPE1-"), sg.Combo(("-", "兵士", "指揮官", "レヴィオン", "財宝", "土の印", "マナリア", "アーティファクト", "機械", "自然"), default_value = "-", size = (20, 1), key = "-TYPE2-")],
    [sg.Text("CV", size = (15, 1)), sg.InputText("", size = (20, 1), key = "-CV-")],
    [sg.Text("イラストレーター", size = (15, 1)), sg.InputText("", size = (20, 1), key = "-ILLUS-")],
    [sg.Text("攻撃力(進化前)", size = (15, 1)), sg.InputText("", size = (20, 1), key = "-ATK-")],
    [sg.Text("体力(進化前)", size = (15, 1)), sg.InputText("", size = (20, 1), key = "-LIFE-")],
    [sg.Text("攻撃力(進化後)", size = (15, 1)), sg.InputText("", size = (20, 1), key = "-ATK_EVO-")],
    [sg.Text("体力(進化後)", size = (15, 1)), sg.InputText("", size = (20, 1), key = "-LIFE_EVO-")],
    [sg.Text("能力(進化前)", size = (15, 5)), sg.Multiline("", key = "-SKILL-"),],
    [sg.Text("能力(進化後)", size = (15, 5)), sg.Multiline("", key = "-SKILL_EVO-")],
    [sg.Text("フレーバーテキスト(進化前)", size = (15, 5)), sg.Multiline("", key = "-DESCRIPTION-")],
    [sg.Text("フレーバーテキスト(進化後)", size = (15, 5)), sg.Multiline("", key = "-DESCRIPTION_EVO-")],
    [sg.Frame("カードタイプ", layout_kind), sg.Text("スペル、アミュレットは攻撃力と体力、\n能力とフレーバーテキストの進化後は不要です", size = (40, 2))],
    [sg.Submit(button_text = "ページ生成")]
]

window = sg.Window("PMLOCS Ver." + ver, layout, resizable = True)

while True:
  event, values = window.read()

  if event is None:
    break

  if event == "ページ生成":
    no = values["-PACK_NO-"]
    pack = values["-PACK_NAME-"]
    card_name = values["-CARD_NAME-"]
    card_cost = str(values["-COST-"])
    card_class = values["-CLASS-"]
    card_reality = values["-REALITY-"]
    card_type1 = values["-TYPE1-"]
    card_type2 = values["-TYPE2-"]
    card_cv = values["-CV-"]
    card_illus = values["-ILLUS-"]
    card_atk = str(values["-ATK-"])
    card_life = str(values["-LIFE-"])
    card_atk_evo = str(values["-ATK_EVO-"])
    card_life_evo = str(values["-LIFE_EVO-"])
    card_skill = values["-SKILL-"].replace("\n", "~~")
    card_skill_evo = values["-SKILL_EVO-"].replace("\n", "~~")
    card_description = values["-DESCRIPTION-"].replace("\n", "~~")
    card_description_evo = values["-DESCRIPTION_EVO-"].replace("\n", "~~")

    if values["-FOLLOWER-"]:
      template = open("follower.txt", "r", encoding = "UTF-8").read()
    elif values["-SPELL-"]:
      template = open("spell.txt", "r", encoding = "UTF-8").read()
    elif values["-AMULET-"]:
      template = open("amulet.txt", "r", encoding = "UTF-8").read()
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    os.makedirs("単一ページ/{0}".format(today))

    if card_type2 == "-":
      card_type = card_type1
    else:
      card_type = card_type1 + "・" + card_type2

    card_type = re.sub(type_pattern, r"''[[\1>タイプ:\1]]''", card_type)
    card_type = re.sub(type_royal_pattern, r"''[[\1>タイプ:指揮官/兵士]]''", card_type) #ロイヤルの兵士・指揮官のみwikiのページ名が特殊なので別処理
    card_skill = re.sub(keyword_pattern,  r"''[[\1]]''", card_skill)
    card_skill_evo = re.sub(keyword_pattern,  r"''[[\1]]''", card_skill_evo)
    template_edited = template.replace("name", card_name).replace("no", no).replace("class", card_class).replace("cost", card_cost).replace("reality", card_reality).replace("type", card_type).replace("pack", pack).replace("cv", card_cv).replace("atk_evo", card_atk_evo).replace("life_evo", card_life_evo).replace("skill_evo", card_skill_evo).replace("description_evo", card_description_evo).replace("atk", card_atk).replace("life", card_life).replace("skill", card_skill).replace("description", card_description).replace("illus", card_illus)
    file_dir = "./単一ページ/{0}/{1}.txt".format(today, card_name)
    card_page = open(file_dir, "x")
    card_page.write(template_edited)
    card_page.close()

    if os.name == "nt":
      subprocess.run("start " + file_dir, shell = True)
    elif os.name == "posix":
      subprocess.run("open " + file_dir_abs)

  sg.popup("『ターゲット撃破』「勝ち勝ちー！」")
window.close()