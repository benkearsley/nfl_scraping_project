import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd 
from mypackage import cleaning_functions as cf
from mypackage import scraping_functions as sf


def predict_wins(plays, train_data):


    # Prepare Training Data
    train_data['seconds_left'] = train_data.apply(cf.seconds_left, axis=1)
    train_data['score_diff'] = train_data.iloc[:,5].astype(float) - train_data.iloc[:,6].astype(float)
    train_data['adjusted_score'] = train_data.apply(cf.adjusted_score_calc, axis=1)
    train_data['win_team'] = train_data.apply(lambda row: cf.win(pd.DataFrame(row).transpose()), axis=1)
    
    y_train = train_data['win_team']
    y_train = y_train.apply(lambda x:float(x[0]))

    columns_to_drop = [5, 6]
    additional_columns_to_drop = ['Quarter', 'Detail', 'Location', 'Time', 'win_team', 'play_start_time', 'game_id', 'win_team']

    train_data = train_data.drop(columns=train_data.columns[columns_to_drop])
    train_data = train_data.drop(columns=additional_columns_to_drop)
    train_data['field_side'] = pd.Categorical(train_data['field_side'])
    train_data['Play_Type'] = pd.Categorical(train_data['Play_Type'])
    train_data['possession'] = pd.Categorical(train_data['possession'])
    train_data['Down'] = pd.Categorical(train_data['Down'])
    train_data['ToGo'] = pd.to_numeric(train_data['ToGo'], errors='coerce')
    train_data['ToGo'] = train_data['ToGo'].astype(float)
    train_data['EPB'] = train_data['EPB'].astype(float)
    train_data['EPA'] = train_data['EPA'].astype(float)
    train_data = pd.get_dummies(train_data, columns=['Play_Type', 'Down', 'field_side', 'possession'])

    train_data = train_data.fillna(0)

    # Prepare Test Data
    plays['seconds_left'] = plays.apply(cf.seconds_left,axis =1)
    plays['score_diff'] = plays.iloc[:,5].astype(float) - plays.iloc[:,6].astype(float)
    plays['adjusted_score'] = plays.apply(cf.adjusted_score_calc,axis=1)
    plays['win_team'] = plays.apply(lambda row: cf.win(pd.DataFrame(row).transpose()), axis=1)

    new_data = plays.drop(columns=plays.columns[columns_to_drop])
    # Optionally, you can also drop additional columns
    additional_columns_to_drop = ['Quarter', 'Detail', 'Location', 'Time', 'win_team', 'play_start_time']
    new_data = new_data.drop(columns=additional_columns_to_drop)
    new_data['field_side'] = pd.Categorical(new_data['field_side'])
    new_data['Play_Type'] = pd.Categorical(new_data['Play_Type'])
    new_data['possession'] = pd.Categorical(new_data['possession'])
    new_data['Down'] = pd.Categorical(new_data['Down'])
    new_data['ToGo'] = pd.to_numeric(new_data['ToGo'], errors='coerce')
    new_data['ToGo'] = new_data['ToGo'].astype(float)
    new_data['EPB'] = new_data['EPB'].astype(float)
    new_data['EPA'] = new_data['EPA'].astype(float)
    new_data = pd.get_dummies(new_data, columns=['Play_Type', 'Down', 'field_side', 'possession'])
    y = plays['win_team']
    y = y.apply(lambda x:float( x[0]))
    new_data = new_data.fillna(0)
    X_test = new_data.drop(columns='win_team')

    rf_classifier = RandomForestClassifier(n_estimators=400, random_state=42)
    rf_classifier.fit(train_data, y_train)
    y_pred = rf_classifier.predict(X_test)
    accuracy = accuracy_score(y, y_pred)
    print(f'accuracy: {accuracy}')

    post_data = X_test
    post_data['y_actuals'] = y
    post_data['y_pred'] = y_pred
    return accuracy, post_data

    