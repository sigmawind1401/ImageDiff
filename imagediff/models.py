from django.db import models
# from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth import get_user_model
from django.utils import timezone

class Config(models.Model):

    user            = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True)
    alert_id        = models.IntegerField(verbose_name="参照ＩＤ")
    email           = models.CharField(max_length=254, verbose_name="メールアドレス")
    match_length    = models.IntegerField(default=3, verbose_name="一致文字数")
    facing_mode     = models.BooleanField(default=1, verbose_name="カメラモード")
    expiration_date = models.DateField(verbose_name="有効期限")
    frequency_limit = models.IntegerField(null=True, blank=True, verbose_name="限度回数")

class Alert(models.Model):

    key           = models.CharField(max_length=80, primary_key=True, verbose_name="キー")
    alert_id      = models.IntegerField(verbose_name="参照ＩＤ")
    alert_word    = models.CharField(max_length=50, verbose_name="警告ワード")
    alert_comment = models.CharField(max_length=254, verbose_name="警告コメント")
    create_user   = models.CharField(max_length=150, verbose_name="作成者")
    created_at    = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    update_user   = models.CharField(max_length=150, verbose_name="更新者")
    updated_at    = models.DateTimeField(auto_now=True, verbose_name="更新日時")

class Log(models.Model):

    key             = models.CharField(max_length=20, primary_key=True, verbose_name="キー")
    log_date        = models.DateTimeField(auto_now_add=True, verbose_name="実行日時")
    user_id         = models.IntegerField(verbose_name="ユーザーＩＤ")
    result          = models.TextField(verbose_name="比較結果")
    image01         = models.TextField(null=True, blank=True, verbose_name="画像01")
    image02         = models.TextField(null=True, blank=True, verbose_name="画像02")

class Word(models.Model):

    key         = models.CharField(max_length=80, primary_key=True, verbose_name="キー")
    alert_id    = models.IntegerField(verbose_name="参照ＩＤ")
    word_before = models.CharField(max_length=1, verbose_name="変換前")
    word_after  = models.CharField(max_length=1, verbose_name="変換後")
    create_user = models.CharField(max_length=150, verbose_name="作成者")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    update_user = models.CharField(max_length=150, verbose_name="更新者")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="更新日時")

# class SearchLog(models.Model):

#     start_date = models.DateField(null=True, blank=True, verbose_name="開始日")
#     end_date   = models.DateField(null=True, blank=True, verbose_name="終了日")

