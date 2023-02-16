import bootstrap_datepicker_plus as datetimepicker
from django import forms

class SearchLogForm(forms.Form):

    startDate = forms.CharField(
        label="開始日",
        required=True,
        disabled=False,
        widget=datetimepicker.DatePickerInput(
            format="%Y-%m-%d",
            attrs={"readonly": "true", "id": "startDate"},
            options={
                "locale": "ja",
                "dayViewHeaderFormat": "YYYY年 MMMM",
                "ignoreReadonly": True,
                "allowInputToggle": True
            }
        )
    )
    
    endDate = forms.CharField(
        label="終了日",
        required=True,
        disabled=False,
        widget=datetimepicker.DatePickerInput(
            format="%Y-%m-%d",
            attrs={"readonly": "true", "id": "endDate"},
            options={
                "locale": "ja",
                "dayViewHeaderFormat": "YYYY年 MMMM",
                "ignoreReadonly": True,
                "allowInputToggle": True
            }
        )
    )


class UploadCsvFileForm(forms.Form):

    csvfile = forms.FileField(
        label="Step1. CSVファイルアップロード",
        required=False,
        disabled=False,
        widget=forms.FileInput(
            attrs={
                 "class": "form-control",
                 "accept": ".csv",
            },
        )
    )
    
    wordSpaceDelHalf = forms.BooleanField(
        label="空白除去（半角）",
        required=False,
        disabled=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )
    
    wordSpaceDelFull = forms.BooleanField(
        label="空白除去（全角）",
        required=False,
        disabled=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )
    
    wordSpaceFullToHalf = forms.BooleanField(
        label="全角→半角（空白）",
        required=False,
        disabled=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )
    
    wordFullToHalf = forms.BooleanField(
        label="全角→半角（英数字記号）",
        required=False,
        disabled=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )
    
    wordHalfToFull = forms.BooleanField(
        label="半角→全角（カタカナ）",
        required=False,
        disabled=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )
    
    # wordSelectCol = forms.ChoiceField(
    #     label="列指定",
    #     required=False,
    #     disabled=False,
    #     widget=forms.Select(
    #         attrs={
    #             "class": "custom-select",
    #         }
    #     ),
    # )
    
    cmtSpaceDelHalf = forms.BooleanField(
        label="空白除去（半角）",
        required=False,
        disabled=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )
    
    cmtSpaceDelFull = forms.BooleanField(
        label="空白除去（全角）",
        required=False,
        disabled=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )
    
    cmtSpaceFullToHalf = forms.BooleanField(
        label="全角→半角（空白）",
        required=False,
        disabled=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )
    
    cmtFullToHalf = forms.BooleanField(
        label="全角→半角（英数字記号）",
        required=False,
        disabled=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )
    
    cmtHalfToFull = forms.BooleanField(
        label="半角→全角（カタカナ）",
        required=False,
        disabled=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )
    
    # cmtSelectCol = forms.ChoiceField(
    #     label="列指定",
    #     required=False,
    #     disabled=False,
    #     widget=forms.Select(
    #         attrs={
    #             "class": "custom-select",
    #         }
    #     ),
    # )
    
    addAlertDBIndexDel = forms.BooleanField(
        label="見出し行除外",
        required=False,
        disabled=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "custom-control-input",
            }
        ),
    )