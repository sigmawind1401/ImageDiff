import datetime
import ast
import re
import io
import csv
import mojimoji
from django.utils.timezone import make_aware
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import check_password
from .functions.CloudVisionApi import CloudVisionApi
from .functions.DiffMatch import DiffMatch
from .functions.DiffMatchPatch import DiffMatchPatch
from .functions.SQL import MySQL
# from .functions.CheckMailAddress import check_mail_address
from .models import Config, Alert, Log, Word
from .forms import SearchLogForm, UploadCsvFileForm

MAX_ALERT_NUM = 30000
MAX_WORD_NUM = 1000

# 一致文字列辞書作成
def create_match_dict(resultList, condLength, alertId):
    
    # 警告辞書取得
    objs = MySQL().get_imagediff_alert_word_order(1, alertId)
    # objs = Alert.objects.filter(alert_id = alertId)

    # 変換文字辞書取得
    words = Word.objects.filter(alert_id = alertId)

    matchDict = {}
    matchLogDict = {}
    for result in resultList:
        if result[0] == 0:      # Match
            string = result[1].replace("\n", "")
            # tString1 = string.replace("Z", "2").replace("l", "1").replace("I", "1").replace("O", "0")
            # tString2 = string.replace("2", "Z").replace("1", "l").replace("1", "I").replace("0", "O")
            tString1 = string
            tString2 = string
            for word in words:
                tString1 = tString1.replace(word.word_before, word.word_after)
                tString2 = tString2.replace(word.word_after, word.word_before)

            length = len(string)
            if length >= condLength:

                # 警告ワード検索
                alertCmtList = []
                # alertCmtLogList = []
                matchLen = "0"
                for obj in objs:
                    if obj[0] in result[1]:
                        match = re.search(obj[0], string)
                        tmpList = []
                        tmpLen = str(match.end() - match.start())
                        if matchLen < tmpLen: matchLen = tmpLen
                        if match.start() > 0: tmpList.append([0, string[:match.start()]])
                        tmpList.append([1, string[match.start():match.end()]])
                        if match.end() < length: tmpList.append([0, string[match.end():]])

                        alertCmtList.append([tmpList, obj[1]])
                        # alertCmtLogList.append(obj.alert_comment)

                    else:
                        # alertWord1 = obj[0].replace("Z", "2").replace("l", "1").replace("I", "1").replace("O", "0")
                        # alertWord2 = obj[0].replace("2", "Z").replace("1", "l").replace("1", "I").replace("0", "O")
                        alertWord1 = obj[0]
                        alertWord2 = obj[0]
                        for word in words:
                            alertWord1 = alertWord1.replace(word.word_before, word.word_after)
                            alertWord2 = alertWord2.replace(word.word_after, word.word_before)

                        if obj[0] in tString1:
                            match = re.search(obj[0], tString1)
                            tmpList = []
                            tmpLen = str(match.end() - match.start())
                            if matchLen < tmpLen: matchLen = tmpLen
                            if match.start() > 0: tmpList.append([0, tString1[:match.start()]])
                            tmpList.append([1, tString1[match.start():match.end()]])
                            if match.end() < length: tmpList.append([0, tString1[match.end():]])

                            alertCmtList.append([tmpList, obj[1]])

                        elif obj[0] in tString2:
                            match = re.search(obj[0], tString2)
                            tmpList = []
                            tmpLen = str(match.end() - match.start())
                            if matchLen < tmpLen: matchLen = tmpLen
                            if match.start() > 0: tmpList.append([0, tString2[:match.start()]])
                            tmpList.append([1, tString2[match.start():match.end()]])
                            if match.end() < length: tmpList.append([0, tString2[match.end():]])

                            alertCmtList.append([tmpList, obj[1]])

                        elif alertWord1 in tString1:
                            match = re.search(alertWord1, tString1)
                            tmpList = []
                            tmpLen = str(match.end() - match.start())
                            if matchLen < tmpLen: matchLen = tmpLen
                            if match.start() > 0: tmpList.append([0, tString1[:match.start()]])
                            tmpList.append([1, tString1[match.start():match.end()]])
                            if match.end() < length: tmpList.append([0, tString1[match.end():]])

                            alertCmtList.append([tmpList, obj[1]])

                        elif alertWord2 in tString2:
                            match = re.search(alertWord2, tString2)
                            tmpList = []
                            tmpLen = str(match.end() - match.start())
                            if matchLen < tmpLen: matchLen = tmpLen
                            if match.start() > 0: tmpList.append([0, tString2[:match.start()]])
                            tmpList.append([1, tString2[match.start():match.end()]])
                            if match.end() < length: tmpList.append([0, tString2[match.end():]])

                            alertCmtList.append([tmpList, obj[1]])
                        

                key = str(length)
                key = "1" + matchLen.zfill(3) + key.zfill(3)
                stringList = matchDict.get(key)
                stringLogList = matchLogDict.get(key)

                # if stringList is None:
                #     matchDict.setdefault(key, [[result[1], alertCmt]])

                # else:
                #     stringList.append([result[1], alertCmt])
                #     matchDict.update({key: stringList})

                if stringList is None: stringList = []
                if stringLogList is None: stringLogList = []

                if len(alertCmtList) == 0:
                    tmpList = []
                    tmpList.append([0, string])
                    stringList.append([tmpList, ""])

                else:
                    for alertCmt in alertCmtList:
                        stringList.append(alertCmt)
                
                stringLogList.append(string)

                matchDict.update({key: stringList})
                matchLogDict.update({key: stringLogList})
            
        elif result[0] == -1:   # Delete
            pass

        elif result[0] == 1:    # Insert
            pass

    return matchDict, matchLogDict


