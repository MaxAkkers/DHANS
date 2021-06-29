from main import *
import random
template_list = [
    ("constituent", "cn_embedded_under_if", "NEUTRAL", const_under_if_templates),
    ("constituent", "cn_disjunction", "NEUTRAL", const_disj_templates),
    ("constituent", "ce_after_since_clause", "NEUTRAL", const_adv_outside_templates),
    ("contradiction", "ce_noun_swap", "NEUTRAL", con_noun_switch_template),
    ("contradiction", "ce_bijv", "NEUTRAL", con_bijv_template),
    ("contradiction", "ce_verb_swap", "NEUTRAL", con_verb_switch),
    ("contradiction", "ce_prep_1", "NEUTRAL", prep_con_template),
    ("contradiction", "ce_prep_1", "NEUTRAL", con_prep_template),
    ("contradiction", "cn_template", "CONTRADICTION", con_template),
    ("contradiction", "cn_template_en", "CONTRADICTION", con_template_en),
    ("contradiction", "cn_bijv", "CONTRADICTION", con_template_bijv),
    ("subsequence", "sn_PP_on_subject", "CONTRADICTION", subseq_pp_on_subj_templates),
    ("subsequence", "sn_relative_clause_on_subject", "CONTRADICTION", subseq_rel_on_subj_templates),
    ("lexical_overlap", "ln_subject/object_swap", "CONTRADICTION", lex_simple_templates),
    ("lexical_overlap", "ln_preposition", "CONTRADICTION", lex_prep_templates),
    ("lexical_overlap", "ln_relative_clause", "CONTRADICTION", lex_rc_templates),
    ("lexical_overlap", "ln_conjunction", "CONTRADICTION", lex_conj_templates),
    ("subsequence", "se_conjunction", "ENTAILMENT", subseq_conj_templates),
    ("subsequence", "se_adjective", "ENTAILMENT", subseq_adj_templates),
    ("subsequence", "se_relative_clause_on_obj", "ENTAILMENT", subseq_rel_on_obj_templates),
    ("subsequence", "se_PP_on_obj", "ENTAILMENT", subseq_pp_on_obj_templates),
    ("constituent", "ce_embedded_under_verb", "ENTAILMENT", const_quot_ent_templates),
    ("constituent", "ce_conjunction", "ENTAILMENT", const_conj_templates),
    ("constituent", "ce_adverb", "ENTAILMENT", const_advs_ent_templates),
    ("lexical_overlap", "le_relative_clause", "ENTAILMENT", lex_rc_ent_templates),
    ("lexical_overlap", "le_around_prepositional_phrase", "ENTAILMENT", lex_cross_pp_ent_templates),
    ("lexical_overlap", "le_conjunction", "ENTAILMENT", lex_ent_conj_templates),
    ("lexical_overlap", "le_passive", "ENTAILMENT", lex_ent_pass_templates)]

def no_the(sentence):
    return sentence.replace("de ", "")

lemma = {}
lemma["professors"] = "professor"
lemma["students"] = "student"
lemma["presidents"] = "president"
lemma["judges"] = "judge"
lemma["senators"] = "senator"
lemma["secretaries"] = "secretary"
lemma["doctors"] = "doctor"
lemma["lawyers"] = "lawyer"
lemma["scientists"] = "scientist"
lemma["bankers"] = "banker"
lemma["tourists"] = "tourist"
lemma["managers"] = "manager"
lemma["artists"] = "artist"
lemma["authors"] = "author"
lemma["actors"] = "actor"
lemma["athletes"] = "athlete"


def repeaters(sentence):
    condensed = no_the(sentence)
    words = []

    for word in condensed.split():
        if word in lemma:
            words.append(lemma[word])
        else:
            words.append(word)

    if len(list(set(words))) == len(words):
        return False
    else:
        return True


fo = open("heuristics_set.txt.txt", "w")

fo.write(
    "sentence1\tsentence2\theuristic\tgold_label\tdata\t\n")

example_counter = 0

for template_tuple in template_list:
    heuristic = template_tuple[0]
    category = template_tuple[1]
    label = template_tuple[2]
    template = template_tuple[3]

    example_dict = {}
    count_examples = 0

    while count_examples < 100:
        example = template_filler(template)
        counter = random.randint(1, 100)
        example_sents = tuple(example[:2])

        if example_sents not in example_dict and not repeaters(example[0]):
            if 0 < counter < 10:
                datatype = "TRAIL"
            elif 11 < counter < 20:
                datatype = "TRAIN"
            else:
                datatype = "TEST"
            example_dict[example_sents] = 1
            pairID = "ex" + str(example_counter)
            fo.write(
                example[0].replace(".", "") + "\t" + example[1].replace(".", "") + "\t" + label + "\t" + heuristic + "\t" + datatype + "\n")
            count_examples += 1
            example_counter += 1