from deprecated import deprecated


@deprecated
def contain_str(source: str, target: str):
    if len(target) == 0:
        return False
    else:
        count = 0
        index = 0
        for c in source:
            if c in target[index:]:
                index = target[index:].find(c)
                if index != len(target) - 1:
                    index = index + 1
                count = count + 1

        return count / len(target) > 0.5


@deprecated
def need_censor_ram_old(value, blacklist, whitelist, HanLP, sts):
    result = HanLP([value])
    coarse = result['tok/coarse'][0]
    potential = []
    needsCensor = []
    guaranteed = []
    for word in coarse:
        for censor in blacklist:
            contains = contain_str(word, censor)
            if contains is True:
                similarity = sts([(word, censor)])
                if 0.0 < similarity[0] < 0.6:
                    potential.append([word, censor, similarity[0]])
                elif 0.6 <= similarity[0] < 0.95:
                    needsCensor.append([word, censor, similarity[0]])
                elif similarity[0] > 0.95:
                    if is_in_whitelist(word, whitelist) is False:
                        guaranteed.append([word, censor, similarity[0]])

    return [potential, needsCensor, guaranteed]


def contain_str_new(source: str, target: str) -> float:
    if len(target) == 0:
        return False
    else:
        count = 0
        index = 0
        for c in source:
            if c in target[index:]:
                index = target[index:].find(c)
                if index != len(target) - 1:
                    index = index + 1
                count = count + 1

        return count / len(target)


def need_censor_ram_new(value, blacklist, whitelist, HanLP, sts):
    result = HanLP([value])
    coarse = result['tok/coarse'][0]
    potential = []
    needsCensor = []
    guaranteed = []
    for word in coarse:
        for censor in blacklist:
            contains = contain_str_new(word, censor)
            if contains == 1.0:
                guaranteed.append([word, censor, 1])
            elif 0.5 < contains < 1:
                similarity = sts([(word, censor)])
                if 0.0 < similarity[0] < 0.6:
                    potential.append([word, censor, similarity[0]])
                elif 0.6 <= similarity[0] < 0.95:
                    needsCensor.append([word, censor, similarity[0]])
                elif similarity[0] > 0.95:
                    if is_in_whitelist(word, whitelist) is False:
                        guaranteed.append([word, censor, similarity[0]])

    return [potential, needsCensor, guaranteed]


def remove(s: str):
    regrex: str = ('*#\\/+=-_<>——-·`。，、＇：∶；?‘’“”〝〞ˆˇ﹕︰﹔﹖﹑•¨….¸;！´？！～—ˉ｜‖＂〃｀@﹫¡¿﹏﹋﹌︴々﹟#﹩$﹠&﹪%*﹡﹢﹦﹤‐￣¯―﹨ˆ˜﹍﹎+=<＿_'
                   '-ˇ~﹉﹊（）〈〉‹›﹛﹜『』〖〗［］《》〔〕{}「」【】︵︷︿︹︽_﹁﹃︻︶︸﹀︺︾ˉ﹂﹄︼❝❞')
    result = s
    for char in regrex:
        result = result.replace(char, '')
    return result


def is_in_whitelist(source, whitelist):
    for word in whitelist:
        if source == word or contain_str(source, word):
            return True
    return False