# 有効期限チェック
def check_expiration_date(expDate, freLimit, userId):

    dt = datetime.date.today()
    if freLimit is None:
        if dt > expDate:
            return 1, "有効期限が過ぎました。\n引き続きご利用になる場合は有効期限の更新ボタンより有効期限の更新をお願い致します。"
        
        else:
            days = (expDate - dt).days
            if days == 0:
                return 2, "本日が有効期限となります。\n引き続きご利用になる場合は設定画面より有効期限の更新をお願い致します。"
            
            elif days <= 5:
                return 2, "有効期限が迫っております。\n引き続きご利用になる場合は設定画面より有効期限の更新をお願い致します。"

    else:
        if Log.objects.filter(user_id=userId).count() >= freLimit:
            return 1, "利用限度回数を超えました。\n引き続きご利用になる場合は有効期限の更新ボタンより有料プランへの更新をお願い致します。"

        if dt > expDate:
            return 1, "有効期限が過ぎました。\n引き続きご利用になる場合は有効期限の更新ボタンより有効期限の更新をお願い致します。"

        else:
            days = (expDate - dt).days
            if days == 0:
                return 2, "本日が有効期限となります。\n引き続きご利用になる場合は設定画面より有効期限の更新をお願い致します。"

            elif days <= 5:
                return 2, "有効期限が迫っております。\n引き続きご利用になる場合は設定画面より有効期限の更新をお願い致します。"

    return 0, ""


@login_required
def view_top(request):

    page = request.GET.get("page", None)
    if page == "camera":
        return redirect("imagediff:camera")
    
    elif page == "camera_1send":
        return redirect("imagediff:camera_1send")
    
    elif page == "config":
        return redirect("imagediff:config")
    
    elif page == "alert":
        return redirect("imagediff:alert")
    
    elif page == "word":
        return redirect("imagediff:word")
    
    elif page == "log":
        return redirect("imagediff:log")
    
    elif page == "logout":
        return redirect("accounts:logout")

    else:
        return render(request, "imagediff/top.html", {"mail": settings.EMAIL_HOST_USER})


@login_required
def view_camera(request):

    # session初期化
    request.session["texts1"] = ""
    request.session["texts2"] = ""
    request.session["resultList"] = []
    request.session["sendType"] = "camera"
    
    # 個別設定取得
    obj = Config.objects.get(user_id=request.user.id)
    d = {"facingMode": obj.facing_mode}

    return render(request, "imagediff/camera.html", d)


