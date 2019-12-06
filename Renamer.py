# -*- coding: utf-8 -*-
"""
Jacobs Autonamer
"""
import os
import shutil
from AutoNamerFuncs import fix_case, get_names, log_movie
#%% Setup

#Exceptions
manual_exceptions = ['Handmaids']
corrections = ['Handmaid%27s']

subs = ('.srt', '.sub')

no_good = [':', '*', '?', '"', '|', '/', '<', '>']

dont_uppercase = ['of','a', 'and', 'in', 'the', 'to', 'do', 'at', 'but', 'or', 
                  'for', 'nor', 'on', 'from', 'by']

#Paths
path = "E:/Torrent"
move_path = "E:/Move/"
check_path = "E:/Check/"
log_path = "E:/Move/Film_log.txt"

#%% Autonamer
folders = os.listdir(path)
folders.remove('temp')

for folder in folders:
    if os.path.isdir(path+'/'+folder):
        continue
    else:
        folders.remove(folder)
        
if len(folders) != 0:
    for folder in folders:
        total_path = path + '/' + folder
        files = os.listdir(path+'/'+folder)
        folder_name = folder.split('.')
        movie = None
        for i in range(len(folder_name)):
            if folder_name[i][0].lower() == 's' and folder_name[i][1:3].isdigit():
                int(folder_name[i][1:3])
                name_list = folder_name[0:i]
                name_list = [word.capitalize() for word in name_list]
                name_list = fix_case(name_list, dont_uppercase)
                season = folder_name[i][1:3]
                movie = False
                break
        if movie is None:
            for i in range(len(folder_name)):
                if folder_name[i:i+4].isdigit():
                    name_list = folder_name[0:i]
                    name_list = [word.capitalize() for word in name_list]
                    name_list = fix_case(name_list, dont_uppercase)
                    movie = True
                    break        

        if movie is None:
            os.rename(total_path, check_path + folder)
            pass

        if not movie:
           name = ' '.join(name_list)
           names, type_ = get_names(name_list, season, manual_exceptions, corrections, no_good)
           network_folder_name = name + '/'
           season = 'Season '+ season + '/'
           for file in files:
               keep = False
               file_ = file.split('.')
               extension = file_[-1]
               for word in file_:
                   if len(word) == 6: 
                       if word[0].lower() == 's' and word[3].lower() == 'e':
                           if word[1:3].isdigit() and word[4:].isdigit():
                               episode = word[4:]
                               keep = True
                               break
               if extension == 'mkv' and keep == False:
                   keep = True
                   episode = None
               if keep and episode == None:
                   os.rename(total_path+'/'+file, check_path+network_folder_name)
               elif keep and episode != None:
                       if type_ != 'Miniserier/':
                           if type_ == 'TV_Serie/':
                               type_ = 'Miniserier/'
                           if not os.path.isdir(move_path + type_ + network_folder_name):
                               os.mkdir(move_path + type_ + network_folder_name)
                           if not os.path.isdir(move_path + type_ + network_folder_name + season):
                               os.mkdir(move_path + type_ + network_folder_name + season)
                           if type(names[int(episode)-1]) is not list:
                               os.rename(total_path+'/'+file, move_path + type_ + network_folder_name
                                         + season + episode + ' - ' + names[int(episode)-1]
                                         + '.' + extension)
                           else:
                               episode_ = episode + '+' + str(int(episode)+1)
                               os.rename(total_path+'/'+file, move_path + type_ + network_folder_name
                                         + season + episode_ + ' - ' + names[int(episode)-1][1]
                                         + '.' + extension )
                       elif type_ == 'Miniserier/':
                           if not os.path.isdir(move_path + type_ + network_folder_name):
                               os.mkdir(move_path + type_ + network_folder_name)
                           if type(names[int(episode)-1]) is not list:
                               os.rename(total_path+'/'+file, move_path + type_ + network_folder_name
                                         + episode + ' - ' + names[int(episode)-1] + '.' + extension)
                           else:
                               episode_ = episode + str(int(episode)+1)
                               os.rename(total_path+'/'+file, move_path + type_ + network_folder_name
                                         + episode_ + ' - ' + names[int(episode)-1][1] + '.' + extension)
               else:
                   try:
                       os.remove(total_path+'/'+file)
                   except:
                       shutil.rmtree(total_path+'/'+file)
                   
        elif movie:
            name = ' '.join(name_list)
            destination = move_path + 'Film/'
            log_movie(name, log_path)

        if len(os.listdir(total_path)) == 0:
            os.rmdir(total_path)
