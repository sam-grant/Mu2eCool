import pandas as pd

particleDict = {
    2212: 'proton',
    211: 'pi+',
    -211: 'pi-',
    -13: 'mu+',
    13: 'mu-'
    # Add more particle entries as needed
    }

def FilterParticles(df, particle): 

    # Filter particles
    if particle in particleDict.values():

        print("Hello, I'm filtering ",particle)
        PDGid = list(particleDict.keys())[list(particleDict.values()).index(particle)]
        return df[df['PDGid'] == PDGid]

    elif particle=="no_proton":
        return df[df['PDGid'] != 2212]

    elif particle=="pi-_and_mu-":
        return df[(df['PDGid'] == -211) | (df['PDGid'] == 13)]

    elif particle=="pi+-":

        print("Hello, I'm filtering ",particle)

        return df[(df['PDGid'] == 211) | (df['PDGid'] == -211)]

    elif particle=="mu+-":

        return df[(df['PDGid'] == -13) | (df['PDGid'] == 13)]

    else: 
        return df


# Create a dictionary with data
data = {
    'PDGid': [211, -211, -211, 211] 
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

print(df)

df_pi_plus = FilterParticles(df, "pi+")
df_pi_minus = FilterParticles(df, "pi-")
df_pi_plusMinus = FilterParticles(df, "pi+-")

print("pi_plus:\n:", df_pi_plus)
print("pi_minus:\n:", df_pi_minus)
print("pi_plusMinus:\n:", df_pi_plusMinus)
