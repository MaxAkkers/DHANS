import random
import numpy as np

def despace(string):
    new_string = string.replace("  ", " ")

    if new_string == string:
        return string
    else:
        return despace(new_string)

def remove_terminals(tree):
    words = tree.split()
    new_words = []

    for word in words:
        if word[0] == "(":
            new_words.append("(")
        else:
            new_words.append(word)

    new_tree = " ".join(new_words)
    new_tree = new_tree.replace("(", " ( ").replace(")", " ) ")

    return despace(new_tree.strip())

def binarize_helper(tree):
    prev_word = ""

    for index, word in enumerate(tree):
        if word != "(" and word != ")":
            if prev_word == "(":
                if index < len(tree) - 1:
                    if tree[index + 1] == ")":
                        return binarize_helper(tree[:index - 1] + [tree[index]] + tree[index + 2:])
        prev_word = word

    for index, word in enumerate(tree):
        if word != "(" and word != ")":
            if prev_word == "(":
                if index < len(tree) - 2:
                    if tree[index + 1] != ")" and tree[index + 1] != "(" and tree[index + 2] == ")":
                        return binarize_helper(
                            tree[:index - 1] + [" ".join(tree[index - 1:index + 3])] + tree[index + 3:])
        prev_word = word

    for index, word in enumerate(tree):
        if word == ")":
            if index > 2:
                if tree[index - 1] != "(" and tree[index - 1] != ")" and tree[index - 2] != "(" and tree[
                    index - 2] != ")" and tree[index - 3] != "(" and tree[index - 3] != ")":
                    return binarize_helper(
                        tree[:index - 2] + ["( " + tree[index - 2] + " " + tree[index - 1] + " )"] + tree[index:])

    return tree

def valid_tree(binary_tree):
    if len(binary_tree) > 1:
        return False

    tree = binary_tree[0]
    parts = tree.split()

    count_brackets = 0
    for part in parts:
        if part == "(":
            count_brackets += 1
        elif part == ")":
            count_brackets -= 1

        if count_brackets < 0:
            return False

    if count_brackets == 0:
        return True


def binarize_tree(tree):
    unterminaled = remove_terminals(tree)

    words = unterminaled.split()

    tree = binarize_helper(words)
    if not valid_tree(tree):
        print("WRONG TREE")

    return binarize_helper(words)[0]


def generate_vp():
    verb = random.choice(pl_verbs)
    if verb in intransitive_verbs:
        return verb, "(VP (VBD " + verb + "))"
    else:
        obj = random.choice(nouns)

        return verb + " de " + obj, "(VP (VBD " + verb + ") (NP (DT de) (NN " + obj + ")))"


def parse_vp(vp):
    words = vp.split()

    if len(words) == 1:
        return "(VP (VBD " + words[0] + "))"
    else:
        return "(VP (VBD " + words[0] + ") (NP (DT de) (NN " + words[2] + ")))"


def parse_pp(pp):
    words = pp.split()

    if words[:2] == ["naast"]:
        return "(ADVP (JJ next) (PP (TO to) (NP (DT de) (" + noun_tag(words[-1]) + " " + words[-1] + "))))"
    elif words[:3] == ["voor"]:
        return "(PP (IN in) (NP (NP (NN front)) (PP (IN of) (NP (NP (DT de) (" + noun_tag(words[-1]) + " " + words[
            -1] + "))))))"
    else:
        return "(PP (IN " + words[0] + ") (NP (DT de) (" + noun_tag(words[-1]) + " " + words[-1] + ")))"


def generate_rc():
    rel = random.choice(rels)

    verb = random.choice(pl_verbs)
    if verb in pl_verbs:
        return rel + " " + verb
    else:
        arg = random.choice(nouns)
        if random.randint(0, 1) == 0:
            return rel + " de " + arg + " " + verb
        else:
            return rel + " " + verb + " de " + arg


def noun_tag(noun):
    if noun in nouns_sg or noun in food_words or noun in location_nouns or noun in location_nouns_b or noun in won_objects or noun in read_wrote_objects:
        return "NN"
    elif noun in nouns_pl or noun in nouns_het:
        return "NNS"
    else:
        return "NN"


def parse_rc(rc):
    words = rc.split()

    if words[0] == "dat":
        if len(words) == 2:
            return "(SBAR (WHNP (WDT dat)) (S (VP (VBD " + words[1] + "))))"
        else:
            if words[1] == "de":
                return "(SBAR (WHNP (WDT dat)) (S (NP (DT de) (" + noun_tag(words[2]) + " " + words[
                    2] + ")) (VP (VBD " + words[3] + "))))"
            else:
                return "(SBAR (WHNP (WDT dat)) (S (VP (VBD " + words[1] + ") (NP (DT de) (" + noun_tag(
                    words[3]) + " " + words[3] + ")))))"

    elif words[0] == "wie":
        if len(words) == 2:
            return "(SBAR (WHNP (WP wie)) (S (VP (VBD " + words[1] + "))))"
        else:
            if words[1] == "de":
                return "(SBAR (WHNP (WP wie)) (S (NP (DT de) (" + noun_tag(words[2]) + " " + words[
                    2] + ")) (VP (VBD " + words[3] + "))))"
            if words[2] == "met de":
                print("hoi")
                return "(SBAR (WHNP (WP wie)) (S (NP (DT de) (" + noun_tag(words[3]) + " " + words[
                    2] + ")) (VP (VBD " + words[3] + "))))"
            else:
                return "(SBAR (WHNP (WP wie)) (S (VP (VBD " + words[1] + ") (NP (DT de) (" + noun_tag(words[3]) + " " + \
                       words[3] + ")))))"

    else:
        print("INVALID RELATIVIZER")


