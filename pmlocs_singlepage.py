# -*- coding: utf-8 -*-
import datetime
import os
import re
import PySimpleGUI as sg
import subprocess

ver = "3.1.0"

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
    [sg.Text("カードパックNo", size = (15, 1)), sg.InputText("20", size = (20, 1))],
    [sg.Text("カードパック名", size = (15, 1)), sg.InputText("暗黒のウェルサ", size = (20, 1))],
    [sg.Text("カード名", size = (15, 1)), sg.InputText("", size = (20, 1))],
    [sg.Text("コスト", size = (15, 1)), sg.InputText("", size = (20, 1))],
    [sg.Text("クラス", size = (15, 1)), sg.Combo(("エルフ", "ロイヤル", "ウィッチ", "ドラゴン", "ネクロマンサー", "ヴァンパイア", "ビショップ", "ネメシス", "ニュートラル"), size = (20, 1))],
    [sg.Text("レアリティ", size = (15, 1)), sg.Combo(("ブロンズ", "シルバー", "ゴールド", "レジェンド"), size = (20, 1))],
    [sg.Text("タイプ", size = (15, 1)),sg.Combo(("-", "兵士", "指揮官", "レヴィオン", "財宝", "土の印", "マナリア", "アーティファクト", "機械", "自然"), default_value = "-", size = (20, 1)), sg.Text("複数のタイプを持つカードは\n指揮官・レヴィオン\nのように・で区切って直接入力してください", size = (35, 3))],
    [sg.Text("CV", size = (15, 1)), sg.InputText("", size = (20, 1))],
    [sg.Text("イラストレーター", size = (15, 1)), sg.InputText("", size = (20, 1))],
    [sg.Text("攻撃力(進化前)", size = (15, 1)), sg.InputText("", size = (20, 1))],
    [sg.Text("体力(進化前)", size = (15, 1)), sg.InputText("", size = (20, 1))],
    [sg.Text("攻撃力(進化後)", size = (15, 1)), sg.InputText("", size = (20, 1))],
    [sg.Text("体力(進化後)", size = (15, 1)), sg.InputText("", size = (20, 1))],
    [sg.Text("能力(進化前)", size = (15, 5)), sg.Multiline("")],
    [sg.Text("能力(進化後)", size = (15, 5)), sg.Multiline("")],
    [sg.Text("フレーバーテキスト(進化前)", size = (15, 5)), sg.Multiline("")],
    [sg.Text("フレーバーテキスト(進化後)", size = (15, 5)), sg.Multiline("")],
    [sg.Frame("カードタイプ", layout_kind), sg.Text("スペル、アミュレットは攻撃力と体力、\n能力とフレーバーテキストの進化後は不要です", size = (40, 2))],
    [sg.Submit(button_text = "ページ生成")]
]

window = sg.Window("PMLOCS Ver." + ver, layout, resizable = True)

while True:
  event, values = window.read()

  if event is None:
    break

  if event == "ページ生成":
    no = values[0]
    pack = values[1]
    card_name = values[2]
    card_cost = str(values[3])
    card_class = values[4]
    card_reality = values[5]
    card_type = values[6]
    card_cv = values[7]
    card_illus = values[8]
    card_atk = str(values[9])
    card_life = str(values[10])
    card_atk_evo = str(values[11])
    card_life_evo = str(values[12])
    card_skill = values[13].replace("\n", "~~")
    card_skill_evo = values[14].replace("\n", "~~")
    card_description = values[15].replace("\n", "~~")
    card_description_evo = values[16].replace("\n", "~~")

    if values["-FOLLOWER-"]:
      template = open("follower.txt", "r", encoding = "UTF-8").read()
    elif values["-SPELL-"]:
      template = open("spell.txt", "r", encoding = "UTF-8").read()
    elif values["-AMULET-"]:
      template = open("amulet.txt", "r", encoding = "UTF-8").read()
    today = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    os.makedirs("単一ページ/{0}".format(today))

    # keyword_list = ["ファンファーレ", "ラストワード", "進化時", "攻撃時", "守護", "疾走", "潜伏", "必殺", "ドレイン", "覚醒", "復讐", "スペルブースト", "カウントダウン", "ネクロマンス", "土の秘術", "突進", "交戦時", "エンハンス", "リアニメイト", "葬送", "共鳴", "チョイス", "アクセラレート", "直接召喚", "結晶", "ユニオンンバースト", "渇望", "狂乱", "融合", "連携", "操縦", "奥義", "解放奥義", "公開"]
    # keyword_pattern = r"(%s)" % "|".join(keyword_list)
    # type_list = ["レヴィオン", "財宝", "土の印", "マナリア", "アーティファクト",  "機械", "自然"]
    # type_pattern = r"(%s)" % "|".join(type_list)
    # type_royal_list = ["指揮官", "兵士"]
    # type_royal_pattern = r"(%s)" % "|".join(type_royal_list)

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