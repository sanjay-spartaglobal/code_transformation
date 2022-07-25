import pandas as pd

# load csv results file
read_df = pd.read_csv('al_results_2020.csv', index_col='index', low_memory=False)

# remove the 3 unwanted columns
df = read_df.drop(columns=['Zscore', 'gender', 'syllabus'])

# drop missing values in dataframe
df = df.dropna()

# removing rows where student was absent from assesments
absent_sub1 = df['sub1_r'] == 'Absent'
absent_sub2 = df['sub2_r'] == 'Absent'
absent_sub3 = df['sub3_r'] == 'Absent'
absent_cgt = df['cgt_r'] == 'Absent'
absent_eng = df['general_english_r'] == 'Absent'
all_absences_series = absent_sub1 & absent_sub2 & absent_sub3 & absent_cgt & absent_eng

# new dataframe object without absence on all exams
clean_df = df[~all_absences_series]


months_dict = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
               'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}

clean_df['birth_month'] = clean_df['birth_month'].apply(lambda key: months_dict[key])

#  concatenate birth_day, birth_month and birth_day to form new birthdate column
clean_df['birth_date'] = clean_df['birth_day'].astype(str) + '-' + clean_df['birth_month'] + '-' + clean_df[
    'birth_year'].astype(str)

clean_df['birth_date'] = pd.to_datetime(clean_df['birth_date'], format='%d-%m-%Y', errors='course')

clean_df = clean_df.drop(columns=['birth_day', 'birth_month', 'birth_year'])

# save cleaned dataframe to new csv file
clean_df.to_csv('cleaned_results.csv')
