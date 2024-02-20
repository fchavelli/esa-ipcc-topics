import json

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
            "earth radiation budget",
            "lightning",
            "upper-air temperature",
            "clouds"
        ],
        "atmospheric composition" : [
            "aerosols",
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
            "lakes",
            "river discharge",
            "terrestrial water storage"
        ],
        "cryosphere": [
            "glaciers",
            "ice sheets",
            "ice shelves",
            "permafrost",
            "snow"
        ],
        "biosphere": [
            "above-ground biomass",
            "albedo",
            "evaporation from land",
            "fire",
            "FADAR",
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
            "sea surface currents",
            "sea surface salinity",
            "sea surface stress",
            "sea surface temperature",
            "subsurface currents",
            "subsurface salinity",
            "subsurface temperature"
        ],
        "biogeochemical": [
            "inorganic carbon",
            "nitrous oxide",
            "nutrients",
            "ocean colour",
            "oxygen",
            "transient tracers"
        ],
        "biological/ecosystems": [
            "marine habitats",
            "plankton"
        ]
    }
}

ecv_aliases = {"precipitation" : ["precipitations"],
               "pressure" : ["pressures"],
               "radiation budget" : ["radiation budgets"],
               "atmosphere temperature" : ["atmosphere temperatures"],
               "wind speed" : ["wind speeds"],
               "wind direction" : ["wind directions"],
               "earth radiation budget" : ["earth radiation budgets"],
               "lightning" : ["lightnings"],
               "upper-air temperature" : ["upper-air temperatures"],
               "water vapour" : ["water vapors", "water vapor", "water vapours"],
               "clouds" : ["cloud"],
               "aerosols" : ["aerosol"],
               "carbon dioxide" : ["carbon dioxides", "CO2"],
               "methane" : ["methanes", "CH4"],
               "ozone" : ["ozones", "O3"],
               "other greenhouse gases" : ["other greenhouse gas", "other GHG", "other GHGs"],
               "precursors for aerosols" : ["precursor for aerosols", "precursors for aerosol", "precursor for aerosol", "precursor of aerosols", "precursor of aerosol", "precursors of aerosols", "precursors of aerosol"],
               "precursors for ozone" : ["precursor for ozone", "precursors of ozone", "precursor of ozone"],
               "groundwater" : ["groundwaters"],
               "lakes" : ["lake"],
               "river discharge" : ["river discharges", "rivers discharge", "rivers discharges"],
               "terrestrial water storage" : ["terrestrial water storages"],
               "glaciers" : ["glacier"],
               "ice sheets" : ["ice sheet"],
               "ice shelves" : ["ice shelf"],
               "permafrost" : ["permafrosts"],
               "snow" : [],
               "above-ground biomass" : ["above ground biomass"],
               "albedo" : ["albedos"],
               "evaporation from land" : ["evaporation from lands", "evaporations from land", "evaporations from lands"],
               "fire" : ["fires"],
               "FADAR" : ["fraction of absorbed photosynthetically active radiation", "fraction of absorbed photosynthetically active radiations", "FAPAR"],
               "land cover" : [],
               "land surface temperature" : ["land surface temperatures", "land surfaces temperature", "land surfaces temperatures"],
               "leaf area index" : ["leaf areas indexes"],
               "soil carbon" : [],
               "soil moisture" : [],
               "anthropogenic GHG fluxes" : ["anthropogenic greenhouse gases fluxes", "anthropogenic greenhouse gas flux", "anthropogenic greenhouse gases flux", "anthropogenic greenhouse gas fluxes", "anthropogenic GHGs fluxes", "anthropogenic GHG flux", "anthropogenic GHGs flux"],
               "anthropogenic water use" : [],
               "ocean surface heat flux" : ["ocean surface heat fluxes"],
               "sea ice" : ["sea ices"],
               "sea level" : ["sea levels", "seas level", "seas levels"],
               "sea state" : ["sea states", "seas state", "seas states"],
               "sea surface currents" : ["sea surface current", "seas surfaces current", "seas surface currents", "seas surfaces currents"],
               "sea surface salinity" : ["sea surface salinities", "seas surfaces salinity", "sea surfaces salinity", "seas surfaces salinities"],
               "sea surface stress" : ["sea surface stresses", "sea surfaces stress", "seas surfaces stresses", "seas surface stress", "seas surfaces stress"],
               "sea surface temperature" : ["sea surface temperatures", "sea surfaces temperature", "sea surfaces temperatures", "seas surface temperatures", "seas surfaces temperature", "seas surfaces temperatures"],
               "subsurface currents" : ["subsurface current", "subsurfaces current", "subsurfaces currents"],
               "subsurface salinity" : ["subsurface salinities", "subsurfaces salinity", "subsurfaces salinities"],
               "subsurface temperature" : ["subsurface temperatures", "subsurfaces temperature", "subsurfaces temperatures"],
               "inorganic carbon" : ["inorganic carbons"],
               "nitrous oxide" : ["nitrous oxides", "N2O"],
               "nutrients" : ["nutrient"],
               "ocean colour" : ["ocean colours", "oceans colour", "oceans colours"],
               "oxygen" : ["oxygens", " O2"], # space to avoid 'o2' in 'co2'
               "transient tracers" : ["transient tracer", "transients tracer", "transients tracers"],
               "marine habitats" : ["marine habitat"],
               "plankton" : ["planktons"]
}

projects = ["Aerosol", "Biomass", "Climate Modelling User Group (CMUG)", "Cloud", "Fire", "Greenhouse Gases (GHGs)", "Glaciers", "High Resolution Land Cover", "Ice Sheets (Antarctic)", "Ice Sheets (Greenland)", "Lakes", "Land Cover", "Land Surface Temperature", "Ocean Colour", "Ozone", "Permafrost", "Precursors for aerosols and ozone", "RECCAP-2", "River Discharge", "Sea Ice", "Sea Level", "Sea Level Budget Closure", "Sea State", "Sea Surface Salinity", "Sea Surface Temperature", "Snow", "Soil Moisture", "Vegetation Parameters", "Water Vapour"]

with open("./data/cci/ecv_aliases.json", "w") as f:
    json.dump(ecv_aliases, f)

with open("./data/cci/ecv_classification.json", "w") as f:
    json.dump(ECV, f)

with open("./data/cci/projects.json", "w") as f:
    json.dump(projects, f)