def template_filler(template_list):
    probs = []
    templates = []

    for template_pair in template_list:
        probs.append(template_pair[0])
        templates.append(template_pair[1])

    template_index = np.random.choice(range(len(templates)), p=probs)
    template_tuple = templates[template_index]

    template = template_tuple[0]
    hypothesis_template = template_tuple[1]
    template_tag = template_tuple[2]
    print(template_tag)
    premise_tree_template = template_tuple[3]
    hypothesis_tree_template = template_tuple[4]

    premise_list = []
    index_dict = {}

    for (index, element) in template:
        if element == "VP":
            vp, vp_parse = generate_vp()
            premise_list.append(vp)
            index_dict[index] = vp

        elif element == "RC":
            rc = generate_rc()
            premise_list.append(rc)
            index_dict[index] = rc

        elif "vobj" in element:
            obj = random.choice(object_dict[index_dict[int(element[-1])]])
            premise_list.append(obj)
            index_dict[index] = obj

        elif isinstance(element, str):
            premise_list.append(element)
            index_dict[index] = element

        else:
            word = random.choice(element)
            premise_list.append(word)
            index_dict[index] = word

    hypothesis_list = []
    for ind in hypothesis_template:
        if template_tag == "temp37" or template_tag == "temp38":
            if index_dict[ind] in pl_ge_verbs:
                hypothesis_list.append(index_dict[ind].replace('ge', ''))
            else:
                hypothesis_list.append(index_dict[ind])
        elif index_dict[ind] in noun_switch and template_tag == "temp1" or index_dict[ind] in noun_switch and template_tag == "temp2":
            hypothesis_list.append((random.choice(nouns)))
        elif index_dict[ind] in pl_verbs_switch and template_tag == "temp4":
            hypothesis_list.append((random.choice(pl_verbs)))
        elif template_tag == "temp3" and index_dict[ind] in nouns_sg:
            hypothesis_list.append((random.choice(bijv_naam)))
            hypothesis_list.append(index_dict[ind])
        else:
            hypothesis_list.append(index_dict[ind])

    premise_tree_list = []
    hypothesis_tree_list = []
    for elt in premise_tree_template:
        if isinstance(elt, int):
            premise_tree_list.append(index_dict[elt])
        elif elt[:3] == "prc":
            comma_split = elt.split(",")
            start_ind = int(comma_split[1])
            end_ind = int(comma_split[2])
            rc_tree = ""
            for i in range(start_ind, end_ind + 1):
                rc_tree += index_dict[i] + " "
            premise_tree_list.append(parse_rc(rc_tree.strip()))
        elif elt[:2] == "nn":
            comma_split = elt.split(",")
            this_ind = int(comma_split[1])
            premise_tree_list.append(noun_tag(index_dict[this_ind]))
        elif elt[:3] == "pvp":
            comma_split = elt.split(",")
            this_ind = int(comma_split[1])
            premise_tree_list.append(parse_vp(index_dict[this_ind]))
        elif elt[:3] == "ppp":
            comma_split = elt.split(",")
            start_ind = int(comma_split[1])
            end_ind = int(comma_split[2])
            pp_tree = ""
            for i in range(start_ind, end_ind + 1):
                pp_tree += index_dict[i] + " "
            premise_tree_list.append(parse_pp(pp_tree.strip()))
        elif elt[:3] == "cap":
            comma_split = elt.split(",")
            this_ind = int(comma_split[1])
            this_word = index_dict[this_ind]
            premise_tree_list.append(this_word[0].upper() + this_word[1:])
        else:
            premise_tree_list.append(elt)

    for elt in hypothesis_tree_template:
        if isinstance(elt, int):
            hypothesis_tree_list.append(index_dict[elt])
        elif elt[:3] == "prc":
            comma_split = elt.split(",")
            start_ind = int(comma_split[1])
            end_ind = int(comma_split[2])
            rc_tree = ""
            for i in range(start_ind, end_ind + 1):
                rc_tree += index_dict[i] + " "
            hypothesis_tree_list.append(parse_rc(rc_tree.strip()))
        elif elt[:2] == "nn":
            comma_split = elt.split(",")
            this_ind = int(comma_split[1])
            hypothesis_tree_list.append(noun_tag(index_dict[this_ind]))
        elif elt[:3] == "pvp":
            comma_split = elt.split(",")
            this_ind = int(comma_split[1])
            hypothesis_tree_list.append(parse_vp(index_dict[this_ind]))
        elif elt[:3] == "cap":
            comma_split = elt.split(",")
            this_ind = int(comma_split[1])
            this_word = index_dict[this_ind]
            hypothesis_tree_list.append(this_word[0].upper() + this_word[1:])
        else:
            hypothesis_tree_list.append(elt)

    premise_tree = "".join(premise_tree_list)
    hypothesis_tree = "".join(hypothesis_tree_list)
    return postprocess(" ".join(premise_list)), postprocess(
        " ".join(hypothesis_list)), template_tag, premise_tree, hypothesis_tree, binarize_tree(
        premise_tree), binarize_tree(hypothesis_tree)


def postprocess(sentence):
    sentence = sentence[0].upper() + sentence[1:]
    return sentence

nouns_sg = ["zanger","tiener", "motorcrossrijder", "goochelaar", "tovenaar", "interviewer", "ruiter",  "motorracer", "priester",
             "autocoureur", "bruid", "gamer"]