@login_required
def view_camera_1send(request):

    # session初期化
    request.session["texts1"] = ""
    request.session["texts2"] = ""
    request.session["resultList"] = []
    request.session["sendType"] = "camera_1send"
    
    # 個別設定取得
    obj = Config.objects.get(user_id=request.user.id)
    d = {"facingMode": obj.facing_mode}

    return render(request, "imagediff/camera_1send.html", d)


@login_required
def view_result(request):

    d = {"optionList": list(range(1, 21, 1))}
    send_type = request.POST.get("send_type")
    if request.method == "POST":

        # 現在日時取得
        dt_now = datetime.datetime.now()

        if "viewResult" in request.POST:

            # 個別設定取得
            obj = Config.objects.get(user_id=request.user.id)

            # 有効期限チェック
            status, message = check_expiration_date(obj.expiration_date, obj.frequency_limit, request.user.id)
            if status == 1:     # 有効期限切れ
                messages.error(request, message)
                return redirect("imagediff:config")
            elif status == 2:   # 有効期限まじか
                messages.warning(request, message)

            # 1枚目テキスト検出実行
            request.session["imgData1"] = request.POST.get("imgData1", None)
            status, texts = CloudVisionApi().run_text_detection(request.session["imgData1"])
            if status != 0: messages.error(request, texts)
            request.session["texts1"] = texts
            
            # 2枚目テキスト検出実行
            if send_type == "1":
                request.session["imgData2"] = None
            else:
                request.session["imgData2"] = request.POST.get("imgData2", None)
                status, texts = CloudVisionApi().run_text_detection(request.session["imgData2"])
                if status != 0: messages.error(request, texts)
            request.session["texts2"] = texts

            # テキスト比較
            if send_type == "1":
                words = Word.objects.filter(alert_id = obj.alert_id)
                texts1 = request.session["texts1"].replace("\n", "").replace(" ", "").replace("　", "")
                texts2 = request.session["texts2"].replace("\n", "").replace(" ", "").replace("　", "")
                texts3 = texts1
                texts4 = texts2
                for word in words:
                    texts3 = texts3.replace(word.word_before, word.word_after)
                    texts4 = texts4.replace(word.word_after, word.word_before)
                request.session["resultList1"] = request.session["texts1"]
                request.session["resultList2"] = []
                request.session["resultList"] = DiffMatch().match_string(texts1, texts2, texts3, texts4)
            else:
                request.session["resultList1"] = DiffMatchPatch().diff_main(request.session["texts1"], request.session["texts2"])
                request.session["resultList2"] = DiffMatchPatch().diff_main(request.session["texts2"], request.session["texts1"])
                request.session["resultList"] = list(set(request.session["resultList1"] + request.session["resultList2"]))
            
            # 一致文字列辞書作成
            matchLength = obj.match_length
            matchDict, matchLogDict = create_match_dict(request.session["resultList"], matchLength, obj.alert_id)
            matchList = sorted(matchDict.items(), reverse=True)
            matchLogList = sorted(matchLogDict.items(), reverse=True)

            # Log更新
            log = Log(
                key="{}{}".format(dt_now.strftime("%Y%m%d%H%M%S"), str(request.user.id).zfill(6)),
                user_id=request.user.id,
                result=matchLogList,
                image01=request.session["imgData1"],
                image02=request.session["imgData2"]
                )
            log.save()
            
            d.update({
                "matchList"  : matchList,
                "matchLength": matchLength,
                "resultList1" : request.session["resultList1"],
                "resultList2" : request.session["resultList2"],
                "sendType"    : request.session["sendType"],
            })
        
        elif "camera" in request.POST:
            return redirect("imagediff:camera")
        
        elif "camera_1send" in request.POST:
            return redirect("imagediff:camera_1send")
        
        elif "top" in request.POST:
            return redirect("imagediff:top")
        
        elif "updateMatchLength" in request.POST:

            # 個別設定更新
            matchLength = int(request.POST.get("matchLength"))
            obj = Config.objects.get(user_id=request.user.id)
            obj.match_length = matchLength
            obj.save()
            matchDict, matchLogDict = create_match_dict(request.session["resultList"], matchLength, obj.alert_id)
            matchList = sorted(matchDict.items(), reverse=True)
            matchLogList = sorted(matchLogDict.items(), reverse=True)

            # Log更新
            log = Log(
                key="{}{}".format(dt_now.strftime("%Y%m%d%H%M%S"), str(request.user.id).zfill(6)),
                user_id=request.user.id,
                result=matchLogList,
                image01=request.session["imgData1"],
                image02=request.session["imgData2"]
                )
            log.save()

            # 有効期限チェック
            status, message = check_expiration_date(obj.expiration_date, obj.frequency_limit, request.user.id)
            if status == 1:     # 有効期限切れ
                messages.error(request, message)
                return redirect("imagediff:config")
            elif status == 2:   # 有効期限まじか
                messages.warning(request, message)
            
            d.update({
                "matchList"  : matchList,
                "matchLength": matchLength,
                "resultList1" : request.session["resultList1"],
                "resultList2" : request.session["resultList2"],
                "sendType"    : request.session["sendType"],
            })
        
    return render(request, "imagediff/result.html", d)
    

