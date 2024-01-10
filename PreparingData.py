import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split





# Read in data into a dataframe
data = pd.read_csv('data_for_analyze/clear_data.csv')
data = data.drop(columns='timestamp')
data = data.drop(columns='datetime')
data = data.drop(columns='zenith')
data = data.drop(columns='azimuth')
#data = data.drop(columns='dhi')
#data = data.drop(columns='dni')
#data = data.drop(columns='ebh')

# Display top of dataframe
data.head()

data.info()
#data.drop
correlations_data = data.corr()['actual_power'].sort_values()
print(correlations_data)

features = data.copy()


print(features.shape)
actual_power = features[features['actual_power'].notnull()]


features = actual_power.drop(columns='actual_power')
targets = pd.DataFrame(actual_power['actual_power'])

# Replace the inf and -inf with nan (required for later imputation)
features = features.replace({np.inf: np.nan, -np.inf: np.nan})

# Split into 70% training and 30% testing set
X, X_test, y, y_test = train_test_split(features, targets, test_size = 0.25, random_state = 32)

print(X.shape)
print(X_test.shape)
print(y.shape)
print(y_test.shape)

def mae(y_true, y_pred):
    return np.mean(abs(y_true - y_pred))


baseline_guess = np.median(y)

print('The baseline guess is a score of %0.2f' % baseline_guess)
print("Baseline Performance on the test set: MAE = %0.4f" % mae(y_test, baseline_guess))

#no_score.to_csv('data/no_score.csv', index = False)
X.to_csv('data_for_analyze/training_features.csv', index = False)
X_test.to_csv('data_for_analyze/testing_features.csv', index = False)
y.to_csv('data_for_analyze/training_labels.csv', index = False)
y_test.to_csv('data_for_analyze/testing_labels.csv', index = False)