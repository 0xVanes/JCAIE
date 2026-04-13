# CAPSTONE 2: DAEGU APARTMENT PRICE PREDICTION

-- DESCRIPTION--
Housing needs of modern society due to limited residential land and dense business in urban areas. Apartment prices are influenced by internal and external factors. It is needed so that individuals or company can make apartment units offers and bidders can sell units on a platform by determining apartment prices since apartment owners are having difficulty in adjusting to market prices (Too high = difficult to make sales and Too low = difficult to maximize profit)

### INSTALL DEPENDENCIES
```
pip install numpy pandas scikit-learn xgboost torch matplotlib seaborn
```
python 3.11.15
### DATASETS
- Hallway type (category), Time to subway (ordinal), Subway station (category), facilities nearby (numerical), university nearby (numerical), public facilities (numerical), school nearby (numerical), parking lot (numerical), yar built (numerical), facilities in aparment (numerical), size (numerical), sale price (numerical - target variable)

### MODELS USED
- Random Forest Regressor
- XGBoost
- ANN Pytorch

### Hyperparameter Tuning
- Each hyperparameters follow a model made by others and published in medium/journal
- GridSearchCV

### Evaluation Metrics
- MAE
- MSE
- RMSE
- R2 Score
- MAPE
- MSELoss

### RESULTS:
- Hasil seluruh model mendekati satu sama lain
- Hasil prediksi XGBoost paling kecil (outlier) dan Pytorch paling besar (scaling)
- Hasil paling stabil Random Forest

### Demo: On Gradio (HuggingFace Space Public or Locally) di Folder Demo or https://huggingface.co/spaces/0xVanes/DaeguApartmentPrediction
'''
python app.py
'''