nouns_pl = ["fotografen", "klimmers", "mannen", "motorrijders","spelers", "boa's",  "hardlopers", "jongvolwassenen", "mimespelers",  "dochters", "leerlingen","vrouwen",
"studenten", "jongens", "soldaten",  "fietsers"]
noun_switch = ["fotografen", "klimmers", "mannen", "motorrijders","spelers", "boa's",  "hardlopers", "jongvolwassenen", "mimespelers",  "dochters", "leerlingen","vrouwen",
"studenten", "jongens", "soldaten",  "fietsers"]

nouns = nouns_pl
pl_verbs = ["zagen", "breken", "knuffelen", "studeren",
            "verlaten", "schoppen", "trekken", "ontwijken", "snuffelen", "gooien",
            "worstelen", "trouwen", "redden", "leren", "duelleren", "vangen", "verpletteren", "dragen", "telefoneren",
            "voeren","tekenen","borstelen"]
pl_verbs_switch = ["zagen", "breken", "knuffelen", "grazen", "studeren",
            "verlaten", "stillen", "schoppen", "trekken", "ontwijken", "snuffelen", "gooien",
            "worstelen", "trouwen", "redden", "leren", "werken", "duelleren", "vangen", "zwemmen", "verpletteren", "dragen", "telefoneren",
            "voeren","tekenen","borstelen",]
de_verbs = ["zagen", "breken", "knuffelen", "studeren",
            "verlaten", "schoppen", "trekken", "ontwijken", "snuffelen", "gooien",
            "worstelen", "trouwen", "redden", "leren", "werken", "duelleren", "vangen", "zwemmen", "verpletteren", "dragen", "telefoneren",
            "voeren", "lezen", "praten", "winnen", "lopen","tekenen","borstelen"]
sg_verbs = ["perst", "plukt", "danst", "laadt", "blies"]
bijv_naam = ["begroeide", "geverfde", "gestreepte", "getalenteerde", "onbeschermde", "gelakte", "gekleurde"]

pl_ge_verbs = ["geslagen", "geholpen", "gescheiden","getrokken", "gesneden", "gegoten", "gegeven", "gebeten"]

passive_verbs = ["berekenen","genieten", "loungen","vervelen",  "stylen"]

nps_verbs = ["wist"]
npz_verbs = ["geduwd", "gestikt", "gestopt"]
npz_verbs_plural = ["genezen"]
understood_argument_verbs = ["lopen", "winnen", "praten", "lezen"]
# All appear at least 100 times with both transitive and intransitive frames

preps = ["dichtbij", "achter", "voor", "naast"]  # Each appears at least 100 times in MNLI
conjs = ["terwijl", "als", "voor"]
food_words = ["courgette", "gehakt", "pizza", "ham", "pasta", "soep", "ui"]
location_nouns = ["buurt", "land", "stad", "bos", "tuin", "woestijn"]
location_nouns_b = ["sportschool"]
won_objects = ["race", "wedstrijd", "oorlog", "kickboxsgevecht", "beker"]
read_wrote_objects = ["boek", "kolommen", "briefje", "toneelstuk", "toespraak"]
adjs = ["ontspannen", "schoon","gretig", "afwezig", "moe", "angstig", "hard", "verbazend", "akoestisch", "terecht", "geschikt", "gulzig", "aangenaam", "doelloos", "prachtig", "echt", "voorbij", "leeg", "laag", "uitdagend", "intens", "geduldig", "blootsvoets", "gezond", "elektrisch", "oud", "wenkbrauw", "nerveus", "geruisloos", "harig", "zwart-wit", "onvermoeibaar", "onstuimig", "hartelijk", "ademloos", "dicht", "herhaaldelijk", "rechts", "goed", "naakt", "bergafwaarts", "vrolijk", "voorzichtig", "groot", "gestaag", "hersenloos", "erg", "onbevreesd", "wakker", "goddelijk", "atletisch", "elegant", "pronkt", "langzaam", "magisch", "waarschijnlijk", "klaar", "oranje", "slim", "flips", "bont", "aziatisch", "rauw", "woedend", "fel", "hoog", "beton", "sluw", "gevaarlijk", "links", "kunstmatig", "precies", "nieuwsgierig", "hevig", "luid", "rustig", "vuil", "abrupt", "bewegingsloos", "rotsachtig", "ondervoed", "moedig", "amusant", "comfortabel", "sierlijk", "onhandig", "vies", "lusteloos", "schattig", "verticaal", "aantrekkelijk", "riskant", "heel", "schoenloos", "vast", "los", "hongerig", "bewaterd", "ver", "achteloos", "roerloos", "topless", "enthousiast", "aandachtig", "gelukkig", "bezig", "beige", "serieus", "krachtig", "hartstochtelijk", "zorgvuldig", "onschuldig", "lui", "moeiteloos", "stil", "vakkundig", "mechanisch", "boos", "roekeloos", "immobiel", "kort", "vurig", "haastig", "luidruchtig", "moeilijk", "lang", "trots", "open"]  # All at least 100 times in MNLI
adj_comp_nonent = ["bang"]
adj_comp_ent = ["sorry", "scherp"]
const_adv = ["na", "voor", "tijdens", "vanaf"]
const_quot_entailed = ["wist"]
rels = ["wie"]
solo = ["alleen", "enkel"]
contradiction = ["geen"]
ent_complement_nouns = ["tijd"]
object_dict = {}
object_dict["maken"] = food_words
object_dict["eten"] = food_words
object_dict["loopt"] = location_nouns
object_dict["winnen"] = won_objects
object_dict["leest"] = read_wrote_objects
object_dict["gelezen"] = read_wrote_objects

