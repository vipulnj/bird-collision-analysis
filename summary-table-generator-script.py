
'''
THIS SCRIPT WAS WRITTEN AFTER THE ANALYSIS ON IPYTHON NOTEBOOK FILE.
BUT, THE OUTPUT OF THE SCRIPT IS THE SAME AS THE IPYTHON NOTEBOOK FILE. 
THIS MAKES THE GENERATION SCRIPT AVAILABLE IN SCRIPT FORM TO ACCEPT COMMAND LINE ARGUMENTS
AND SKIPS OVER SOME OF THE VISUALIZATION AND VERFICICATION PART OF THE ORIGINAL FILE
AND GETS STRAIGHT DOWN TO PERFORMING THE TRANSFORMATIONS.
'''


# 1. We first accept the inputDir and outputDir as inputs to the script. 
# These arguments will tells us where to read the JSONs from and write the resulting CSVs.

# import libraries
import sys, os, utils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore") # doing this for readability only

# loads paths to JSON files
inputDir, outputDir = sys.argv[1], sys.argv[2]

jsonFile_lightLevels = os.path.join(inputDir, 'light_levels.json')
jsonFile_flightCall = os.path.join(inputDir, 'flight_call.json')
jsonFile_chicagoCollisionData = os.path.join(inputDir, 'chicago_collision_data.json')

if not os.path.exists(inputDir):
    print("Please create the specified input dir and place 'light_levels.json', 'flight_call.json' and 'chicago_collision_data.json' inside it.")
    os._exit(1)

if not os.path.exists(jsonFile_lightLevels):
    print(f"NOT FOUND :: {jsonFile_lightLevels}")
    os._exit(1)
if not os.path.exists(jsonFile_lightLevels):
    print(f"NOT FOUND :: {jsonFile_flightCall}")
    os._exit(1)
if not os.path.exists(jsonFile_lightLevels):
    print(f"NOT FOUND :: {jsonFile_chicagoCollisionData}")
    os._exit(1)

# create outputDir if it does not exist
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

# 2. Then, we check if the JSON files in the directory are valid JSON files. 
# Once done evaluating that, we check if there are missing serial numbers in the JSON 
# which might to some missing rows in the table we will generate.

''' THIS HAS BEEN ANALYZED IN THE IPYTHON NOTEBOOK FILE '''





# 3. Next, we create dataframe objects using the JSONs 
# which would in `df_lightLevels`, `df_flightCall` and `df_chicagoCollisionData`. 

df_lightLevels = pd.read_json(jsonFile_lightLevels)
df_flightCall = pd.read_json(jsonFile_flightCall)
df_chicagoCollisionData = pd.read_json(jsonFile_chicagoCollisionData)





# 4. Some of the column names in the dataframes need to be fixed. Some of this information can be found in the supplemental material.

# Supplemental material: 
# https://royalsocietypublishing.org/action/downloadSupplement?doi=10.1098%2Frspb.2019.0364&file=rspb20190364supp1.pdf

# we're given that df_flightCall has incorrect column names in the problem statement itself
df_flightCall.rename(columns = {
    "Species": "Genus", # given in problem statement
    "Family": "Species", # given in problem statement
    "Collisions": "Family", # given in problem statement
    "Call": "Flight Call", # given in problem statement
    "Flight": "Collisions" # found this in supplemental material -- Table S1, explained later
}, inplace=True)


df_lightLevels.rename(columns={
    "Light Score ": "Light Score" # remove the extra space in df_lightLevels['Light Score ']
}, inplace=True)






# 5. Next, we delete duplicated rows in `df_lightLevels` and `df_flightCall` dataframes. 
# We do NOT delete duplicate in `df_chicagoCollisionData` since each row in this dataframe is an occurence of collision.

# repeated data in df_flightCall and df_lightLevels is not useful and can interfere with our joins
df_flightCall = df_flightCall.drop_duplicates()
df_lightLevels = df_lightLevels.drop_duplicates()







# 6. Next, we examine the null values in the three dataframes. 

### `df_chicagoCollisionData` and `df_flightCall` have no nulls in any of their columns. 

### However, `df_lightLevels` has nulls values under both the `Date` and `Light Score` columns.

