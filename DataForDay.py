import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split



date = '2020-08-08'



# Read in data into a dataframe
df = pd.read_csv('data_for_analyze/clear_data.csv')
df_date = df.copy()
df_no_date = df.copy()


#print(df)
for index, row in df.iterrows():
    if row["datetime"][:10] == date:
        df_no_date.drop(index=index, inplace=True)
    else:
        df_date.drop(index=index, inplace=True)
#data = data.drop(columns='timestamp')
#data = data.drop(columns='datetime')
#data = data.drop(columns='zenith')
#data = data.drop(columns='azimuth')
#data = data.drop(columns='dhi')
#data = data.drop(columns='dni')
#data = data.drop(columns='ebh')
#data = data.rem
# Display top of dataframe
df.head()

df.info()
df_date.info()
df_no_date.info()
#data.drop
#correlations_data = data.corr()['actual_power'].sort_values()
#print(correlations_data)

#features = data.copy()


#print(features.shape)
#actual_power = features[features['actual_power'].notnull()]
features_date = df_date.copy()
features_date = features_date.drop(columns='timestamp')
features_date = features_date.drop(columns='datetime')
features_date = features_date.drop(columns='zenith')
features_date = features_date.drop(columns='azimuth')
features_date = features_date.drop(columns='actual_power')


targets_date = df_date.copy()
targets_date = targets_date.drop(columns='timestamp')
targets_date = targets_date.drop(columns='datetime')
targets_date = targets_date.drop(columns='zenith')
targets_date = targets_date.drop(columns='azimuth')
targets_date = targets_date.drop(columns='ghi')
targets_date = targets_date.drop(columns='ebh')
targets_date = targets_date.drop(columns='dni')
targets_date = targets_date.drop(columns='dhi')
targets_date = targets_date.drop(columns='cloud_opacity')
targets_date = targets_date.drop(columns='air_temp')

print(features_date.info())
print(targets_date.info())

features_no_date = df_no_date.copy()
features_no_date = features_no_date.drop(columns='timestamp')
features_no_date = features_no_date.drop(columns='datetime')
features_no_date = features_no_date.drop(columns='zenith')
features_no_date = features_no_date.drop(columns='azimuth')
features_no_date = features_no_date.drop(columns='actual_power')


targets_no_date = df_no_date.copy()
targets_no_date = targets_no_date.drop(columns='timestamp')
targets_no_date = targets_no_date.drop(columns='datetime')
targets_no_date = targets_no_date.drop(columns='zenith')
targets_no_date = targets_no_date.drop(columns='azimuth')
targets_no_date = targets_no_date.drop(columns='ghi')
targets_no_date = targets_no_date.drop(columns='ebh')
targets_no_date = targets_no_date.drop(columns='dni')
targets_no_date = targets_no_date.drop(columns='dhi')
targets_no_date = targets_no_date.drop(columns='cloud_opacity')
targets_no_date = targets_no_date.drop(columns='air_temp')

print(features_no_date.info())
print(targets_no_date.info())

#features = actual_power.drop(columns='actual_power')
#targets = pd.DataFrame(actual_power['actual_power'])

# Replace the inf and -inf with nan (required for later imputation)
#features = features.replace({np.inf: np.nan, -np.inf: np.nan})

# Split into 70% training and 30% testing set
#X, X_test, y, y_test = train_test_split(features, targets, test_size = 0.25, random_state = 32)



#print(X.shape)
#print(X_test.shape)
#print(y.shape)
#print(y_test.shape)


features_no_date.to_csv(date+'/training_features.csv', index = False)
features_date.to_csv(date+'/testing_features.csv', index = False)
targets_no_date.to_csv(date+'/training_labels.csv', index = False)
targets_date.to_csv(date+'/testing_labels.csv', index = False)