advs_embed_entailed = ["achter", "met", "tegenover", "bovenop", "van", "onder", "tussen", "tegen", "voor", "uit", "bij","naast", "boven"]
advs_outside_entailed = ["achter", "met", "tegenover", "achterin", "bovenop", "dichtbij", "van", "vol", "naar", "onder", "tot", "tussen", "langs", "tegen", "door", "voor", "in", "binnen", "buiten", "uit", "zonder", "bij", "vanuit", "op", "te", "naast", "beneden", "boven", "na", "heen", "tijdens", "om", "over", "vanaf", "aan", "via", "rond"]

# Contradiction entailment

con_noun_switch_template = [(0.5, (
    [(0, contradiction), (1, nouns), (2, de_verbs), (3, "met de"), (4, noun_switch), (5, ".")], [1, 2, 3, 4, 5], "temp1",
    ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,4", " ", 4, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"])),
    (0.5, (
    [(0, contradiction), (1, noun_switch), (2, de_verbs), (3, "met de"), (4, nouns), (5, ".")], [1, 2, 3, 4, 5], "temp2",
    ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,4"," ", 4, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1"," ", 1, "))) (. .)))"]))
]

con_bijv_template = [(1.0, (
    [(0, "de"), (1, nouns_sg), (2, sg_verbs), (3, ".")], [0, 1, 2, 3], "temp3",
    ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"]))]

con_verb_switch = [(1.0, (
    [(0, "de"), (1, bijv_naam), (2, nouns), (3, pl_verbs_switch), (4, "niet"), (5, ".")], [0, 1, 2, 3, 5], "temp4",
    ["(ROOT (S (NP (DT de) (", "nn,2", " ", 2, ")) (VP (VBD ", 3, ") (NP (DT de) (", "nn,2", " ", 2, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,2", " ", 2, ")) (VP (VBD ", 3, ") (NP (DT de) (", "nn,2", " ", 2, "))) (. .)))"]))]

prep_con_template = [(1.0, (
[(0, contradiction), (1, nouns), (2, de_verbs), (3, preps), (4, "de"), (5, nouns), (6, ".")], [4, 5, 2, 3, 4, 1, 6], "temp5",
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,5", " ", 5, "))) (. .)))"],
["(ROOT (S (NP (DT de) (", "nn,5", " ", 5, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"]))]

con_prep_template = [(1.0, (
[(0, contradiction), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, preps), (6, "de"), (7, nouns)], [3, 4, 2, 6, 7], "temp6",
["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,7", " ", 7, "))) (. .)))"],
["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,4", " ", 4, "))) (. .)))"]))]

# Contradiction entailment
con_template = [(1.0, (
[(0, contradiction), (1, nouns), (2, pl_verbs), (3, ".")], [1, 2, 3], "temp7",
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"],
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"]))]

con_template_en = [(1.0, (
[(0, "de"), (1, nouns), (2, "en"), (3, "de"), (4, nouns), (5, pl_verbs), (6, "niet"), (7, ".")], [0, 1, 2, 3, 4, 5, 7], "temp8",
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 5, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"],
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 5, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"]))]

con_template_bijv = [(1.0, (
[(0, "de"), (1, bijv_naam), (2, nouns), (3, de_verbs), (4, "niet"), (5, "met de"), (6, bijv_naam), (7, nouns), (8, ".")], [0, 1, 2, 3, 5, 6, 7, 8], "temp9",
["(ROOT (S (NP (DT de) (", "nn,2", " ", 2, ")) (VP (VBD ", 3, ") (NP (DT de) (", "nn,7", " ", 7, "))) (. .)))"],
["(ROOT (S (NP (DT de) (", "nn,2", " ", 2, ")) (VP (VBD ", 3, ") (NP (DT de) (", "nn,7", " ", 7, "))) (. .)))"]))]

# Lexical Overlap: Simple sentence entailment
lex_simple_templates = [(1.0, (
[(0, "de"), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, ".")], [3, 4, 2, 0, 1, 5], "temp10",
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,4", " ", 4, "))) (. .)))"],
["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"]))]

# Lexical Overlap: Preposition on subject
lex_prep_templates = [
    (1.0 / 3, (
    [(0, "de"), (1, nouns), (2, preps), (3, "de"), (4, nouns), (5, pl_verbs), (6, "de"), (7, nouns),
     (8, ".")], [3, 4, 5, 0, 1, 8], "temp11",
    ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "ppp,2,4", ") (VP (VBD ", 5, ") (NP (DT de) (", "nn,7", " ",
     7, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 5, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"])),
    (1.0 / 3, (
    [(0, "de"), (1, nouns), (2, preps), (3, "de"), (4, nouns), (5, pl_verbs), (6, "de"), (7, nouns),
     (8, ".")], [6, 7, 5, 0, 1, 8], "temp12",
    ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "ppp,2,4", ") (VP (VBD ", 5, ") (NP (DT de) (", "nn,7", " ",
     7, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,7", " ", 7, ")) (VP (VBD ", 5, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"])),
    (1.0 / 3, (
    [(0, "de"), (1, nouns), (2, preps), (3, "de"), (4, nouns), (5, pl_verbs), (6, "de"), (7, nouns),
     (8, ".")], [6, 7, 5, 3, 4, 8], "temp13",
    ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "ppp,2,4", ") (VP (VBD ", 5, ") (NP (DT de) (", "nn,7", " ",
     7, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,7", " ", 7, ")) (VP (VBD ", 5, ") (NP (DT de) (", "nn,4", " ", 4, "))) (. .)))"])),

]