''' THIS HAS BEEN ANALYZED IN THE IPYTHON NOTEBOOK FILE '''





# 7. Next, we examine for unique values in the columns of all the dataframes. 

### check for unique values on some of the columns where we can investigate. 

### This is where we clean up text by fixing the case of the text values, 
# leading or trailing whitespace in the text values, fix repeated values or incorrectly spelled values and so on.

# **^^ We see repeat of `'catharus', 'cistothorus', ... 'vireo', 'zonotrichia'` in lower case. Also, since these are Genus part of scientific name, 
# the first letter of all words must be uppercase. This will also fix our issue of repeats due to lower case we just mentioned.**

# **^^ The Species part of the scientific name (consists of Genus and species parts, in this order) needs to start with the lower letter. 
# Hence, we need not change anything here. Also, we do not see any repeats due to casing here.**

# **^^ we see there is a mistake in the spelling for the Icteridae family**

# **^^ changing the casing to lower case and changing the Rare to 'no' will fix this issue. 
# We change 'Rare' to 'no' since the paper makes this assumption**

# **^^ changing the casing to lower case should solve this issue**


# **^^ stripping leading and trailing whitespaces should fix this issue**

''' THIS HAS BEEN ANALYZED IN THE IPYTHON NOTEBOOK FILE '''


# change 'rare' under df_flightCall['Flight Call'] to 'no' since the paper makes this assumption
df_flightCall['Flight Call'] = df_flightCall['Flight Call'].replace('Rare', 'no')

# changed Icteriidae to Icteridae, after verification on Google
df_flightCall['Family'] = df_flightCall['Family'].replace('Icteriidae', 'Icteridae')

# fix casing
df_flightCall['Genus'] = df_flightCall['Genus'].apply(utils.changeToTitleCase)
df_chicagoCollisionData['Genus'] = df_chicagoCollisionData['Genus'].apply(utils.changeToTitleCase)
df_flightCall['Flight Call'] = df_flightCall['Flight Call'].apply(utils.changeToLowerCase)
df_flightCall['Habitat'] = df_flightCall['Habitat'].apply(utils.changeToLowerCase)
df_flightCall['Stratum'] = df_flightCall['Stratum'].apply(utils.changeToLowerCase)








# 8. Next, we try to fix the null values in `df_lightLevels`

''' THIS HAS BEEN ANALYZED IN THE IPYTHON NOTEBOOK FILE '''

# we drop null values of `df_lightLevels` since knowing the light scores without their dates is not useful.
df_lightLevels = df_lightLevels.dropna(subset=['Date'])

# next, we drop dates that occur twice under the dates column. By keeping the first occurence and 
# dropping subsequent occurences, we do not attempt to actively pick the highest light score for a repeating date.
df_lightLevels = df_lightLevels.drop_duplicates(subset='Date', keep='first')

# we also change the datatype under df_lightLevels['Light Score'] to Int16
df_lightLevels['Light Score'] = df_lightLevels['Light Score'].astype('Int16')

# With the remaining valid values in the `Date` column, 
# we extract information like day of week, day of month, day of year, week of year, month, seasons, 
# quarter, year and try to look for trends using them. 

# before we do so, we need to add Seasons information

# https://seasonsyear.com/USA/Illinois/Chicago
Seasons_dict = {
    1: 0, 2: 0, 12: 0, # 0 = Winter
    3: 1, 4: 1, 5: 1,  # 1 = Spring
    6: 2, 7: 2, 8: 2,  # 2 = Summer
    9: 3, 10: 3, 11: 3  # 3 = Fall or Autumn
}

df_lightLevels_temp = df_lightLevels.copy()

df_lightLevels_temp["Day of week"] = df_lightLevels_temp["Date"].dt.dayofweek # 0 = Monday, 6 = Sunday
df_lightLevels_temp["Day of month"] = df_lightLevels_temp["Date"].dt.day # 1 to 31
df_lightLevels_temp["Day of year"] = df_lightLevels_temp["Date"].dt.dayofyear # 1 to 366
df_lightLevels_temp["Week of year"] = df_lightLevels_temp["Date"].dt.weekofyear # 1 to 52

