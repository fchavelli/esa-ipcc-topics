import json
import pickle
import logging

# Projects not in any ECV instance:
    # Vegetation Parameters
    # RECCAP-2
    # Ice Sheets (Antarctic)
    # High Resolution Land Cover
    # Climate Modelling User Group (CMUG)
    # Ice Sheets (Greenland)
    # Precursors for aerosols and ozone
    # Sea Level Budget Closure

# Assumptions
    # Project 'ICe Sheets' created to handle 'Ice Sheets (Antarctic)' and 'Ice Sheets (Greenland)'
    # ECV 'above-ground biomass' is part of 'Biomass' project

# Import ecv instances:
    # ecvs_file_path = './data/cci/ecvs.pkl'
    # with open(ecvs_file_path, 'rb') as file:
    #     ecv_instances = pickle.load(file)

ecvs_file_path = './data/cci/ecvs.pkl'

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class ECV:
    def __init__(self, name, search_term, display_name, category, subcategory, aliases, project):
        self.name = name
        self.search_term = search_term
        self.display_name = display_name
        self.category = category
        self.subcategory = subcategory
        self.aliases = aliases
        self.project = project

    def display(self):
        """Displays information about the ECV instance."""
        info = f"Name: {self.name}, Category: {self.category}, Subcategory: {self.subcategory}, Project: {self.project}, Display: {self.display_name}, Search Term: {self.search_term}, Aliases: {self.aliases}"
        print(info)

def create_ecv_instances(ecv_structure, ecv_aliases, projects):
    logging.info("Starting the ECV instances creation process")
    ecv_instances = []

    for category, subcategories in ecv_structure.items():
        for subcategory, search_terms in subcategories.items():
            for search_term in search_terms:
                name = search_term.replace(' ', '_')
                display_name = search_term.capitalize()
                aliases = ecv_aliases.get(search_term, [])
                project = next((proj for proj in projects if (proj.lower() == search_term.lower() or proj.lower() == search_term.lower()[:-1])), None)
                # Exceptions:
                if search_term == 'above-ground biomass':
                    project = 'Biomass'
                if search_term in ['carbon_dioxide', 'methane', 'other_greenhouse_gases']:
                    project = 'Greenhouse Gases (GHGs)'
                ecv_instance = ECV(name, search_term, display_name, category, subcategory, aliases, project)
                ecv_instances.append(ecv_instance)

                logging.info(f"Name: {name}, Category: {category}, Subcategory: {subcategory}, Project: {project}")
                #logging.info(f"Display: {display_name}, Search term: {search_term}, Aliases: {aliases}")
    
    logging.info("Finished creating ECV instances")
    return ecv_instances

with open('./data/cci/ecv_aliases.json', 'r') as f:
    ECV_ALIASES = json.load(f)
with open('./data/cci/ecv_classification.json', 'r') as f:
    ECV_TREE = json.load(f)
with open('./data/cci/projects.json', 'r') as f:
    PROJECTS = json.load(f)

# Create ECV instances
ecv_instances = create_ecv_instances(ECV_TREE, ECV_ALIASES, PROJECTS)

# Saving instances to a file for easy import
with open(ecvs_file_path, 'wb') as file:
    pickle.dump(ecv_instances, file)

logging.info("ECV instances have been saved to ecvs.pkl")
