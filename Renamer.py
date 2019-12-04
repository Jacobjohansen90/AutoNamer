# -*- coding: utf-8 -*-
"""
Jacobs Autonamer
"""
import os
import shutil
from AutoNamerFuncs import fix_case, get_names
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
        for i in range(len(folder_name)):
            if folder_name[i][0].lower() == 's' and folder_name[i][1:3].isdigit():
                int(folder_name[i][1:3])
                name_list = folder_name[0:i]
                name_list = [word.capitalize() for word in name_list]
                name_list = fix_case(name_list, dont_uppercase)
                season = folder_name[i][1:3]
                movie = False
                break
            elif folder_name[i].isdigit():
                name_list = folder_name[0:i]
                name_list = [word.capitalize() for word in name_list]
                name_list = fix_case(name_list, dont_uppercase)
                movie = True
                break
        if not movie:
           name = ' '.join(name_list)
           names, type_ = get_names(name_list, season)
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



#You are here
               if keep:
                   if not os.path.isdir(done_path+network_folder):
                       os.mkdir(done_path+network_folder)
                   if not miniseries:
                       if not os.path.isdir(done_path+network_folder+season):
                           os.mkdir(done_path+network_folder+season)
                       if type(names[int(episode)-1]) is not list:
                           os.rename(total_path+'/'+file, done_path + network_folder + season + episode + ' - ' + names[int(episode)-1]+'.'+extension)
                       else:
                           episode = int(episode)
                           episode_ = str(episode) + '+' + str(episode+1)
                           os.rename(total_path+'/'+file, done_path + network_folder + season + episode_ + ' - ' + names[int(episode)-1][1]+'.'+extension)
                   else:
                       if len(names[int(episode)-1]) == 1:
                           os.rename(total_path+'/'+file, done_path + network_folder + episode + ' - ' + names[int(episode)-1]+'.'+extension)
                       else:
                           episode = int(episode)
                           episode = str(episode) + '+' + str(episode+1)
                           os.rename(total_path+'/'+file, done_path + network_folder + episode + ' - ' + names[int(episode)-1]+'.'+extension)
               else:
                   try:
                       os.remove(total_path+'/'+file)
                   except:
                       shutil.rmtree(total_path+'/'+file)
        elif is_series == False:
            continue
            #name = ' '.join(name_list)
            #destination = move_path + 'Film/'
            #log_movie(name)
           
        else:
            shutil.move(path+'/'+folder, move_path)
        
        if len(os.listdir(total_path)) == 0:
            os.rmdir(total_path)