df_lightLevels_temp["Month"] = df_lightLevels_temp["Date"].dt.month # 1 to 12
df_lightLevels_temp["Season"] = df_lightLevels_temp["Date"].dt.month.apply(lambda val: Seasons_dict[val]) # 0 to 3
df_lightLevels_temp["Quarter"] = df_lightLevels_temp["Date"].dt.quarter # 1 to 4
df_lightLevels_temp["Year"] = df_lightLevels_temp["Date"].dt.year # 

# **^^ So, we see time component of the datetime column does not contribute in anyway.**
''' THIS HAS BEEN ANALYZED IN THE IPYTHON NOTEBOOK FILE '''

### Let us see if we can find trends in `Light Score` variable and between time and `Light Score` variable.

# **^^ Looking at the Season, Week-of-year, Day-of-year plots, we observe that the collisions drastically reduce during the 
# months of Winter(0), Summer(2) i.e. when the migration of birds in not happens. 
# This is in line with the common knowledge that birds migrate in during Spring and away as Autumn/Fall approaches**

### ^^ looking at the trends, we cannot reliably impute the missing values under the `df_lightLevels['Light Score']`

''' THIS HAS BEEN ANALYZED IN THE IPYTHON NOTEBOOK FILE '''






# 9. We perform a left join between `df_chicagoCollisionData` and `df_lightLevels` on the column `Date` in the two dataframes.

df_chicagoCollisionData_LJOIN_lightLevels = df_chicagoCollisionData.merge(df_lightLevels, how='left', on='Date')

## same no. of rows in the resulting table as the left table means all the duplicates in the right table have been cleaned
''' THIS HAS BEEN ANALYZED IN THE IPYTHON NOTEBOOK FILE '''







# 10. Next, we take the `df_chicagoCollisionData_LJOIN_lightLevels` as the left table and `df_flightCall` as right table 
# and perform left join on the column names `Genus` and `Species`. 

### We chose Genus and Species becuase these two constitute a scientific name for each species/type of bird (Source: Paper, Wikipedia)

# gives final fully joined dataframe 
df_fullDataJoined = df_chicagoCollisionData_LJOIN_lightLevels.merge(df_flightCall, how='left', on=['Genus', 'Species'])

## again, same no. of rows in the resulting table as the left table means all the duplicates in the right table have been cleaned
''' THIS HAS BEEN ANALYZED IN THE IPYTHON NOTEBOOK FILE '''






# 11. After joining, we see that 89 rows are still missing information for columns `Family`, `Collisions`, `Flight Call`, `Habitat`, `Stratum`. 

# These missing values are seen because `df_flightCall` dataframe does not have these rows. 
# We lookup information about the **Genus** and **Species** together i.e. the scientific name, 
# and can find out what family a Genus-Species row belongs to, whether make **Flight Call**, 
# what their **Habitat** is and the **Stratum** they fly in. 


# a simple google search tells us that ammodramus genus belongs to Passerellidae family

# replace null values in the df_fullDataJoined['Family']
df_fullDataJoined["Family"].loc[df_fullDataJoined["Genus"] == "Ammodramus"] = "Passerellidae"

# next, we populate flight call, habitat, stratum based on the Genus name since we could not 
# find specific info about Ammodramus nelsoni, Ammodramus henslowii, Ammodramus leconteii
df_fullDataJoined["Flight Call"].loc[df_fullDataJoined["Genus"] == "Ammodramus"] = "yes"
df_fullDataJoined["Habitat"].loc[df_fullDataJoined["Genus"] == "Ammodramus"] = "open"
df_fullDataJoined["Stratum"].loc[df_fullDataJoined["Genus"] == "Ammodramus"] = "lower"

### the only null values are under `df_fullDataJoined['Collisions']` and `df_fullDataJoined['Light Score']`
### The 69784 - 69695 = 89 values under  `df_fullDataJoined['Collisions']` still remain.







# 12. The values under `Collisions` column are the same "number of rows" in `df_fullDataJoined` for 
# given `(Family, Genus, Species)` tuple. Therefore, we can just count the number of rows in `df_fullDataJoined` for 
# the tuple and fill in the NA values under `Collisions`.

# we find out the ones we need to do it for

df_missingCollisions = df_fullDataJoined[df_fullDataJoined["Collisions"].isnull()]

# So, we have to do it for `("Passerellidae", "Ammodramus", "nelsoni")`, 
# `("Passerellidae", "Ammodramus", "henslowii")` and `("Passerellidae", "Ammodramus", "leconteii")`

numCollisions_nelsoni = len(
    df_missingCollisions[
        (df_missingCollisions["Family"] == "Passerellidae") & \
        (df_missingCollisions['Genus'] == "Ammodramus") & \
        (df_missingCollisions['Species'] == "nelsoni")
    ]
)

numCollisions_henslowii = len(
    df_missingCollisions[
        (df_missingCollisions["Family"] == "Passerellidae") & \
        (df_missingCollisions['Genus'] == "Ammodramus") & \
        (df_missingCollisions['Species'] == "henslowii")
    ]
)

numCollisions_leconteii = len(
    df_missingCollisions[
        (df_missingCollisions["Family"] == "Passerellidae") & \
        (df_missingCollisions['Genus'] == "Ammodramus") & \
        (df_missingCollisions['Species'] == "leconteii")
    ]
)


# use these values to impute the collisions column in df_fullDataJoined
df_fullDataJoined.loc[
    (df_fullDataJoined["Family"] == "Passerellidae") & \
    (df_fullDataJoined["Genus"] == "Ammodramus") & \
    (df_fullDataJoined["Species"] == "nelsoni"), "Collisions"
] = numCollisions_nelsoni

df_fullDataJoined.loc[
    (df_fullDataJoined["Family"] == "Passerellidae") & \
    (df_fullDataJoined["Genus"] == "Ammodramus") & \
    (df_fullDataJoined["Species"] == "henslowii"), "Collisions"
] = numCollisions_henslowii

df_fullDataJoined.loc[
    (df_fullDataJoined["Family"] == "Passerellidae") & \
    (df_fullDataJoined["Genus"] == "Ammodramus") & \
    (df_fullDataJoined["Species"] == "leconteii"), "Collisions"
] = numCollisions_leconteii

# Checking the df_fullDataJoined again, we will see even the collisions column has been filled.
''' THIS HAS BEEN ANALYZED IN THE IPYTHON NOTEBOOK FILE '''








# 13. Finally, we perform a group by operation to group by the columns **`Family`, `Genus`, `Species`** 
# and aggregate values under other columns

df_summary = df_fullDataJoined.groupby(by=["Family", "Genus", "Species"], as_index=False).agg(
    common_locality = pd.NamedAgg(column="Locality", aggfunc=(lambda x:x.value_counts().index[0])), # The locality where this kind of birds commonly collided
    average_lightScore = pd.NamedAgg(column="Light Score", aggfunc="mean"), # the average light score for which these type of birds met with a collisions. 
    num_collisions = pd.NamedAgg(column="Collisions", aggfunc="first"), # The total count of collisions counted in McCormick Place and downtown Chicago that was record for these type of birds. 
    flight_call = pd.NamedAgg(column="Flight Call", aggfunc="first"), # Do these type of birds make nocturnal flight calls?
    habitat = pd.NamedAgg(column="Habitat", aggfunc="first"), # What is the habitat for these type of birds?
    stratum = pd.NamedAgg(column="Stratum", aggfunc="first") # How high do these type of birds fly?  
)

# change dtype to Int16
df_summary['num_collisions'] = df_summary['num_collisions'].astype('Int16')

# rename columns for better readability

df_summary.rename(columns = {
    "common_locality": "Common Locality",
    "average_lightScore": "Average Light Score",
    "num_collisions": "Number of Collisions",
    "flight_call": "Flight Call",
    "habitat": "Habitat",
    "stratum": "Stratum"
}, inplace=True)


# 14. Finally, we save the dataframe as a CSV file named **summary_table.csv**. 
# Along with it, we can also save `df_fullDataJoined` as **fullDataJoined_table.csv**.

df_summary.to_csv(os.path.join(outputDir, 'summary_table.csv'), index=False)
df_fullDataJoined.to_csv(os.path.join(outputDir, 'fullDataJoined_table.csv'), index=False)

print("Successfully ran the script!")