# Lexical Overlap: Relative clause on subject
lex_rc_templates = [
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (2, rels), (3, "de"), (4, nouns), (5, pl_verbs), (6, de_verbs),
     (7, "met de"), (8, nouns), (9, ".")], [3, 4, 6, 7, 1, 9], "temp14",
    ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "prc,2,5", ") (VP (VBD ", 6, ") (NP (DT de) (", "nn,8", " ",
     8, "))) (. .)))"],["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 6, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"]))
    ,
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (2, rels), (3, "de"), (4, nouns), (5, pl_verbs), (6, de_verbs),
     (7, "met de"), (8, nouns), (9, ".")], [3, 8, 6, 7, 1, 9], "temp15",
    ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "prc,2,5", ") (VP (VBD ", 6, ") (NP (DT de) (", "nn,8", " ",
     8, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,8", " ", 8, ")) (VP (VBD ", 6, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"])),
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (10, "met"), (2, rels), (3, "de"), (4, nouns), (5, de_verbs), (6, de_verbs),
     (7, "met de"), (8, nouns), (9, ".")], [3, 8, 6, 7, 4, 9], "temp16",
    ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "prc,2,5", ") (VP (VBD ", 6, ") (NP (DT de) (", "nn,8", " ",
     8, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,8", " ", 8, ")) (VP (VBD ", 6, ") (NP (DT de) (", "nn,4", " ", 4, "))) (. .)))"])),
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (2, rels), (3, pl_verbs), (4, "de"), (5, nouns), (6, de_verbs),
     (7, "met de"), (8, nouns), (9, ".")], [4, 5, 6, 7, 1, 9], "temp17",
    ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "prc,2,5", ") (VP (VBD ", 6, ") (NP (DT de) (", "nn,8", " ",
     8, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,5", " ", 5, ")) (VP (VBD ", 6, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"])),
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (2, rels), (4, "de"), (5, nouns), (3, pl_verbs), (6, de_verbs),
     (7, "met de"), (8, nouns), (9, ".")], [4, 8, 6, 7, 1, 9], "temp18",
    ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "prc,2,5", ") (VP (VBD ", 6, ") (NP (DT de) (", "nn,8", " ",
     8, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,8", " ", 8, ")) (VP (VBD ", 6, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"])),
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (2, rels), (4, "de"), (5, nouns),(3, pl_verbs) , (6, de_verbs),
     (7, "met de"), (8, nouns), (9, ".")], [4, 8, 6, 7, 5, 9], "temp19",
    ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "prc,2,5", ") (VP (VBD ", 6, ") (NP (DT de) (", "nn,8", " ",
     8, "))) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,8", " ", 8, ")) (VP (VBD ", 6, ") (NP (DT de) (", "nn,5", " ", 5, "))) (. .)))"])),
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, rels), (6, de_verbs),
     (7, "met de"), (8, nouns), (9, ".")], [3, 4, 2, 7, 1, 9], "temp20",
    ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4, ")) ",
     "prc,5,8", ")) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"])),
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, rels), (6, de_verbs),
     (7, "met de"), (8, nouns), (9, ".")], [3, 4, 2, 7, 8, 9], "temp21",
    ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4, ")) ",
     "prc,5,8", ")) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,8", " ", 8, "))) (. .)))"])),
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, rels), (6, de_verbs),
     (7, "met de"), (8, nouns), (9, ".")], [3, 8, 2, 7, 1, 9], "temp22",
    ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4, ")) ",
     "prc,5,8", ")) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,8", " ", 8, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"])),
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (2, de_verbs), (3, "met de"), (4, nouns), (5, rels), (6, "de"), (7, nouns),
     (8, pl_verbs), (9, ".")], [0, 4, 2, 3, 1, 9], "temp23",
    ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4, ")) ",
     "prc,5,8", ")) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"])),
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (2, de_verbs), (3, "met de"), (4, nouns), (5, rels), (6, "de"), (7, nouns),
     (8, pl_verbs), (9, ".")], [0, 4, 2, 3, 7, 9], "temp24",
    ["(ROOT (S (NP (DT De) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4, ")) ",
     "prc,5,8", ")) (. .)))"],
    ["(ROOT (S (NP (DT De) (", "nn,4", " ", 4, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,7", " ", 7, "))) (. .)))"])),
    (1.0 / 12, (
    [(0, "de"), (1, nouns), (2, de_verbs), (3, "met de"), (4, nouns), (5, rels), (6, "de"), (7, nouns),
     (8, pl_verbs), (9, ".")], [6, 7, 2, 3, 1, 9], "temp25",
    ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4, ")) ",
     "prc,5,8", ")) (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,7", " ", 7, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,1", " ", 1, "))) (. .)))"]))
]

# Lexical Overlap: Conjunctions
lex_conj_templates = [
    (0.25, ([(0, "de"), (1, nouns), (2, "en"), (3, "de"), (4, nouns), (5, pl_verbs), (6, "de"), (7, nouns),
             (8, ".")], [0, 1, 5, 3, 4, 8], "temp26",
            ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) (CC and) (NP (DT de) (", "nn,4", " ", 4,
             "))) (VP (VBD ", 5, ") (NP (DT de) (", "nn,7", " ", 7, "))) (. .)))"],
            ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 5, ") (NP (DT de) (", "nn,4", " ", 4,
             "))) (. .)))"])),
    (0.25, ([(0, "de"), (1, nouns), (2, "en"), (3, "de"), (4, nouns), (5, pl_verbs), (6, "de"), (7, nouns),
             (8, ".")], [3, 4, 5, 0, 1, 8], "temp27",
            ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) (CC and) (NP (DT de) (", "nn,4", " ", 4,
             "))) (VP (VBD ", 5, ") (NP (DT de) (", "nn,7", " ", 7, "))) (. .)))"],
            ["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 5, ") (NP (DT de) (", "nn,1", " ", 1,
             "))) (. .)))"])),
    (0.25, ([(0, "de"), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, "en"), (6, "de"), (7, nouns),
             (8, ".")], [3, 4, 2, 6, 7, 8], "temp28",
            ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4,
             ")) (CC and) (NP (DT de) (", "nn,7", " ", 7, ")))) (. .)))"],
            ["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,7", " ", 7,
             "))) (. .)))"])),
    (0.25, ([(0, "de"), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, "and"), (6, "de"), (7, nouns),
             (8, ".")], [6, 7, 2, 3, 4, 8], "temp29",
            ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4,
             ")) (CC and) (NP (DT de) (", "nn,7", " ", 7, ")))) (. .)))"],
            ["(ROOT (S (NP (DT de) (", "nn,7", " ", 7, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,4", " ", 4,
             "))) (. .)))"]))
]

