import re
import pymysql

db = pymysql.Connect(host="localhost", user="user", passwd="pass", db="db", charset="utf8")
select_rus = 'SELECT id, `header`  FROM page_translation WHERE localize_id=40'
select_tur = 'SELECT id, `header`  FROM page_translation WHERE localize_id=38'
select_eng = 'SELECT id, `header`  FROM page_translation WHERE localize_id=39'
update = "UPDATE news_article_translation SET body='{0}' WHERE id={1}"

cur = db.cursor()

cur.execute(select_rus)
txt_rus = [row for row in cur.fetchall()]

cur.execute(select_tur)
txt_tur = [row for row in cur.fetchall()]

cur.execute(select_eng)
txt_eng = [row for row in cur.fetchall()]

space = u"\w+\s+"
end_of_word = u"\w+"
rus_search_pattern = re.compile(u"regular".format(space, end_of_word), re.UNICODE + re.I)
tur_search_pattern = re.compile(u"regular".format(space, end_of_word), re.UNICODE + re.I)
eng_search_pattern = re.compile(u"regular".format(space, end_of_word), re.UNICODE + re.I)


def Get_Repl_Strings(found_str):
 old_str = found_str
 old = old_str.split()[1:]
 new_str = list(" ".join(old))
 new_str[0] = new_str[0].upper()
 return old_str, "".join(new_str)


def ShowReplaces(search_res):
 for i in set(search_res):
  old_str, new_str = Get_Repl_Strings(i)
  print( old_str + " => " + new_str)


def MakeReplaces(search_res, txt):
 for i in set(search_res):
  old_str, new_str = Get_Repl_Strings(i)
  txt =txt.replace(old_str, new_str)
 return txt


def main(txt_lang, lang_search_pattern):
    for i in txt_lang:
        try:
            lang_search_res = re.findall(lang_search_pattern, i[1])
        except TypeError:
            pass
        if len(lang_search_res) != 0:
            txt = MakeReplaces(lang_search_res, i[1])
            print(i[0])
            cur.execute(update.format(db.escape_string(txt), i[0]))
            db.commit()


def Show(txt_lang, lang_search_pattern):
    for i in txt_lang:
        try:
            lang_search_res = re.findall(lang_search_pattern, i[1])
        except TypeError: pass
        ShowReplaces(lang_search_res)


main(txt_rus, rus_search_pattern)
main(txt_eng, eng_search_pattern)
main(txt_tur, tur_search_pattern)