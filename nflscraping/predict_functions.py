import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_curve, auc
import pandas as pd 
import numpy as np
from nflscraping import cleaning_functions as cf
from nflscraping import scraping_functions as sf
import seaborn as sns
import matplotlib.pyplot as plt


def predict_wins(test_data, train_data, n_estimators=400, random_state=42):
    """
    Train a Random Forest classifier on the provided training data and predict
    the outcome of wins on the given test data.

    Dataframes input as test_data or train_data must fit a certain format,
    namely that output by the the scraping functions scrape_game_data function.

    Parameters:
    -----------
    test_data : pandas.DataFrame
        DataFrame containing the test data.
    train_data : pandas.DataFrame
        DataFrame containing the training data.
    n_estimators : int, optional, default: 400
        The number of trees in the forest.
    random_state : int, optional, default: 42
        Controls the randomness of the estimator.

    Returns:
    --------
    tuple
        A tuple containing the accuracy score of the predictions and a DataFrame
        with additional information including actual and predicted values.

    Notes:
    ------
    - The function performs data preprocessing on both training and test data,
      including dropping rows with missing values, creating new features, and
      converting categorical variables into dummy variables.
    - It uses a RandomForestClassifier for prediction with specified `n_estimators`
      and `random_state`.
    - The accuracy of the predictions is calculated using accuracy_score from scikit-learn.

    Example:
    --------
    >>> accuracy, post_data = predict_wins(test_data, train_data, n_estimators=500, random_state=0)
    >>> print(f'Accuracy: {accuracy}')
    >>> print(post_data.head())
    """
    # Prepare Training Data
    train_data = train_data.dropna(subset=['Down'])
    train_data = train_data[train_data['Down'] != '']
    train_data['seconds_left'] = train_data.apply(cf.seconds_left, axis=1)
    train_data['score_diff'] = train_data.iloc[:,5].astype(float) - train_data.iloc[:,6].astype(float)
    train_data['adjusted_score'] = train_data.apply(cf.adjusted_score_calc, axis=1)
    train_data['win_team'] = train_data.apply(lambda row: cf.win(pd.DataFrame(row).transpose()), axis=1)

    y_train = train_data['win_team']
    y_train = y_train.apply(lambda x:float(x[0]))

    columns_to_drop = [5, 6]
    additional_columns_to_drop = ['Quarter', 'Detail', 'Location', 'Time', 'win_team', 'play_start_time', 'game_id', 'win_team', 'posession']

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
    test_data = test_data.dropna(subset=['Down'])
    test_data = test_data[test_data['Down'] != '']
    test_data['seconds_left'] = test_data.apply(cf.seconds_left, axis=1)
    test_data['score_diff'] = test_data.iloc[:,5].astype(float) - test_data.iloc[:,6].astype(float)
    test_data['adjusted_score'] = test_data.apply(cf.adjusted_score_calc, axis=1)
    test_data['win_team'] = test_data.apply(lambda row: cf.win(pd.DataFrame(row).transpose()), axis=1)
    test_data['win_team'] = test_data.apply(lambda row: cf.win(pd.DataFrame(row).transpose()), axis=1)

    y = test_data['win_team']
    columns_to_drop = [5, 6]
    additional_columns_to_drop = ['Quarter', 'Detail', 'Location', 'Time', 'win_team', 'play_start_time', 'game_id', 'win_team']
    new_data = test_data.drop(columns=test_data.columns[columns_to_drop])
    # Optionally, you can also drop additional columns
    additional_columns_to_drop = ['Quarter', 'Detail', 'Location', 'Time', 'win_team', 'play_start_time']
    new_data = new_data.drop(columns=additional_columns_to_drop)

    new_data['field_side'] = pd.Categorical(new_data['field_side'])
    new_data['Play_Type'] = pd.Categorical(new_data['Play_Type'])
    new_data['possession'] = pd.Categorical(new_data['possession'])
    new_data['Down'] = new_data['Down'].astype(float)
    new_data['Down'] = pd.Categorical(new_data['Down'])
    new_data['ToGo'] = pd.to_numeric(new_data['ToGo'], errors='coerce')
    new_data['ToGo'] = new_data['ToGo'].astype(float)
    new_data['EPB'] = new_data['EPB'].astype(float)
    new_data['EPA'] = new_data['EPA'].astype(float)
    new_data['yardline'] = new_data['yardline'].astype(float)
    new_data = pd.get_dummies(new_data, columns=['Play_Type', 'Down', 'field_side', 'possession'])

    y = y.apply(lambda x:float( x[0]))
    new_data = new_data.fillna(0)

    rf_classifier = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    rf_classifier.fit(train_data, y_train)
    y_pred = rf_classifier.predict(new_data)
    accuracy = accuracy_score(y, y_pred)
    print(f'accuracy: {accuracy}')

    post_data = new_data
    post_data['y_actuals'] = y
    post_data['y_pred'] = y_pred

    fpr, tpr, _ = roc_curve(y, y_pred)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = {:.2f})'.format(roc_auc))
    plt.plot([0,1], [0,1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc='lower right')
    plt.show()
    

    return accuracy, post_data

    