# Lexical Overlap: Relative clause
lex_rc_ent_templates = [
    (0.25, ([(0, "de"), (1, nouns), (2, advs_embed_entailed), (3, rels), (4, "de"), (5, nouns), (6, pl_verbs), (7, pl_verbs),
             (8, "de"), (9, nouns), (10, ".")], [4, 5, 6, 2, 0, 1, 10], "temp30",
            ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "prc,3,6", ") (VP (VBD ", 6, ") (NP (DT de) (",
             "nn,9", " ", 9, "))) (. .)))"],
            ["(ROOT (S (NP (DT de) (", "nn,5", " ", 5, ")) (VP (VBD ", 6, ") (NP (DT de) (", "nn,1", " ", 1,
             "))) (. .)))"])),
    (0.25, ([(0, "de"), (1, nouns), (2, advs_embed_entailed), (3, rels), (4, "de"), (5, nouns), (6, pl_verbs), (7, pl_verbs),
             (8, "de"), (9, nouns), (10, ".")], [0, 1, 6, 2, 4, 9, 10], "temp31",
            ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "prc,3,6", ") (VP (VBD ", 6, ") (NP (DT de) (",
             "nn,9", " ", 9, "))) (. .)))"],
            ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 6, ") (NP (DT de) (", "nn,5", " ", 5,
             "))) (. .)))"])),
    (0.25, ([(0, "de"), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, rels), (6, pl_verbs),
             (7, advs_embed_entailed), (8, "de"), (9, nouns), (10, ".")], [3, 4, 6, 7, 8, 9, 10], "temp32",
            ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4,
             ")) ", "prc,5,8", ")) (. .)))"],
            ["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) (VP (VBD ", 6, ") (NP (DT de) (", "nn,9", " ", 9,
             "))) (. .)))"])),
    (0.25, ([(0, "de"), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, rels), (6, advs_embed_entailed), (7, "de"), (8, nouns),
             (9, pl_verbs), (10, ".")], [6, 7, 8, 6, 3, 4, 10], "temp33",
            ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4,
             ")) ", "prc,5,8", ")) (. .)))"],
            ["(ROOT (S (NP (DT de) (", "nn,8", " ", 8, ")) (VP (VBD ", 9, ") (NP (DT de) (", "nn,4", " ", 4,
             "))) (. .)))"]))]

# Lexical Overlap: Across PP
lex_cross_pp_ent_templates = [(1.0, (
[(0, "de"), (1, nouns), (2, preps), (3, "de"), (4, nouns), (5, pl_verbs), (6, "de"), (7, nouns), (8, ".")],
[0, 1, 5, 6, 7, 8], "temp34",
["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "ppp,2,4", ") (VP (VBD ", 5, ") (NP (DT de) (", "nn,7", " ", 7,
 "))) (. .)))"],
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 5, ") (NP (DT de) (", "nn,7", " ", 7, "))) (. .)))"]))]

# Lexical Overlap: Conjunctions
lex_ent_conj_templates = [
    (0.5, ([(0, "de"), (1, nouns), (2, "en"), (3, "de"), (4, nouns), (5, pl_verbs), (6, "de"), (7, nouns),
            (8, ".")], [0, 1, 5, 6, 7, 8], "temp35",
           ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) (CC and) (NP (DT de) (", "nn,4", " ", 4,
            "))) (VP (VBD ", 5, ") (NP (DT de) (", "nn,7", " ", 7, "))) (. .)))"],
           ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 5, ") (NP (DT de) (", "nn,7", " ", 7,
            "))) (. .)))"])),
    (0.5, ([(0, "de"), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, "en"), (6, "de"), (7, nouns),
            (8, ".")], [0, 1, 2, 6, 7, 8], "temp36",
           ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4,
            ")) (CC and) (NP (DT de) (", "nn,7", " ", 7, ")))) (. .)))"],
           ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,7", " ", 7,
            "))) (. .)))"]))
]

