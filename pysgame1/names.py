from pysgame1.util import resource_path

def load_names(filename):
    """Loads a name file and returns it as a list of names"""
	
    names = file(resource_path(filename)).read().split('\n')
    names = [name.strip() for name in names]
    names = [name for name in names if name]
    return names

female_names = load_names("data/female_names.txt")
male_names = load_names("data/male_names.txt")
surnames = load_names("data/surnames.txt")
