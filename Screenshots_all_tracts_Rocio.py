#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Create MrView Screenshots
#Written by Rocio Velasco Poblaciones, 2022 
import glob 
import os
import numpy as np
from tqdm import tqdm

#individual_subjects = False # Modify this like to a list of subjects to avoid doing all. Example below.
individual_subjects = ['18112']

def get_latest_file_from_list(files_folder):
    creation_time_list=list()
    
    for i in files_folder: 
         creation_time_list.append(os.path.getctime(i))                        
    creation_time_array = np.array(creation_time_list)
    latest_file = np.array(files_folder)[creation_time_array == np.max(creation_time_array)][0]
    return(latest_file)


def get_tract_from_subject_id(tracts_path, subject_id, pattern_to_search):
    print("Looking for : "       + tracts_path + str(subject_id) + "/*" + pattern_to_search)
    files_with_pattern = glob.glob(tracts_path + str(subject_id) + "/*" + pattern_to_search)
    
    
    # Files with pattern is a list, that might contain multiple files. We need the latest one
    if len(files_with_pattern)!=0:
        latest_file_with_pattern = get_latest_file_from_list(files_with_pattern)
    else:
        latest_file_with_pattern = 'None'
        
    print("Latest file with pattern:" + latest_file_with_pattern)
    # Get latest files with pattern allows us to ensure that we use only one, the newest.
    return(latest_file_with_pattern)


def exec_mrview(output_folder,subject_id,t1_file,file_name,pattern_file_name):
    os.system("mkdir " + output_folder)
    print(output_folder)    

    comand_mrview_coronal = 'mrview "' + t1_file + '" -plane 1 -imagevisible 1 -tractography.load "' + file_name + '" -tractography.slab -1 -tractography.geometry pseudotubes -capture.folder '+output_folder+' -capture.prefix '+str(subject_id)+'_' +str(pattern_file_name.replace(".tck",""))+'_Coronal -capture.grab -exit'
    print(comand_mrview_coronal )
    if (t1_file!='None') & (file_name!='None'):
        os.system(comand_mrview_coronal)
    else:
        print('No file')

    comand_mrview_axial = 'mrview "' + t1_file + '" -plane 0 -imagevisible 1 -tractography.load "' + file_name + '" -tractography.slab -1 -tractography.geometry pseudotubes -capture.folder '+output_folder+' -capture.prefix '+str(subject_id)+'_' +str(pattern_file_name.replace(".tck",""))+'_Saggital -capture.grab -exit'
    print(comand_mrview_axial )
    if (t1_file!='None') & (file_name!='None'):
        os.system(comand_mrview_axial)
    else:
        print('No file')
    print('End_of_line')
    
    
    
    
    
#Include the files we want to have the screenshots
file_name_list=['LCST_wbt_noEval_clean.tck',
                'CFMaj_wbt_noEval_clean.tck',
                'CC_Mot_wbt_noEval_clean.tck',
                'CC_Occ_wbt_noEval_clean.tck', 
                'CC_OrbFron_wbt_noEval_clean.tck',
                'CC_PostPar_wbt_noEval_clean.tck', 
                'CC_SupFron_wbt_noEval_clean.tck',
                'CC_SupPar_wbt_noEval_clean.tck',
                'CC_Temp_wbt_noEval_clean.tck',
                'CC_AntFron_wbt_noEval_clean.tck',
                'CFMin_wbt_noEval_clean.tck',
                'LAF_wbt_noEval_clean.tck',
                'LATR_wbt_noEval_clean.tck',
                'LCC_wbt_noEval_clean.tck',
                'LCH_wbt_noEval_clean.tck',
                'LCST_wbt_noEval_clean.tck',
                'LICP_wbt_noEval_clean.tck',
                'LIFOF_wbt_noEval_clean.tck',
                'LILF_wbt_noEval_clean.tck',
                'LSCP_wbt_noEval_clean.tck',
                'LSLF_wbt_noEval_clean.tck',
                'LUF_wbt_noEval_clean.tck',
                'MCP_wbt_noEval_clean.tck',
                'RAF_wbt_noEval_clean.tck',
                'RATR_wbt_noEval_clean.tck',
                'RCC_wbt_noEval_clean.tck',
                'RCH_wbt_noEval_clean.tck',
                'RCST_wbt_noEval_clean.tck',
                'RICP_wbt_noEval_clean.tck',
                'RIFOF_wbt_noEval_clean.tck',
                'RILF_wbt_noEval_clean.tck',
                'RSCP_wbt_noEval_clean.tck',
                'RSLF_wbt_noEval_clean.tck']

t1_pattern='t1.nii.gz'

#Path to the folder with files 
tracts_path = "/Volumes/share$/Travis-Lab/MRI/neonateMRIdata/FWAnalyses/SDKApr2022/PTNeonateBrain/"
#Folder list is a list of folders included in the directory (tracts_path)

# This part of the code looks for the folders with the subjects ids as names
# If individual_subjects variable is set to False (by default), the code looks for all folders 
# named with 5 numbers inside tracts_path. 

if individual_subjects is False:
    folder_list= glob.glob(tracts_path + '[0-9][0-9][0-9][0-9][0-9]/')
# If individual_subjects is set to a list of folder names (i.e., ['12345', '12346']), then we generate 
# a custom list of folders to analyze in folder_list, basically containing the paths to those folders. 
# Example: 
# folder_list = ['/PATH/TO/FOLDER/12345', '/PATH/TO/FOLDER/12346/']
else:
    folder_list = []
    
    for individual_subject_id in individual_subjects:
        folder_list.append(tracts_path + individual_subject_id + "/")

        

for i in tqdm(folder_list): # For all the folders 
    subject_id = i.split("/")[-2] # This line of code gets the subject id from the path - Find a better way
    print(subject_id)
    
    t1_file = get_tract_from_subject_id(tracts_path=tracts_path,
                                              subject_id=subject_id,
                                              pattern_to_search=t1_pattern)
    
    
    for pattern_file_name in file_name_list: # Now we iterate for all the tracts in the subject id
        file_name = get_tract_from_subject_id(tracts_path=tracts_path,
                                              subject_id=subject_id,
                                              pattern_to_search=pattern_file_name)
        
    

        # This is the destination folder for the screenshots
        output_folder= '/Volumes/share$/Travis-Lab/MRI/neonateMRIdata/FWAnalyses/MCHRI/SDK_MCHRI_b700/screenshots_b700/' +str(subject_id)
        # This is a list of the existing pngs. 
        existing_files=glob.glob(output_folder +'/*.png')

        # Lets find the files inside subject_id folder that contain the strings stored in 
        # file_name_list. We also want to get the newest one 
        
        
        
        # If there are pngs, dont do it. 
        #if len(existing_files)==0:
        exec_mrview(output_folder,subject_id,t1_file,file_name,pattern_file_name)   
        


# In[ ]:




