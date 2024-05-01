import pandas as pd
import numpy as np

def removeCOH(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Get column names containing 'COH' or 'Unnamed: 122'
    coh_columns = [col for col in df.columns if 'COH' in col or col == 'Unnamed: 122']

    # Drop columns containing 'COH' or 'Unnamed: 122'
    df.drop(columns=coh_columns, inplace=True)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)



def process_columns(csv_file):
    # Iterate over each column in the DataFrame
    df = pd.read_csv(csv_file)
    for col in df.columns:
        # Check if the column contains 'AB'
        if 'AB' in col:
            # Check if a certain string is in the column
            if 'delta' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = np.sqrt((df[col].abs() * 3))
            elif 'theta' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = np.sqrt((df[col].abs() * 4))
            elif 'alpha' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = np.sqrt((df[col].abs() * 4))
            elif 'beta' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = np.sqrt((df[col].abs() * 13))
            elif 'highbeta' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = np.sqrt((df[col].abs() * 5))
            elif 'gamma' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = np.sqrt((df[col].abs() * 10))
    df.to_csv(csv_file, index=False)

def get_attenuated_vals(csv_file):
    df = pd.read_csv(csv_file)
    #print('here')
    vals = []
    for col in df.columns:
        #epsilons, rhos = scalp, hard bone, soft bone, dura
        c = col.split('.')
        if 'AB' not in c[0]:
            continue
        if 'delta' in c:
            epsilons = [1140,99300,1.88e7,9.51e5]
            rhos = [5000,50,14.14,2]
        elif 'theta' in c:
            epsilons = [1140,78700,1.47e7,7.45e5]
            rhos = [5000,50,13.71,2]
        elif 'alpha' in c:
            epsilons = [1140,55200,1e7,5.10e5]
            rhos = [5000,50,13.22,2]
        elif 'beta' in c:
            epsilons = [1140,27700,4.54e6,2.36e5]
            rhos = [5000,50,12.72,2]
        elif 'highbeta' in c:
            epsilons = [1140,16800,2.36e6,1.27e5]
            rhos = [5000,50,12.53,2]
        elif 'gamma' in c:
            epsilons = [1140,12600,1.53e6,8.55e4]
            rhos = [5000,49.75,12.45,2]

        #get distances based on sensor location c[-1]
        #d = scalp, hard bone (not constant), soft bone (not constant), dura
        #0.2 hard, 0.8 soft, d_scalp = 5.8 mm, d_dura = 0.322 mm
        #all vals in mm for d
        d = [5.8,0,0,0.322]
        if 'FP' in c[-1]:
            d[1] = 0.2*5.34
            d[2] = 0.8*5.34
        elif 'F' in c[-1]:
            d[1] = 0.2*6.63
            d[2] =0.8*6.63
        elif 'T' in c[-1]:
            d[1] = 0.2*1.96
            d[2] =0.8*1.96
        elif 'C' in c[-1]:
            d[1] = 0.2*4.71
            d[2] =0.8*4.71
        elif 'P' in c[-1]:
            d[1] = 0.2*5.35
            d[2] =0.8*5.35
        elif 'O' in c[-1]:
            d[1] = 0.2*8.20
            d[2] =0.8*8.20
        d = [num * 1e-3 for num in d]
        vals.append([epsilons, rhos, d])
    return vals
        
def get_excel_dimensions(excel_file):
    df = pd.read_csv(excel_file)
    num_rows, num_cols = df.shape
    return num_rows, num_cols

def attenuate_values(vals, csv_file):
    df = pd.read_csv(csv_file)
    i = 0
    current = 80e-6
    area = (4e-3 ** 2) * np.pi
    for col in df.columns:
        c = col.split('.')
        if 'AB' not in c[0]:
            continue
        #unpack vals
        e = vals[i][0]
        p = vals[i][1]
        d = vals[i][2]

        #compute impedance
        impedance = 0
        
        for j in range(4):
            impedance += parallel(p[j]*d[j]*area, (area*e[j])/d[j])
        
        #print(impedance)
        df[col] = df[col].mul(1e-6) - current*impedance
        df[col] = df[col].mul(1e6)
        i += 1
    #print(i)
    df.to_csv('data_edited_edited.csv', index=False)

def parallel(a,b):
    return (a * b) / (a + b)
        

def process_columns_to_PSD(csv_file):
    # Iterate over each column in the DataFrame
    df = pd.read_csv(csv_file)
    for col in df.columns:
        # Check if the column contains 'AB'
        if 'AB' in col:
            # Check if a certain string is in the column
            if 'delta' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = (np.square(df[col]) / 3).abs()
            elif 'theta' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = (np.square(df[col]) / 4).abs()
            elif 'alpha' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = (np.square(df[col]) / 4).abs()
            elif 'beta' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = (np.square(df[col]) / 13).abs()
            elif 'highbeta' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = (np.square(df[col]) / 5).abs()
            elif 'gamma' in col:
                # Apply operations specific to the column with 'certain_string'
                df[col] = (np.square(df[col]) / 10).abs()
    df.to_csv('data_edited_final.csv', index=False)    


# Step 1: Remove COH from dataset
#removeCOH('data_edited.csv')

#Step 2: attain voltage in microvolts
#process_columns('data_edited.csv')

#Step 3: Get appropriate attenuated vals for each column, verify
#vals = get_attenuated_vals('data_edited.csv')
#--works
#print(get_excel_dimensions('data_edited.csv'))
#print(len(vals))
#print(vals[2])

#Step 4: Change all values accordingly and revert to original PSD format
#attenuate_values(vals, 'data_edited.csv')
#process_columns_to_PSD('data_edited_edited.csv')

removeCOH('data.csv')


