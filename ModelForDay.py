# Pandas and numpy for data manipulation
import matplotlib
import pandas as pd
import numpy as np

# No warnings about setting value on copy of slice
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', 60)


date = "2020-08-08"
# Matplotlib for visualization
import matplotlib.pyplot as plt
#%matplotlib inline

# Set default font size
plt.rcParams['font.size'] = 24

from IPython.core.pylabtools import figsize

# Seaborn for visualization
import seaborn as sns
sns.set(font_scale = 2)

# Imputing missing values and scaling values
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer


# Machine Learning Models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

# Hyperparameter tuning
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV



# Read in data into dataframes
train_features = pd.read_csv(date+'/training_features.csv')
test_features = pd.read_csv(date+'/testing_features.csv')
train_labels = pd.read_csv(date+'/training_labels.csv')
test_labels = pd.read_csv(date+'/testing_labels.csv')

# Display sizes of data
print('Training Feature Size: ', train_features.shape)
print('Testing Feature Size:  ', test_features.shape)
print('Training Labels Size:  ', train_labels.shape)
print('Testing Labels Size:   ', test_labels.shape)


figsize(8, 8)

# Histogram of the Energy Star Score
#plt.style.use('fivethirtyeight')
#plt.hist(train_labels['actual_power'].dropna(), bins = 100)
#plt.xlabel('actual_power'); plt.ylabel('Number of Buildings')
#plt.title('ENERGY Star Score Distribution')
#plt.show()



#imputer = Imputer(strategy='median')
imputer = SimpleImputer(missing_values=np.nan, strategy='median')

# Train on the training features
imputer.fit(train_features)

# Transform both training data and testing data
X = imputer.transform(train_features)
X_test = imputer.transform(test_features)

print('Missing values in training features: ', np.sum(np.isnan(X)))
print('Missing values in testing features:  ', np.sum(np.isnan(X_test)))


print(np.where(~np.isfinite(X)))
print(np.where(~np.isfinite(X_test)))

scaler = MinMaxScaler(feature_range=(0, 1))

# Fit on the training data
scaler.fit(X)

# Transform both the training and testing data
X = scaler.transform(X)
X_test = scaler.transform(X_test)


y = np.array(train_labels).reshape((-1, ))
y_test = np.array(test_labels).reshape((-1, ))




def mae(y_true, y_pred):
    return np.mean(abs(y_true - y_pred))


# Takes in a model, trains the model, and evaluates the model on the test set
def fit_and_evaluate(model):
    # Train the model
    model.fit(X, y)

    # Make predictions and evalute
    model_pred = model.predict(X_test)
    model_mae = mae(y_test, model_pred)

    # Return the performance metric
    return model_mae


lr = LinearRegression()
lr_mae = fit_and_evaluate(lr)

print('Linear Regression Performance on the test set: MAE = %0.4f' % lr_mae)


svm = SVR(C = 1000, gamma = 0.1)
svm_mae = fit_and_evaluate(svm)

print('Support Vector Machine Regression Performance on the test set: MAE = %0.4f' % svm_mae)



random_forest = RandomForestRegressor(random_state=1)
random_forest_mae = fit_and_evaluate(random_forest)

print('Random Forest Regression Performance on the test set: MAE = %0.4f' % random_forest_mae)



gradient_boosted = GradientBoostingRegressor(random_state=13)
gradient_boosted_mae = fit_and_evaluate(gradient_boosted)

print('Gradient Boosted Regression Performance on the test set: MAE = %0.4f' % gradient_boosted_mae)


knn = KNeighborsRegressor(n_neighbors=10)
knn_mae = fit_and_evaluate(knn)

print('K-Nearest Neighbors Regression Performance on the test set: MAE = %0.4f' % knn_mae)


#plt.style.use('fivethirtyeight')
#figsize(8, 6)

# Dataframe to hold the results
model_comparison = pd.DataFrame({'model': ['Linear Regression', 'Support Vector Machine',
                                           'Random Forest', 'Gradient Boosted',
                                            'K-Nearest Neighbors'],
                                 'mae': [lr_mae, svm_mae, random_forest_mae,
                                         gradient_boosted_mae, knn_mae]})

# Horizontal bar chart of test mae
#model_comparison.sort_values('mae', ascending = False).plot(x = 'model', y = 'mae', kind = 'barh', color = 'red', edgecolor = 'black')

# Plot formatting
#plt.ylabel(''); plt.yticks(size = 14); plt.xlabel('Mean Absolute Error'); plt.xticks(size = 14)
#plt.title('Model Comparison on Test MAE', size = 20);


default_model = GradientBoostingRegressor(random_state = 42)

# Select the best model
file_text = 'id,actual,predicted\n'
final_model = svm
final_pred = final_model.predict(X_test)
for i in range(len(final_pred)):
    file_text = file_text+str(i)+','+str(int(y_test[i]))+','+str(int(final_pred[i]))+'\n'
    if not y_test[i] == 0:
        if y_test[i] > 5000:
            print((round((y_test[i]-final_pred[i])/y_test[i]*100)), round(y_test[i]), " - ", round(final_pred[i]))
with open(date+'/final_data.csv', 'w') as f2:
    f2.write(file_text)
f2.close()


total_produced_power = 0
total_predicted_power = 0

hours_file_text = 'id,actual,predicted,error\n'
hours_data = []
for i in range(0,int(len(y_test)/12)):
    actual_power = 0
    predicted_power = 0
    for j in range(0,12):
        actual_power = actual_power + y_test[i*12+j]/12
        if final_pred[i*12+j]>0:
            predicted_power = predicted_power + final_pred[i*12+j]/12
    hours_data.append([i,actual_power,predicted_power])
    error = 0.0
    total_produced_power = total_produced_power + actual_power
    total_predicted_power = total_predicted_power + predicted_power
    if actual_power>0:
        error = abs(actual_power-predicted_power)/actual_power
    hours_file_text = hours_file_text + str(i) + ',' + str(int(actual_power)) + ',' + str(int(predicted_power))+','+str(int(error*100))+'\n'
#print(hours_data)

with open(date+'/final_data_hours.csv', 'w') as f3:
    f3.write(hours_file_text)
f3.close()

total_error = int(abs(total_produced_power-total_predicted_power)/total_produced_power*100)
day_summary_text = "Total produced power: "+ str(int(total_produced_power))+"kW"+"\n"
day_summary_text = day_summary_text + "Total predicted power: "+ str(int(total_predicted_power))+"kW"+"\n"
day_summary_text = day_summary_text + "Day inaccuracy: "+ str(total_error)+'%'+"\n"

with open(date+'/day_summary.txt', 'w') as f4:
    f4.write(day_summary_text)
f4.close()


figsize(8, 8)

# Density plot of the final predictions and the test values
sns.kdeplot(final_pred, label = 'Predictions')
sns.kdeplot(y_test, label = 'Values')

# Label the plot
plt.xlabel('Energy Star Score');
plt.ylabel('Density');
plt.title('Test Values and Predictions');
#plt.show()