@login_required
def view_config(request):

    d = {}
    if request.method == "POST":

        if "updateEmail" in request.POST:
            email = request.POST.get("email")
            obj = Config.objects.get(user_id=request.user.id)
            user = User.objects.get(id=request.user.id)
            if obj.email == email:
                messages.info(request, "更新前と同じメールアドレスのため、更新をスキップしました。")
            elif len(email) == 0:
                messages.warning(request, "メールアドレスは必ず設定してください。")
            else:
                obj.email = email
                obj.save()
                user.email = email
                user.save()
                messages.info(request, "メールアドレスの更新が完了しました。")

        elif "updateMatchLength" in request.POST:
            matchLength = int(request.POST.getlist("matchLength")[0])
            obj = Config.objects.get(user_id=request.user.id)
            if obj.match_length == matchLength:
                messages.info(request, "更新前と同じ一致文字数のため、更新をスキップしました。")
            else:
                obj.match_length = matchLength
                obj.save()
                messages.info(request, "一致文字数の更新が完了しました。")

        elif "updateFacingMode" in request.POST:
            facingMode = int(request.POST.getlist("facingMode")[0])
            obj = Config.objects.get(user_id=request.user.id)
            if obj.facing_mode == facingMode:
                messages.info(request, "更新前と同じカメラモードのため、更新をスキップしました。")
            else:
                obj.facing_mode = facingMode
                obj.save()
                messages.info(request, "カメラモードの更新が完了しました。")

        elif "updateExpirationDate" in request.POST:
            return redirect("accounts:signup_step3_update")

        elif "chgPassword" in request.POST:
            old_password = request.POST.get("password")
            new_password1 = request.POST.get("newPassword1")
            new_password2 = request.POST.get("newPassword2")

            if new_password1 != new_password2:  # 新しいパスワード入力チェック
                messages.error(request, "確認用パスワードと一致しなかったため、変更をキャンセルしました。")
            
            else:
                user = User.objects.get(id=request.user.id)

                if check_password(old_password, user.password) == False:    # 古いパスワード入力チェック
                    messages.error(request, "古いパスワードが違ったため、変更をキャンセルしました。")
                
                else:
                    user.set_password(new_password1)
                    user.save()
                    messages.info(request, "パスワードの変更が完了しました。")
                    return redirect("accounts:login")

        elif "back" in request.POST:
            return redirect("imagediff:top")

    else:
        pass

    data = MySQL().get_imagediff_config(2, request.user.id)

    d.update({
        "data"      : data,
        "optionList": list(range(1, 21, 1)),
        "count"     : Log.objects.filter(user_id=request.user.id).count()
        })

    return render(request, "imagediff/config.html", d)