# Lexical Overlap: Across adverb
# Lexical Overlap: Passive
lex_ent_pass_templates = [
    (0.5, ([(0, "de"), (1, nouns_sg), (2, "is"), (3, pl_ge_verbs), (4, "door"), (5, "de"), (6, nouns), (7, ".")],
           [5, 6, 3, 0, 1, 7], "temp37",
           ["(ROOT (S (NP (DT de) (NN ", 1, ")) (VP (VBD was) (VP (VBN ", 3, ") (PP (IN by) (NP (DT de) (", "nn,6",
            " ", 6, "))))) (. .)))"],
           ["(ROOT (S (NP (DT de) (", "nn,6", " ", 6, ")) (VP (VBD ", 3, ") (NP (DT de) (", "nn,1", " ", 1,
            "))) (. .)))"])),
    (0.5, ([(0, "de"), (1, nouns_pl), (2, "zijn"), (3, pl_ge_verbs), (4, "door"), (5, "de"), (6, nouns), (7, ".")],
           [5, 6, 3, 0, 1, 7], "temp38",
           ["(ROOT (S (NP (DT de) (NNS ", 1, ")) (VP (VBD were) (VP (VBN ", 3, ") (PP (IN by) (NP (DT de) (", "nn,6",
            " ", 6, "))))) (. .)))"],
           ["(ROOT (S (NP (DT de) (", "nn,6", " ", 6, ")) (VP (VBD ", 3, ") (NP (DT de) (", "nn,1", " ", 1,
            "))) (. .)))"]))
]

# Subsequence: PP on subject
subseq_pp_on_subj_templates = [(1.0, (
[(0, "de"), (1, nouns), (2, preps), (3, "de"), (4, nouns), (5, "zijn"), (6, pl_ge_verbs), (7, ".")], [3, 4, 5, 6, 7], "temp39",
["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "ppp,2,4", ") ", "pvp,6", " (. .)))"],
["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) ", "pvp,6", " (. .)))"]))]

# Subsequence: Rel clause on subject
subseq_rel_on_subj_templates = [(1.0, (
[(0, "de"), (1, nouns), (2, rels), (3, "de"), (4, nouns), (5, pl_verbs), (6, pl_verbs), (7, "de"), (8, nouns), (9, ".")], [3, 4, 6, 7, 8, 9],
"temp40", ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) ", "prc,2,5", ") ", "pvp,6", " (. .)))"],
["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) ", "pvp,6", " (. .)))"]))]

# Subsequence: Conjoined subject
subseq_conj_templates = [
    (1.0, (
    [(0, "de"), (1, nouns), (2, "en"), (3, "de"), (4, nouns), (5, pl_verbs), (6, ".")], [3, 4, 5, 6], "temp41",
    ["(ROOT (S (NP (NP (DT de) (", "nn,1", " ", 1, ")) (CC and) (NP (DT de) (", "nn,4", " ", 4, "))) ", "pvp,5",
     " (. .)))"], ["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) ", "pvp,5", " (. .)))"])),
]

# Subsequence: Modified plural subject
subseq_adj_templates = [(1.0, ([(0, bijv_naam), (1, nouns_pl), (2, pl_verbs), (3, ".")], [1, 2, 3], "temp42",
                               ["(ROOT (S (NP (JJ ", "cap,0", ") (NNS ", 1, ")) ", "pvp,2", " (. .)))"],
                               ["(ROOT (S (NP (NNS ", "cap,1", ")) ", "pvp,2", " (. .)))"]))]

# Subsequence: Relative clause
subseq_rel_on_obj_templates = [(1.0, (
[(0, "de"), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, rels), (6, pl_verbs), (7, ".")], [0, 1, 2, 3, 4, 7],
"temp43",
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4, ")) ", ") (NP (NP (DT de) (",
 ")) (. .)))"],
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,4", " ", 4, "))) (. .)))"]))]

# Subsequence: PP
subseq_pp_on_obj_templates = [(1.0, (
[(0, "de"), (1, nouns), (2, pl_verbs), (3, "de"), (4, nouns), (5, preps), (6, "de"), (7, nouns), (8, ".")],
[0, 1, 2, 3, 4, 8], "temp44",
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (NP (DT de) (", "nn,4", " ", 4, ")) ", "ppp,5,7",
 ")) (. .)))"],
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (NP (DT de) (", "nn,4", " ", 4, "))) (. .)))"]))]

# Constituent: If
const_under_if_templates = [
    (1.0, (
    [(0, "als"), (1, "de"), (2, nouns), (3, pl_verbs), (4, ","), (5, pl_verbs), (6, "de"), (7, nouns), (8, ".")],
    [1, 2, 3, 8], "temp45",
    ["(ROOT (S (SBAR (IN Whether) (CC or) (RB not) (S (NP (DT de) (", "nn,2", " ", 2, ")) ", "pvp,3",
     ")) (, ,) (S (NP (DT de) (", "nn,7", " ", 7, ")) ", "pvp,5", ") (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,2", " ", 2, ")) ", "pvp,3", " (. .)))"]))
]

# Constituent: Disjunction
const_disj_templates = [
    (0.5, (
    [(0, "de"), (1, nouns), (2, pl_verbs), (3, "of"), (4, "de"), (5, nouns), (6, pl_verbs), (7, ".")], [0, 1, 2, 7],
    "temp46",
    ["(ROOT (S (S (NP (DT de) (", "nn,1", " ", 1, ")) ", "pvp,2", ") (, ,) (CC or) (S (NP (DT de) (", "nn,5", " ", 5,
     ")) ", "pvp,6", ") (. .)))"], ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) ", "pvp,2", " (. .)))"])),
    (0.5, (
    [(0, "de"), (1, nouns), (2, pl_verbs), (3, "of"), (4, "de"), (5, nouns), (6, pl_verbs), (7, ".")], [4, 5, 6, 7],
    "temp47",
    ["(ROOT (S (S (NP (DT de) (", "nn,1", " ", 1, ")) ", "pvp,2", ") (, ,) (CC or) (S (NP (DT de) (", "nn,5", " ", 5,
     ")) ", "pvp,6", ") (. .)))"], ["(ROOT (S (NP (DT de) (", "nn,5", " ", 5, ")) ", "pvp,6", " (. .)))"]))
]

