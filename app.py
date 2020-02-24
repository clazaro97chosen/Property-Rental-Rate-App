from flask import Flask, render_template, request, redirect

import joblib, pickle
import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.compose import ColumnTransformer 
from sklearn.preprocessing import RobustScaler
from database import *

model = joblib.load('modeling/model.joblib')
imputer = pickle.load(open('modeling/imputer.pkl','rb'))
scaler = pickle.load(open('modeling/scaler.pkl','rb'))
column_ordering = pickle.load(open('modeling/column_ordering.pkl','rb'))
info_df = pickle.load(open('modeling/info_df.pkl','rb'))

app = Flask(__name__, template_folder='templates')

@app.before_request
def before_request():
    #create db if needed and connect
    initialize_db()

@app.teardown_request
def teardown_request(Exception):
    #close the db connection
    db.close()

@app.route('/info.html', methods=['GET', 'POST'])
def information():
    if request.method == 'GET':
        return render_template('info.html')

    if request.method == 'POST':
        calculator_variable = request.form['calculator_variable']
        city = request.form['user_city']
        user_city = request.form['user_city'].lower()
        user_city = user_city.replace(' ','')
        try:
            result = (info_df.loc[info_df['city']==user_city,calculator_variable]).values[0]
        except:
            return 'Sorry {} was not found please check the spelling or spacing of the city you entered' \
                    '<br/> Or type "cityname,California" into google and use the spelling Google has'\
                    '<br/>Note: unfortunately no data was gathered for'\
                    '<br/>Carmel-By-the-Sea,La-Cañada-Flintridge Paso-Robles, St.Helena, Ventura'.format(city)
        return render_template('info.html',city=city,calculator_variable=calculator_variable,result = result,scroll='viewpoint')

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        #with form prefilled
        return render_template('index.html')

    if request.method == 'POST':
        #render another template with previous input.
        med_owner_cost = request.form['med_owner_cost']
        if med_owner_cost ==0:
            med_owner_cost_value = np.nan
        elif med_owner_cost != 0:
            med_owner_cost_value = med_owner_cost    

        med_hcost_own_wo_mortg = request.form['med_hcost_own_wo_mortg']
        if med_hcost_own_wo_mortg == 0:
            med_hcost_own_wo_mortg_value = np.nan
        elif med_hcost_own_wo_mortg !=0:
            med_hcost_own_wo_mortg_value = med_hcost_own_wo_mortg
        
        med_hcost_ownmortg = np.nan
        hcost_aspercentof_hincome_ownmortg = request.form['hcost_aspercentof_hincome_ownmortg']
        if hcost_aspercentof_hincome_ownmortg == 0:
            hcost_aspercentof_hincome_ownmortg_value = np.nan
        elif hcost_aspercentof_hincome_ownmortg != 0:
            hcost_aspercentof_hincome_ownmortg_value = hcost_aspercentof_hincome_ownmortg

        hcost_as_perc_of_hincome_womortg = request.form['hcost_as_perc_of_hincome_womortg']
        if hcost_as_perc_of_hincome_womortg == 0:
            hcost_as_perc_of_hincome_womortg_value = np.nan
        elif hcost_as_perc_of_hincome_womortg != 0:
            hcost_as_perc_of_hincome_womortg_value = hcost_as_perc_of_hincome_womortg
        
        med_hval_aspercentof_medearn = request.form['med_hval_aspercentof_medearn']
        med_real_estate_taxes = request.form['med_real_estate_taxes']
        med_homeval = request.form['med_homeval']
        median_year_house_built = request.form['median_year_house_built']
        owned_homes = request.form['owned_homes']
        median_num_ofrooms = request.form['median_num_ofrooms']
        rent_home_percent = request.form['rent_home_percent']
        housing_density = request.form['housing_density']
        household_size_for_renters = request.form['household_size_for_renters']
        med_year_renter_moved_in = request.form['med_year_renter_moved_in']
        area_total_sq_mi = request.form['area_total_sq_mi']
        med_year_moved_in_for_owners = request.form['med_year_moved_in_for_owners']
        population = request.form['population']
        housing_units = request.form['housing_units']
        household_size_of_howners = request.form['household_size_of_howners']
        med_own_cost_aspercentof_income = np.nan
        family_members_per_hunit = request.form['family_members_per_hunit']
        

        #finding the appropriate cluster values from the city inputted 
        city = request.form['city']
        user_city = request.form['city'].lower()
        user_city = user_city.replace(' ','')
        try:
            cluster1 = (info_df.loc[info_df['city'] == user_city,'cluster1']).values[0]
            cluster2 = (info_df.loc[info_df['city'] == user_city,'cluster2']).values[0]
        except:
            return 'Sorry {} was not found please check the spelling or spacing of the city you entered' \
            '<br/> Or type "cityname,California" into google and use the spelling Google has' \
            '<br/>Note: unfortunately no data was gathered for'\
            '<br/>Carmel-By-the-Sea,La-Cañada-Flintridge Paso-Robles, St.Helena, Ventura'.format(city)
                    
        
        input_variables = pd.DataFrame([[med_owner_cost_value, med_hcost_ownmortg, med_real_estate_taxes,owned_homes,
                                        median_num_ofrooms,med_homeval,rent_home_percent,housing_density,
                                        med_hcost_own_wo_mortg_value,household_size_for_renters,med_year_renter_moved_in,
                                        median_year_house_built,med_hval_aspercentof_medearn,area_total_sq_mi,
                                        hcost_aspercentof_hincome_ownmortg_value,med_year_moved_in_for_owners,population,housing_units,
                                        household_size_of_howners,med_own_cost_aspercentof_income,family_members_per_hunit,
                                        hcost_as_perc_of_hincome_womortg_value,cluster2,cluster1]],
                                       columns=['med_owner_cost', 'med_hcost_ownmortg', 'med_real_estate_taxes','owned_homes',
                                        'median_num_ofrooms','med_homeval','rent_home_percent','housing_density',
                                        'med_hcost_own_wo_mortg','household_size_for_renters','med_year_renter_moved_in',
                                        'median_year_house_built','med_hval_aspercentof_medearn','area_total_sq_mi',
                                        'hcost_aspercentof_hincome_ownmortg','med_year_moved_in_for_owners','population','housing_units',
                                        'household_size_of_howners','med_own_cost_aspercentof_income','family_members_per_hunit',
                                        'hcost_as_perc_of_hincome_womortg','cluster2','cluster1'],
                                       index=['input'])

        #scale & use model in pipeline
        #input_variables = scaler.transform(input_variables)
        imputed_dat = imputer.transform(input_variables)
        imputed_dat = pd.DataFrame(imputed_dat,columns=column_ordering)
        input_variables = scaler.transform(imputed_dat)

        #return input and prediction
        prediction = round(model.predict(input_variables)[0])
        
        #write to database
        data = request.form.to_dict()

        Housing_Market.create(**data,predicted_rental_rate = prediction)
        #render another template with users input.
        return render_template('submission.html', 
                                city = city,med_owner_cost = med_owner_cost, med_hcost_ownmortg = med_hcost_ownmortg, 
                                                med_real_estate_taxes= med_real_estate_taxes, owned_homes= owned_homes,
                                        median_num_ofrooms = median_num_ofrooms, med_homeval = med_homeval, rent_home_percent = rent_home_percent,
                                        housing_density = housing_density, med_hcost_own_wo_mortg = med_hcost_own_wo_mortg, household_size_for_renters = household_size_for_renters,
                                        med_year_renter_moved_in = med_year_renter_moved_in, median_year_house_built = median_year_house_built,
                                        med_hval_aspercentof_medearn = med_hval_aspercentof_medearn, area_total_sq_mi = area_total_sq_mi,
                                        hcost_aspercentof_hincome_ownmortg = hcost_aspercentof_hincome_ownmortg, med_year_moved_in_for_owners = med_year_moved_in_for_owners,
                                        population = population, housing_units = housing_units, household_size_of_howners = household_size_of_howners, med_own_cost_aspercentof_income  = med_own_cost_aspercentof_income,
                                        family_members_per_hunit = family_members_per_hunit, hcost_as_perc_of_hincome_womortg = hcost_as_perc_of_hincome_womortg,user_rental_rate = request.form['user_rental_rate'],
                                result = prediction,scroll='viewpoint')

if __name__ == '__main__':
    app.run()