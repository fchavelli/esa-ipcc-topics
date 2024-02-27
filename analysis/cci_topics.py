import json
from openpyxl import Workbook

CMIP6 = {
    'Systematic Biases': {
        'Clouds/Circulation': ['CFMIP', 'DynVarMIP'],
        'Regional phenomena': ['GMMIP', 'HighResMIP', 'PAMIP'],
        'Ocean/Land/Ice': ['OMIP', 'FAFMIP', 'LS3MIP', 'SIMIP', 'ISMIP6']
    },
    'Response to Forcing': {
        'Paleo': ['PMIP'],
        'Characterizing forcing': ['RFMIP', 'DAMIP', 'VolMIP'],
        'Chemistry/Aerosols': ['AerChemMIP'],
        'Carbon cycle': ['C4MIP']
    },
    'Variability, Predictability, Future Scenarios': {
        'Land use': ['LUMIP'],
        'Geo-engineering': ['CDRMIP', 'GeoMIP'],
        'Decadal prediction': ['DCPP'],
        'Scenarios': ['ScenarioMIP'],
        'Impacts': ['CORDEX', 'VIACS AB']
    }
}

ECV = {
    "atmosphere": {
        "surface" : [
            "precipitation",
            "pressure",
            "radiation budget",
            "atmosphere temperature",
            "water vapour",
            "lightning",
            "upper-air temperature",
            "cloud"
        ],
        "atmospheric composition" : [
            "aerosol",
            "carbon dioxide",
            "methane",
            "ozone",
            "other greenhouse gases",
            "precursors for aerosols",
            "precursors for ozone"
        ],
        "wind" : [
            "wind speed",
            "wind direction"
        ]
    },
    "land": {
        "hydrosphere": [
            "groundwater",
            "lake",
            "river discharge",
            "terrestrial water storage"
        ],
        "cryosphere": [
            "glacier",
            "ice sheet",
            "ice shelf",
            "permafrost",
            "snow"
        ],
        "biosphere": [
            "above-ground biomass",
            "albedo",
            "evaporation from land",
            "fire",
            "FAPAR",
            "land cover",
            "land surface temperature",
            "leaf area index",
            "soil carbon",
            "soil moisture"
        ],
        "anthroposphere": [
            "anthropogenic GHG fluxes",
            "anthropogenic water use"
        ]
    },
    "ocean": {
        "physical": [
            "ocean surface heat flux",
            "sea ice",
            "sea level",
            "sea state",
            "sea surface current",
            "sea surface salinity",
            "sea surface stress",
            "sea surface temperature",
            "subsurface current",
            "subsurface salinity",
            "subsurface temperature"
        ],
        "biogeochemical": [
            "inorganic carbon",
            "nitrous oxide",
            "nutrient",
            "ocean colour",
            "oxygen",
            "transient tracer"
        ],
        "biological/ecosystems": [
            "marine habitat",
            "plankton"
        ]
    }
}

ecv_aliases = {"precipitation" : [],
               "pressure" : [],
               "radiation budget" : [],
               "atmosphere temperature" : [],
               "wind speed" : [],
               "wind direction" : [],
               "lightning" : [],
               "upper-air temperature" : [],
               "water vapour" : ["water vapor"],
               "cloud" : [],
               "aerosol" : [],
               "carbon dioxide" : ["CO2"],
               "methane" : ["CH4"],
               "ozone" : ["O3"],
               "other greenhouse gases" : ["other greenhouse gas", "other GHG"],
               "precursors for aerosols" : ["precursors for aerosol", "precursor for aerosol", "precursor of aerosol", "precursors of aerosol"],
               "precursors for ozone" : ["precursor for ozone", "precursors of ozone", "precursor of ozone"],
               "groundwater" : [],
               "lake" : [],
               "river discharge" : ["rivers discharge"],
               "terrestrial water storage" : [],
               "glacier" : [],
               "ice sheet" : [],
               "ice shelf" : ["ice shelves"],
               "permafrost" : [],
               "snow" : [],
               "above-ground biomass" : ["above ground biomass"],
               "albedo" : [],
               "evaporation from land" : ["evaporations from land"],
               "fire" : [],
               "FAPAR" : ["fraction of absorbed photosynthetically active radiation"],
               "land cover" : [],
               "land surface temperature" : ["lands surface temperature"],
               "leaf area index" : [],
               "soil carbon" : [],
               "soil moisture" : [],
               "anthropogenic GHG fluxes" : ["anthropogenic greenhouse gases fluxes", "anthropogenic greenhouse gas flux", "anthropogenic greenhouse gases flux", "anthropogenic greenhouse gas fluxes", "anthropogenic GHGs fluxes", "anthropogenic GHG flux", "anthropogenic GHGs flux"],
               "anthropogenic water use" : [],
               "ocean surface heat flux" : ["ocean surface heat fluxes"],
               "sea ice" : [],
               "sea level" : ["seas level"],
               "sea state" : ["seas state"],
               "sea surface current" : ["seas surface current", "seas surface currents"],
               "sea surface salinity" : ["seas surface salinity"],
               "sea surface stress" : ["sea surface stresses", "seas surface stress"],
               "sea surface temperature" : ["seas surface temperature"],
               "subsurface current" : [],
               "subsurface salinity" : ["subsurfaces salinity"],
               "subsurface temperature" : ["subsurfaces temperature"],
               "inorganic carbon" : [],
               "nitrous oxide" : ["N2O"],
               "nutrient" : [],
               "ocean colour" : ["oceans colour"],
               "oxygen" : [" O2"], # space to avoid 'o2' in 'co2'
               "transient tracer" : [],
               "marine habitat" : [],
               "plankton" : []
}

projects = ["Aerosol", "Biomass", "Climate Modelling User Group (CMUG)", "Cloud", "Fire", "Greenhouse Gases (GHGs)", "Glaciers", "High Resolution Land Cover", "Ice Sheets (Antarctic)", "Ice Sheets (Greenland)", "Lakes", "Land Cover", "Land Surface Temperature", "Ocean Colour", "Ozone", "Permafrost", "Precursors for aerosols and ozone", "RECCAP-2", "River Discharge", "Sea Ice", "Sea Level", "Sea Level Budget Closure", "Sea State", "Sea Surface Salinity", "Sea Surface Temperature", "Snow", "Soil Moisture", "Vegetation Parameters", "Water Vapour"]

with open("./data/cci/ecv_aliases.json", "w") as f:
    json.dump(ecv_aliases, f)

with open("./data/cci/ecv_classification.json", "w") as f:
    json.dump(ECV, f)

with open("./data/cci/projects.json", "w") as f:
    json.dump(projects, f)


def save_dict_to_excel(data_dict, file_name='output.xlsx'):
    # Create a new Excel workbook and grab the active worksheet
    wb = Workbook()
    ws = wb.active
    
    # Iterate over the dictionary items
    for row_index, (key, values) in enumerate(data_dict.items(), start=1):
        # Write the key in the first column
        ws.cell(row=row_index, column=1, value=key)
        
        # Write the values in the next columns
        for col_index, value in enumerate(values, start=2):
            ws.cell(row=row_index, column=col_index, value=value)
    
    # Save the workbook to the specified file name
    wb.save(file_name)
    print(f"Dictionary saved to '{file_name}' successfully.")

# Save the dictionary to an Excel file
save_dict_to_excel(ecv_aliases, './temp/ecv_aliases.xlsx')