const_adv_outside_templates = [
    (1.0, ([(0, "als"), (1, "de"), (2, nouns), (3, "de"), (4,  nouns), (5, pl_verbs), (6, ","), (7, pl_verbs), (8, "de"), (9, nouns), (10, ".")],
    [8, 9, 7, 10], "temp48",
    ["(ROOT (S (SBAR (PP (IN In) (NP (NN case))) (S (NP (DT de) (", "nn,2", " ", 2, ")) ", "pvp,5",
     ")) (, ,) (S (NP (DT de) (", "nn,9", " ", 9, ")) ", "pvp,7", ") (. .)))"],
    ["(ROOT (S (NP (DT de) (", "nn,4", " ", 4, ")) ", "pvp,7", " (. .)))"]))
]

# Constituent: Knew
const_quot_ent_templates = [(1.0, (
[(0, "de"), (1, nouns_sg), (2, "ziet"), (3, "dat"), (4, "de"), (5, nouns), (6, pl_verbs), (7, ".")],
[4, 5, 6, 7], "temp49",
["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) (VP (VBD ", 2, ") (SBAR (IN dat) (S (NP (DT de) (", "nn,5", " ", 5,
 ")) ", "pvp,6", "))) (. .)))"], ["(ROOT (S (NP (DT de) (", "nn,5", " ", 5, ")) ", "pvp,6", " (. .)))"]))]

# Constituent: Conjunction
const_conj_templates = [
    (0.5, ([(0, "de"), (1, nouns), (2, pl_verbs), (3, "en"), (4, "de"), (5, nouns), (6, pl_verbs), (7, ".")],
           [0, 1, 2, 7], "temp50",
           ["(ROOT (S (S (NP (DT de) (", "nn,1", " ", 1, ")) ", "pvp,2", ") (, ,) (CC and) (S (NP (DT de) (", "nn,5",
            " ", 5, ")) ", "pvp,6", ") (. .)))"],
           ["(ROOT (S (NP (DT de) (", "nn,1", " ", 1, ")) ", "pvp,2", " (. .)))"])),
    (0.5, ([(0, "de"), (1, nouns), (2, pl_verbs), (3, "en"), (4, "de"), (5, nouns), (6, pl_verbs), (7, ".")],
           [4, 5, 6, 7], "temp51",
           ["(ROOT (S (S (NP (DT de) (", "nn,1", " ", 1, ")) ", "pvp,2", ") (, ,) (CC and) (S (NP (DT de) (", "nn,5",
            " ", 5, ")) ", "pvp,6", ") (. .)))"],
           ["(ROOT (S (NP (DT de) (", "nn,5", " ", 5, ")) ", "pvp,6", " (. .)))"]))
]

# Constituent: Sentential adverbs
const_advs_ent_templates = [
    (0.5, ([(0, "zonder twijfel"), (1, pl_verbs), (2, "de"), (3, nouns), (4, "met de"), (5, nouns), (6, ".")], [2, 3, 1, 4, 5, 6], "temp52",
               ["(ROOT (S (PP (Zonder twijfel) (NP (DT a) (NN doubt))) (S (NP (DT de) (", "nn,3", " ", 3, ")) ", "pvp,1",
                ") (. .)))"], ["(ROOT (S (NP (DT de) (", "nn,3", " ", 3, ")) ", "pvp,1", " (. .)))"])),
    (0.5, ([(0, "natuurlijk"), (1, pl_verbs), (2, "de"), (3, nouns), (4, "met de"), (5, nouns), (6, ".")], [2, 3, 1, 4, 5, 6], "temp53",
               ["(ROOT (S (PP (IN Of) (NP (NN course))) (S (NP (DT de) (", "nn,3", " ", 3, ")) ", "pvp,1",
                ") (. .)))"], ["(ROOT (S (NP (DT de) (", "nn,3", " ", 3, ")) ", "pvp,1", " (. .)))"]))
]

if __name__ == "__main__":
    print("Contradiction: Entailed")
    print(template_filler(con_noun_switch_template))
    print(template_filler(con_bijv_template))
    print(template_filler(con_verb_switch))
    print(template_filler(prep_con_template))
    print(template_filler(con_prep_template))
    print("")

    print("Contradiction: Not entailed")
    print(template_filler(con_template))
    print(template_filler(con_template_en))
    print(template_filler(con_template_bijv))
    print("")

    print("Lexical Overlap: Not entailed")
    print(template_filler(lex_simple_templates))
    print(template_filler(lex_prep_templates))
    print(template_filler(lex_rc_templates))
    print(template_filler(lex_conj_templates))
    print("")

    print("Lexical Overlap: Entailed")
    print(template_filler(lex_rc_ent_templates))
    print(template_filler(lex_cross_pp_ent_templates))
    print(template_filler(lex_ent_conj_templates))
    print(template_filler(lex_ent_pass_templates))
    print("")

    print("Subsequence: Not entailed")
    print(template_filler(subseq_pp_on_subj_templates))
    print(template_filler(subseq_rel_on_subj_templates))
    print("")

    print("Subsequence: Entailed")
    print(template_filler(subseq_conj_templates))
    print(template_filler(subseq_adj_templates))
    print(template_filler(subseq_rel_on_obj_templates))
    print(template_filler(subseq_pp_on_obj_templates))
    print("")

    print("Constituent: Not entailed")
    print(template_filler(const_under_if_templates))
    print(template_filler(const_disj_templates))
    print(template_filler(const_adv_outside_templates))
    print("")

    print("Constituent: Entailed")
    print(template_filler(const_quot_ent_templates))
    print(template_filler(const_conj_templates))
    print(template_filler(const_advs_ent_templates))


