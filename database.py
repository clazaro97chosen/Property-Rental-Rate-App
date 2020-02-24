from peewee import *

db = SqliteDatabase('housing.db')

class Housing_Market(Model):
    id = PrimaryKeyField()
    city = TextField()
    med_owner_cost = FloatField()
    med_hcost_own_wo_mortg = FloatField()
    hcost_aspercentof_hincome_ownmortg = FloatField()
    hcost_as_perc_of_hincome_womortg = FloatField()
    med_hval_aspercentof_medearn = FloatField()
    med_real_estate_taxes = FloatField()
    med_homeval = FloatField()
    median_year_house_built = FloatField()
    median_num_ofrooms = FloatField()
    family_members_per_hunit = FloatField()
    household_size_of_howners = FloatField()
    household_size_for_renters = FloatField()
    med_year_renter_moved_in = FloatField()
    med_year_moved_in_for_owners = FloatField()
    housing_units = FloatField()
    owned_homes = FloatField()
    rent_home_percent = FloatField()
    housing_density = FloatField()
    area_total_sq_mi = FloatField()
    population = FloatField()
    user_rental_rate = FloatField()
    predicted_rental_rate = FloatField()
    
    class Meta:
        database = db

def initialize_db():
    db.connect()
    db.create_tables([Housing_Market],safe = True)

