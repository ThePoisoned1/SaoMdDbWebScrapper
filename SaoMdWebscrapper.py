import operator
import requests
from bs4 import BeautifulSoup
import re
from character import Character
from pprint import pprint
import json
import csv


def contains_chara_info(data):
    aux = data.find_all('h3')
    if len(aux) > 0 and aux[0].text == 'NO DATA':
        return False
    return True


def get_HTML_from_url(url):
    page = requests.get(url)
    page = BeautifulSoup(page.content, "html.parser")
    return page


def check_for_bracket(word):
    if word[0] == '[':
        return word[0]+word[1:].capitalize()
    else:
        return word.capitalize()


def fix_name(name):
    old = name.split(' ')
    if len(old) == 1:
        return check_for_bracket(name) if len(name) > 0 else name
    fixedName = []
    fixedName.append(check_for_bracket(old[0]))
    for word in old[1:]:
        word = word.replace('’', "'")
        if word.lower() in ['of', 'the', 'a']:
            fixedName.append(word.lower())
        elif '-' in word:
            fixedName.append('-'.join([x.capitalize()
                             for x in word.split('-')]))
        else:
            fixedName.append(word.capitalize())
    return ' '.join(fixedName)


def parse_name(name):
    return re.sub(' {2,}', ' ', name.split('\n')[1].strip())


def get_chara_basics(data):
    result = data.find_all('div', class_="title__first")
    name = parse_name(result[0].find_all('h5')[0].text)
    name = fix_name(name)
    unitName = result[0].find_all('h6')[0].text.lower().strip()
    unitName = fix_name(unitName).replace('’', "'")
    aux = result[0].find_all('img')
    rarity = int(aux[0]['alt'][0])
    weapon, element = aux[1]['alt'].split('_')
    return name, unitName, rarity, weapon, element


def get_chara_skills(data):
    skillInfo = data.find_all('div', class_='skill_title')
    count = 1
    swordSkills = {}
    for skill in skillInfo[:3]:
        swordSkills[f'SS{count}'] = skill.find_all(
            'span', class_='ss_txt')[0].text
        count += 1
    count = 1
    battleSkills = {}
    for skill in skillInfo[3:]:
        battleSkills[f'BS{count}'] = skill.find_all(
            'span', class_='ss_txt')[0].text
        count += 1
    specialSkills = []
    specialSkillsInfo = data.find_all(
        'div', class_='carousel-cell')
    if len(specialSkillsInfo) > 0:
        specialSkillsInfo = specialSkillsInfo[-1].parent.find_all('img')
        for ssk in specialSkillsInfo:
            aux = ssk['src'].split('/')[-1]  # filename
            aux = aux[4:]  # remove ssk_
            aux = aux.split('.')[0]  # remove extension
            aux = aux.replace('_', ' ').title()
            specialSkills.append(aux)
    else:
        specialSkills = None
    return swordSkills, battleSkills, specialSkills


def get_chara_stats(data):
    info = data.find_all('div', class_='box_stats')[
        0].parent.find_all('script')
    unupgraded = True
    upgradedStats = None
    hp, deff, att, crit, mp = 0, 0, 0, 0, 0
    for charaRarity in info:
        rarityInfo = charaRarity.text  # get <script> with JSON
        rarityInfo = re.sub(r"[\n '+]", "", rarityInfo)  # parse JSON
        # get only stats JSON
        rarityInfo = re.findall(r'\((.*?)\)', rarityInfo)
        if len(rarityInfo) < 1:
            continue

        if len(rarityInfo) == 2 and rarityInfo[1] == 'canvas.char_gif':
            continue

        rarityInfo = rarityInfo[0]
        rarityInfo = eval(rarityInfo)  # to dict
        rarityInfo = rarityInfo['lb0']
        if unupgraded:
            hp = rarityInfo['hp']
            mp = rarityInfo['mp']
            att = rarityInfo['atk']
            deff = rarityInfo['def']
            crit = rarityInfo['crit']
            unupgraded = False
        else:
            upgradedStats = {
                'hp': rarityInfo['hp'],
                'mp':  rarityInfo['mp'],
                'atk': rarityInfo['atk'],
                'def': rarityInfo['def'],
                'crit': rarityInfo['crit']
            }
    return hp, mp, att, deff, crit, upgradedStats


def get_chara_data_from_html(data):
    name, unitName, rarity, weapon, element = get_chara_basics(data)
    swordSkills, battleSkills, specialSkills = get_chara_skills(data)
    hp, mp, att, deff, crit, upgradedStats = get_chara_stats(data)
    return Character(
        charaId=0,
        charaName=name,
        unitName=unitName,
        rarity=rarity,
        weapon=weapon,
        element=element,
        swordSkills=swordSkills,
        battleSkills=battleSkills,
        spceialSkills=specialSkills,
        hp=hp,
        mp=mp,
        atk=att,
        deff=deff,
        crit=crit,
        upgradedStats=upgradedStats
    )


def load_CSV(path):
    with open(path, 'r+', newline='', encoding="utf8") as file:
        reader = csv.reader(file)
        res = list(map(tuple, reader))
    return res[1:]


def load_chara_ids(path):
    data = load_CSV(path)
    ids = {}
    for entry in data:
        ids[fix_name(entry[1])] = int(fix_name(entry[0]))
    return ids


def write_JSON(data):
    with open('MdCharas.json', 'w+', encoding='utf-8') as f:
        f.write(data)


def webscrap():
    baseUrl = 'https://saomd.fanadata.com/character-'
    charaIds = load_chara_ids('data.csv')
    alldata = {}
    skipped = []
    num = 1
    while num < 1600:
        if num == 100:
            num = 880
        data = get_HTML_from_url(f'{baseUrl}{num}')
        if contains_chara_info(data):
            print(f'{baseUrl}{num}')
            chara = get_chara_data_from_html(data)
            if charaIds.get(f'{chara.unitName} {chara.charaName}'.strip()):
                chara.charaId = charaIds[f'{chara.unitName} {chara.charaName}'.strip(
                )]
                alldata[chara.charaId] = chara.__dict__()
            else:
                skipped.append(f'{chara.unitName} {chara.charaName}'.strip())
        else:
            print(num, end=', ')
        num += 1
    sorted_d = sorted(alldata.items(), key=operator.itemgetter(0))
    write_JSON(json.dumps(sorted_d, indent=4))
    pprint(skipped)


if __name__ == '__main__':
    # charaIds = load_chara_ids('data.csv')
    # data = get_HTML_from_url(f'https://saomd.fanadata.com/character-951')
    # chara = get_chara_data_from_html(data)
    # chara.charaId = charaIds[f'{chara.unitName} {chara.charaName}'.strip()]
    # alldata = {}
    # alldata[chara.charaId]=chara.__dict__()
    # write_JSON(json.dumps(alldata,indent=4))
    webscrap()
