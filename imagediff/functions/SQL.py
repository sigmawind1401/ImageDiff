from django.db import connection


class MySQL:

    # type [0: tuple, 1: list, 2: dict, 3: dict(key=top)]
    def exe_sql(self, sql, type):

        with connection.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
        
        data = None
        if type == 0:
            data = rows

        elif type == 1:
            data = []
            for row in rows:
                data.append(list(row))
        
        elif type == 2:
            columns = [col[0] for col in cur.description]
            data = [
                dict(zip(columns, row))
                for row in rows
                ]
        
        elif type == 3:
            data = {}
            for row in rows:
                if data.get(row[0]) is None:
                    data.update({row[0]: row[1]})
        
        return data

    # # type [0: tuple, 1: list, 2: dict]
    # def exe_sql(self, sql, type):

    #     cur = connection.cursor()
    #     cur.execute(sql)
    #     rows = cur.fetchall()
        
    #     data = None
    #     if type == 0:
    #         data = rows

    #     elif type == 1:
    #         data = []
    #         for row in rows:
    #             data.append(list(row))
        
    #     elif type == 2:
    #         columns = [col[0] for col in cur.description]
    #         data = [
    #             dict(zip(columns, row))
    #             for row in rows
    #             ]
        
    #     return data


    def get_imagediff_config(self, type, key):
        
        sql = ""
        sql += "select "
        sql += " user_id "
        sql += ",(select username from auth_user where id = {}) as user_name ".format(key)
        sql += ",alert_id "
        sql += ",(select username from auth_user where id = imagediff_config.alert_id) as alert_user_name "
        sql += ",email "
        sql += ",match_length "
        sql += ",facing_mode "
        sql += ",expiration_date "
        sql += ",frequency_limit "
        sql += "from "
        sql += " imagediff_config "
        sql += "where user_id = {} ".format(key)

        return self.exe_sql(sql, type)


    def get_imagediff_alert_word(self, type, key):
        
        sql = ""
        sql += "select "
        sql += " alert_word "
        sql += ",alert_comment "
        sql += "from "
        sql += " imagediff_alert "
        sql += "where alert_id = {} ".format(key)

        return self.exe_sql(sql, type)


    def get_imagediff_alert_word_order(self, type, key):
        
        sql = ""
        sql += "select "
        sql += " alert_word "
        sql += ",alert_comment "
        sql += "from "
        sql += " imagediff_alert "
        sql += "where alert_id = {} ".format(key)
        sql += "order by "
        sql += " char_length(alert_word) desc "

        return self.exe_sql(sql, type)