@login_required
def view_alert(request):

    d = {}
    if request.method == "POST":

        if "chgAlertDB" in request.POST:
            try:
                user = User.objects.get(username=request.POST.get("username"))
                if check_password(request.POST.get("password"), user.password):
                    obj = Config.objects.get(user_id=request.user.id)
                    setattr(obj, "alert_id", user.id)
                    obj.save()
                    messages.info(request, "警告ＤＢの参照先が変更されました。")
                else:
                    messages.error(request, "パスワードが異なるため、処理をキャンセルしました。")
            except User.DoesNotExist:
                messages.error(request, "存在しないユーザー名のため、処理をキャンセルしました。")

        elif "addAlertDB" in request.POST:
            data = MySQL().get_imagediff_config(2, request.user.id)
            alert_id = data[0].get("alert_id")
            count = Alert.objects.filter(alert_id=alert_id).count()
            alert_word = request.POST.get("alertWord1")
            alert_comment = request.POST.get("alertComment1")
            if len(alert_word) == 0:
                messages.error(request, "警告ワードが空白だったため、追加できませんでした。")

            elif len(alert_comment) == 0:
                messages.error(request, "警告コメントが空白だったため、追加できませんでした。")

            elif count >= MAX_ALERT_NUM:
                messages.error(request, "登録上限を超えるため、追加できませんでした。")

            else:
                obj, created = Alert.objects.get_or_create(
                    alert_id=alert_id,
                    alert_word=alert_word,
                    defaults={
                        "key"          : "{}_{}".format(alert_id, alert_word),
                        "alert_comment": alert_comment,
                        "create_user"  : data[0].get("user_name"),
                        "update_user"  : data[0].get("user_name"),
                    },
                )
                if created == True:
                    messages.info(request, "警告ワードの追加が完了しました。")

                else:
                    messages.error(request, "既に同じ警告ワードが登録済みのため、追加できませんでした。")

        elif "editAlertDB" in request.POST:
            pass

        elif "delAlertDB" in request.POST:
            key = request.POST.get("key3")
            if len(key) != 0:
                Alert.objects.filter(key=key).delete()
                messages.info(request, "警告ワードの削除が完了しました。")

            else:
                messages.error(request, "キー情報が取得できなかったため、処理をキャンセルしました。")

        elif "delAlertDBAll" in request.POST:
            config = Config.objects.get(user_id=request.user.id)
            Alert.objects.filter(alert_id=config.alert_id).delete()
            messages.info(request, "警告ワードの全件削除が完了しました。")

        elif "readCsv" in request.POST:
            return redirect("imagediff:csv")

        elif "back" in request.POST:
            return redirect("imagediff:top")

    data = MySQL().get_imagediff_config(2, request.user.id)
    obj = Alert.objects.filter(alert_id=data[0].get("alert_id")).order_by("alert_id")
    d.update({
        "data"     : data,
        "alertList": obj,
        "count"    : Alert.objects.filter(alert_id=data[0].get("alert_id")).count(),
    })

    return render(request, "imagediff/alert.html", d)


