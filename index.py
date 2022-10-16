import pprint
import requests
import os
import datetime

proxies={'http':''}
user_list=requests.get('https://json.medrocket.ru/users',
                        proxies=proxies).json()
todos_list=requests.get('https://json.medrocket.ru/todos',
                         proxies=proxies).json()

#  Запись данных пользователей и их дел в оперативную память.\/

files_userId=[] #  Список словарей информации о пользователях
for i in range(len(user_list)):
     new_user = dict(username='', userId= '',company='', name='', email= '', count_todo_t= 0, count_todo_f= 0, true= [], false= [])     
     files_userId.append(new_user)
     files_userId[i]['username']=user_list[i]['username']
     files_userId[i]['userId']=user_list[i]['id']
     files_userId[i]['company']=user_list[i]['company']['name']
     files_userId[i]['name']=user_list[i]['name']
     files_userId[i]['email']=user_list[i]['email']

count = 0  #  Счётчик записанных в память todos
noncount = 0  #  Счётчик незаписанных
for i in range(len(todos_list)):
     if(todos_list[i].get('title',None) != None):
          if todos_list[i]['completed'] == True:
               files_userId[todos_list[i]['userId']-1]['true'].append(todos_list[i]['title'])
               count += 1
               files_userId[todos_list[i]['userId']-1]['count_todo_t'] += 1
          elif todos_list[i]['completed'] == False:
               files_userId[todos_list[i]['userId'] - 1]['false'].append(todos_list[i]['title'])
               count += 1
               files_userId[todos_list[i]['userId'] - 1]['count_todo_f'] += 1
     else:
          noncount += 1
check_todos = ""
if i + 1 - noncount == count:
     check_todos = 'ok' #  ok-todos записанны без потерь
else:
     check_todos = 'not ok' #  ok-todos записанны с потерями
print(check_todos)  



#  Проверка на существование директории tasks и старых отчётов.
#  Переименование старых файлов под нужный формат.\/

if not os.path.isdir("tasks"):  #  
     os.mkdir("tasks")
else:          
     for i in range(len(files_userId)):
          if os.path.isfile('tasks\\' + files_userId[i]['username'] + '.txt'):
               old_f = open('tasks\\' + files_userId[i]['username'] + '.txt')
               t_time = old_f.readlines()[1]
               old_f.close()
               t_time = ''.join(t_time)
               str_time = t_time.find('>')
               t_time=t_time[str_time+8:str_time+12]+'-'+t_time[str_time+5:str_time+7]+'-'+t_time[str_time+2:str_time+4]+'T'+t_time[str_time+13:str_time+15]+'-'+t_time[str_time+16:str_time+18]
               os.rename('tasks\\'+files_userId[i]['username']+'.txt', 'tasks\\Old_'+files_userId[i]['username']+'_'+t_time+'.txt')
               #  Время для старых файлов переименовывается не в заданном вами
               #  формате, так как использование ':', запрещено Соглашением об
               #  именах, поэтому я его заменил на '-':
               #  https://learn.microsoft.com/ru-ru/windows/win32/fileio/naming-a-file

#  Запись в файлы из оперативной памяти

preview_text = '# Отчёт для  .\n  < >  \nВсего задач:  \n\n## Актуальные задачи ( ):\n \n## Завершённые задачи ( ):\n '
preview_text = list(preview_text)     
dt_obj = datetime.datetime.now()  #  Время сейчас, для записи в файлы
dt_string = dt_obj.strftime("%d.%m.%Y %H:%M")
for i in range(len(files_userId)):
     tt_list = []  #  Списки завершённых todos
     tf_list = []  #     (не) 
     for j in range(len(files_userId[i]['true'])):
          if len(files_userId[i]['true'][j]) >= 46:
               tt_list.append('- ' + files_userId[i]['true'][j][:46] + '…\n')
          else:
               tt_list.append('- ' + files_userId[i]['true'][j] + '\n')
     for j in range(len(files_userId[i]['false'])):
          if len(files_userId[i]['false'][j]) >= 46:
               tf_list.append('- ' + files_userId[i]['false'][j][:46] + '…\n')
          else:
               tf_list.append('- ' + files_userId[i]['false'][j] + '\n')

     preview_text[12] = files_userId[i]['company']
     preview_text[15] = files_userId[i]['name']
     preview_text[18] = files_userId[i]['email']
     preview_text[21] = dt_string
     preview_text[36] = str(files_userId[i]['count_todo_f']+files_userId[i]['count_todo_t'])
     preview_text[61] = str(files_userId[i]['count_todo_f'])
     preview_text[65] = ''.join(tf_list)
     preview_text[90] = str(files_userId[i]['count_todo_t'])
     preview_text[94] = ''.join(tt_list)

     filename = "tasks\\" + files_userId[i]['username'] + '.txt'
     f = open(filename,'w')
     try:
          f.write(''.join(preview_text))   
     except:
          print('Неожиданная ошибка')
     finally:
          f.close()