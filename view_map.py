

community = "WEST ENGLEWOOD" # HERE IT HAS TO BE LINKED WITH THE FORM
community_crimes = located_crimes[located_crimes['community']== community]
community_boundaries = commu_df[commu_df['community']== community]

base = community_boundaries.plot(color = "white")
community_crimes.plot(ax = base)