@login_required
def view_csv(request):

    d = {}
    if request.method == "POST":
        form = UploadCsvFileForm(request.POST, request.FILES)
        if "readCsv" in request.POST:
            if len(request.FILES) == 0:
                messages.error(request, "ファイル情報が取得できませんでした。")
                
            else:
                csvfile = io.TextIOWrapper(form.files["csvfile"], newline="", encoding="utf-8")
                if csvfile.name.endswith(".csv") == False:
                    messages.error(request, "ファイルの拡張子がcsvでないため取り込めませんでした。")

                else:
                    reader = csv.reader(csvfile)
                    rows = []
                    for row in reader:
                        rows.append(row)
                    request.session["rows"] = rows
                    options = []
                    for i in range(0, len(rows[0])):
                        options.append(["{}".format(i), "{}列目".format(i + 1)])

                    d.update({
                        "rows": rows[:10],
                        "options": options,
                        })

        elif "addAlertDB" in request.POST:
            rows = request.session["rows"] if request.POST.get("addAlertDBIndexDel") is None else request.session["rows"][1:]
            word_col = int(request.POST.get("wordSelectCol"))
            cmt_col = int(request.POST.get("cmtSelectCol"))
            config = Config.objects.get(user_id=request.user.id)
            alert_word_dict = MySQL().get_imagediff_alert_word(3, config.alert_id)
            count = Alert.objects.filter(alert_id=config.alert_id).count()
            add_dict = {}
            update_dict = {}
            word_length_over_count = 0
            cmt_length_over_count = 0
            overlap_count = 0
            cmt_update_count = 0

            # 重複除外
            for row in rows:
                word = row[word_col]
                cmt = row[cmt_col]
                if request.POST.get("wordSpaceDelHalf") is not None: word = word.replace(" ", "")       # 空白除去（半角）
                if request.POST.get("wordSpaceDelFull") is not None: word = word.replace("　", "")      # 空白除去（全角）
                if request.POST.get("wordSpaceFullToHalf") is not None: word = word.replace("　", " ")  # 全角→半角（空白）
                if request.POST.get("wordFullToHalf") is not None: word = mojimoji.zen_to_han(word, kana=False, digit=True, ascii=True)     # 全角→半角（英数字記号）
                if request.POST.get("wordHalfToFull") is not None: word = mojimoji.han_to_zen(word, kana=True, digit=False, ascii=False)    # 全角→半角（半角→全角（カタカナ））
                if request.POST.get("cmtSpaceDelHalf") is not None: cmt = cmt.replace(" ", "")          # 空白除去（半角）
                if request.POST.get("cmtSpaceDelFull") is not None: cmt = cmt.replace("　", "")         # 空白除去（全角）
                if request.POST.get("cmtSpaceFullToHalf") is not None: cmt = cmt.replace("　", " ")     # 全角→半角（空白）
                if request.POST.get("cmtFullToHalf") is not None: cmt = mojimoji.zen_to_han(cmt, kana=False, digit=True, ascii=True)        # 全角→半角（英数字記号）
                if request.POST.get("cmtHalfToFull") is not None: cmt = mojimoji.han_to_zen(cmt, kana=True, digit=False, ascii=False)       # 全角→半角（半角→全角（カタカナ））
                if len(word) <= 50:
                    if len(cmt) <= 254:
                        if alert_word_dict.get(word) is None:     # 現状のDBにキーがないかチェック
                            if add_dict.get(word) is None:        # 追加予定Dictにキーがないかチェック
                                add_dict.update({word: cmt})
                            else:
                                overlap_count += 1
                        else:
                            if alert_word_dict.get(word) != cmt:    # コメントの更新チェック
                                if update_dict.get(word) is None:      # 更新予定Dictにキーがないかチェック
                                    update_dict.update({word: cmt})
                                    cmt_update_count += 1
                    else:
                        cmt_length_over_count += 1
                else:
                    word_length_over_count += 1
            
            add_dict_count = len(add_dict)
            if add_dict_count == 0 and cmt_update_count == 0:
                messages.error(request, "新規に追加または更新できる項目がないため、処理をキャンセルしました。")
            
            elif add_dict_count + count >= MAX_ALERT_NUM:
                messages.error(request, "登録上限を超えるため、追加できませんでした。")
            
            else:
                if cmt_update_count != 0:  # 更新処理
                    for key, val in update_dict.items():
                        Alert.objects.filter(key="{}_{}".format(config.alert_id, key)).update(
                            alert_comment=val,
                            create_user=request.user.username,
                            update_user=request.user.username
                        )
                if add_dict_count != 0:  # 追加処理
                    add_alerts = []
                    for key, val in add_dict.items():
                        alert = Alert(
                            key="{}_{}".format(config.alert_id, key),
                            alert_id=config.alert_id,
                            alert_word=key,
                            alert_comment=val,
                            create_user=request.user.username,
                            update_user=request.user.username
                            )
                        add_alerts.append(alert)
                    Alert.objects.bulk_create(add_alerts)
                messages.info(request, "CSVファイルの取込が完了しました。")
                if word_length_over_count > 0: messages.warning(request, "{}件の検索ワード指定文字数超過を確認しました".format(word_length_over_count))
                if cmt_length_over_count > 0: messages.warning(request, "{}件のコメント指定文字数超過を確認しました".format(cmt_length_over_count))
                if overlap_count > 0: messages.warning(request, "{}件の重複を確認しました".format(overlap_count))
                if cmt_update_count > 0: messages.info(request, "{}件のコメントを更新しました".format(cmt_update_count))
            
            return redirect("imagediff:alert")

        elif "back" in request.POST:
            return redirect("imagediff:alert")

    else:
        form = UploadCsvFileForm()

    d.update({"form": form})

    return render(request, "imagediff/csv.html", d)


