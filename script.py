from data_cleanup import *
from robot import *

''' Give the location of the file and the name of the datasheet and mouse ID of interest.
    Finally give the location of the output file'''
file_path = 'Dementia_project.xlsx'
data_sheet = 'Quantification'
miceid_sheet = 'Sheet1'
output_path = ''
control_name = 'WT'

df, df_mice = load_data(file_path, data_sheet, miceid_sheet)
df_filtered, df_eliminated = data_cleanup(df, df_mice)
robot_layer(df_filtered, df_eliminated, 'WT', output_path=output_path)

# TODO: graphs
