import sqlite3

path_db = '../client.sqlite'
txtfilepath = '100gb.txt'

with sqlite3.connect(path_db) as con:
    cur = con.cursor()

    while True:
        print('\nНомер задания 2, 6 или 8?')
        print("Введите соответствующую цифру.")
        tasknum = int(input())


        if tasknum == 8:
            print("Введите соответствующую цифру.")
            print("1)Добавить 3 станка: “Сварочный аппарат №1”, “Пильный аппарат №2”, “Фрезер №3”, сделать их активными.")
            print("2)Скопировать со станков: “Фрезерный станок”, “Старый, ЧПУ”, “Сварка”, причины простоя и перенести их на новые станки.")
            print("3)Определить группу “Цех №2” для новых станков.")
            print("4)Добавить станки “Пильный станок” и “Старый ЧПУ” к новой группе.")
            print("5 для просмотра таблицы")
            print("6 для Commit")

            num = int(input())

            if num == 1:
                cur.execute("""
                INSERT INTO endpoints(name, active) VALUES
                ('Сварочный аппарат №1', "true"), 
                ('Пильный аппарат №2', "true"),
                ('Фрезер №3', "true");
                """)

            elif num == 2:
                couples = [('Сварочный аппарат №1','Фрезерный станок'),('Пильный аппарат №2','Старый ЧПУ'),('Фрезер №3','Сварка')]
                for couple in couples:
                    new_one = couple[0]
                    old_one = couple[1]
                    cur.execute(f"""
                    INSERT INTO endpoint_reasons(endpoint_id, reason_name, reason_hierarchy)
                     SELECT (SELECT id FROM endpoints WHERE name = '{new_one}'),
                      reason_name, reason_hierarchy FROM endpoint_reasons
                       WHERE endpoint_id IN(SELECT id FROM endpoints WHERE name = '{old_one}');
                        """)
                    cur.execute('COMMIT')

            elif num == 3:
                cur.execute("""
                INSERT INTO endpoint_groups (endpoint_id, name)
                SELECT id, 'Цех №2' FROM endpoints WHERE name in ('Сварочный аппарат №1','Пильный аппарат №2','Фрезер №3')
                """)

            elif num == 4:
                cur.execute("""
                UPDATE endpoint_groups SET name = 'Цех №2' WHERE endpoint_id IN 
                (SELECT id FROM endpoints WHERE name IN ('Пильный станок','Старый ЧПУ'));
                """)

            elif num == 5:
                print('Введите название таблицы.')
                print('endpoints, endpoint_groups, endpoint_reasons')
                table = input()
                cur.execute(f'SELECT * FROM {table}')
                print(cur.fetchall())

            elif num == 6:
                con.commit()


            else:
                break




        elif tasknum == 2:
            print("Введите соответствующую цифру.")
            print("1) Написать запрос, который выводит причины простоя только активных станков.")
            print("2) Написать запрос, который выводит количество причин простоев для каждой неактивной точки")
            print("3) Написать запрос, который выведет для каждого активного оборудования, "
                  "количество причины простоя  'Перебои напряжения' "
                  "(нужно учесть что это надо сделать для каждой группы(reason_hierarchy))")
            print("4 для просмотра таблицы")
            print("5 для Commit")

            num = int(input())

            if num == 1:
                cur.execute(""" 
                SELECT reason_name FROM endpoint_reasons WHERE endpoint_id IN
                (SELECT id FROM endpoints WHERE active = "true")
                """)
                print(cur.fetchall())

            elif num == 2:
                cur.execute("""
                SELECT COUNT(reason_name) FROM endpoint_reasons WHERE endpoint_id IN
                (SELECT id FROM endpoints WHERE active = "false")
                """)
                print(cur.fetchall())

            elif num == 3:
                cur.execute(""" 
                SELECT endpoint_id, COUNT(reason_name), reason_hierarchy  FROM endpoint_reasons WHERE endpoint_id
                IN(SELECT id FROM endpoints WHERE active = "true") AND reason_name = "Перебои напряжения" 
                GROUP BY endpoint_id
                """)
                print(cur.fetchall())

            elif num == 4:
                print('Введите название таблицы.')
                print('endpoints, endpoint_groups, endpoint_reasons')
                table = input()
                cur.execute(f'SELECT * FROM {table}')
                print(cur.fetchall())

            elif num == 5:
                con.commit()




        elif tasknum == 6:
            print('Есть огромный текстовый файл (более 100 ГБ - он точно не поместится в оперативной памяти),'
                  ' состоящий из строк, как его оптимально обрабатывать?')
            print('Я думаю что это можно делать построчно.\n')
            with open(txtfilepath, 'r', encoding='utf-8') as big_file:
                for line in big_file:
                    print(line, end='')

        else:
            break