@login_required
def view_log(request):

    d = {}
    form = SearchLogForm()
    if request.method == "POST":

        if "searchLog" in request.POST:
            if len(request.POST.get("startDate")) == 0 or len(request.POST.get("endDate")) == 0:
                messages.error(request, "検索日は必ず指定してください。")
            else:
                startDate = make_aware(datetime.datetime.strptime(request.POST.get("startDate"), '%Y-%m-%d'))
                endDate = make_aware(datetime.datetime.strptime(request.POST.get("endDate"), '%Y-%m-%d') + datetime.timedelta(days=1))
                objs = Log.objects.filter(user_id=request.user.id, log_date__range=(startDate, endDate)).order_by("log_date")
                logList = []
                for obj in objs:
                    tmpList = []
                    resultList = ast.literal_eval(obj.result)
                    if len(resultList) == 0:
                        tmpList.append("該当なし")
                    else:
                        for result in resultList:
                            for r in result[1]:
                                tmpList.append(r)
                    logList.append([obj.log_date, tmpList, obj.image01, obj.image02])
                d.update({"logList": logList})

        elif "back" in request.POST:
            return redirect("imagediff:top")

    d.update({"form": form})


    return render(request, "imagediff/log.html", d)


@login_required
def view_word(request):

    d = {}
    if request.method == "POST":

        if "chgAlertDB" in request.POST:
            try:
                user = User.objects.get(username=request.POST.get("username"))
                if check_password(request.POST.get("password"), user.password):
                    obj = Config.objects.get(user_id=request.user.id)
                    setattr(obj, "alert_id", user.id)
                    obj.save()
                    messages.info(request, "警告ＤＢの参照先が変更されました。")
                else:
                    messages.error(request, "パスワードが異なるため、処理をキャンセルしました。")
            except User.DoesNotExist:
                messages.error(request, "存在しないユーザー名のため、処理をキャンセルしました。")

        elif "addWordDB" in request.POST:
            data = MySQL().get_imagediff_config(2, request.user.id)
            alert_id = data[0].get("alert_id")
            count = Word.objects.filter(alert_id=alert_id).count()
            word_before = request.POST.get("wordBefore1")
            word_after = request.POST.get("wordAfter1")
            if len(word_before) == 0:
                messages.error(request, "変換前が空白だったため、追加できませんでした。")

            elif len(word_after) == 0:
                messages.error(request, "変換後が空白だったため、追加できませんでした。")

            elif count >= MAX_WORD_NUM:
                messages.error(request, "登録上限を超えるため、追加できませんでした。")

            else:
                obj, created = Word.objects.get_or_create(
                    alert_id=alert_id,
                    word_before=word_before,
                    defaults={
                        "key"        : "{}_{}_{}".format(alert_id, word_before, word_after),
                        "word_after" : word_after,
                        "create_user": data[0].get("user_name"),
                        "update_user": data[0].get("user_name"),
                    },
                )
                if created == True:
                    messages.info(request, "変換文字の追加が完了しました。")

                else:
                    messages.error(request, "既に同じ変換文字が登録済みのため、追加できませんでした。")

        elif "editWordDB" in request.POST:
            pass

        elif "delWordDB" in request.POST:
            key = request.POST.get("key3")
            if len(key) != 0:
                Word.objects.filter(key=key).delete()
                messages.info(request, "変換文字の削除が完了しました。")

            else:
                messages.error(request, "キー情報が取得できなかったため、処理をキャンセルしました。")

        elif "delWordDBAll" in request.POST:
            config = Config.objects.get(user_id=request.user.id)
            Word.objects.filter(alert_id=config.alert_id).delete()
            messages.info(request, "変換文字の全件削除が完了しました。")

        elif "readCsv" in request.POST:
            return redirect("imagediff:csv")

        elif "back" in request.POST:
            return redirect("imagediff:top")

    data = MySQL().get_imagediff_config(2, request.user.id)
    obj = Word.objects.filter(alert_id=data[0].get("alert_id")).order_by("alert_id")
    d.update({
        "data"    : data,
        "wordList": obj,
        "count"   : Word.objects.filter(alert_id=data[0].get("alert_id")).count(),
    })

    return render(request, "imagediff/word.html", d)