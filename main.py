from flask import Flask, request
import pymysql
import load
import hanlp
import logic

app = Flask(__name__)
blacklist, whitelist = load.load_from_db()
website_list = []
HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)  # 分词
sts = hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH)  # 语义近似度
regular_regrex = ('\\<>——-·`。，、＇：；‘’“”〝〞ˆˇ﹕︰﹔﹖﹑•¨….¸;！´？！～—ˉ｜‖＂〃｀﹫¡¿﹏﹋﹌︴々﹟﹩﹠﹪﹡﹢﹦﹤‐￣¯―﹨ˆ˜﹍﹎<＿_'
                  '-ˇ~﹉﹊（）〈〉‹›﹛﹜『』〖〗［］《》〔〕{}「」【】︵︷︿︹︽_﹁﹃︻︶︸﹀︺︾ˉ﹂﹄︼❝❞')
http_regrex = '*#+=-_∶?/[]()&$%\'@.'


@app.route('/censor', methods=['POST'])
def handle():
    value: str = request.get_json()['comment']
    value = logic.remove(value, regular_regrex)
    containsWebsite = logic.censor_websites(value, website_list)
    if type(containsWebsite) is dict:
        return {'error': '信息包含违禁网站！'}
    else:
        value = logic.remove(value, http_regrex)
        # return logic.need_censor_ram_new(value, blacklist, whitelist, HanLP, sts)
        result = logic.find_censor_dict(value, blacklist, whitelist, HanLP, sts, 'tok/coarse')
        result['containsCensoredWebsite'] = containsWebsite
        return result


@app.route('/addBlacklist', methods=['POST'])
def add_blacklist():
    words = request.get_json()['blacklist']
    try:
        blacklist.extend(words)
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='censors')
        cursor = connection.cursor()
        sql = 'INSERT INTO blacklist VALUES (null, %s)'
        for word in words:
            cursor.execute(sql, word)
        connection.commit()
        cursor.close()
        connection.close()
        return 'success'
    except Exception as e:
        return '添加至黑名单失败！错误原因：' + str(e)


@app.route('/addWhitelist', methods=['POST'])
def add_white():
    words = request.get_json()['whitelist']
    try:
        whitelist.extend(words)
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='censors')
        cursor = connection.cursor()
        sql = 'INSERT INTO whitelist VALUES (null, %s)'
        for word in words:
            cursor.execute(sql, word)
        connection.commit()
        cursor.close()
        connection.close()
        return 'success'
    except Exception as e:
        return '添加至白名单失败！错误原因：' + str(e)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True)
    # app.run(host='0.0.0.0', debug=True)
