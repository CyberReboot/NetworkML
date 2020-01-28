import inspect
import os
import sys

# TODO move print statements to logging

class Featurizer():

    def import_class(self, path, classes):
        """
        Imports classs from an external directory at runtime. Imported functions will be added
        to classes
        :param path: path where the modules reside
        :param classes: existing class instances
        :return list of newly add class instances
        """
        # make sure path exists
        if os.path.isdir(path) is False:
            print("Error: path {} does not exist".format(path))
            return classes

        #add the path to the PYTHONPATH
        sys.path.append(path)

        #acquire list of files in the path
        mod_list = os.listdir(path)

        for f in mod_list:

            #continue if it is not a python file
            if f[-3:] != '.py':
                continue

            #get module name by removing extension
            mod_name = os.path.basename(f)[:-3]

            #import the module
            module = __import__(mod_name, locals(), globals())
            for name,cls in inspect.getmembers(module):
                if inspect.isclass(cls) and name != "Features":
                    instance = cls()
                    #append an instance of the class to classes
                    classes.append((instance, name))
                    print(f'Importing class: {name}')

        return classes

    def main(self, feature_choices, rows, features_path):
        results = []
        functions = []
        groups = ('default')
        classes = []
        classes = self.import_class(features_path, classes)

        if 'functions' in feature_choices:
            functions = feature_choices['functions']
        if 'groups' in feature_choices:
            groups = feature_choices['groups']

        feature_rows = []
        run_methods = []
        for f in classes:
            if groups:
                methods = filter(lambda funcname: funcname.startswith(groups), dir(f[0]))
                for method in methods:
                    print(f'Running method: {f[1]}/{method}')
                    feature_row = f[0].run_func(method, rows)
                    feature_rows.append(feature_row)
                    run_methods.append((f[1], method))

        # run remaining extras
        for function in functions:
            if function not in run_methods:
                for f in classes:
                    if f[1] == function[0]:
                        print(f'Running method: {f[1]}/{function[1]}')
                        feature_row = f[0].run_func(function[1], rows)
                        feature_rows.append(feature_row)
        return feature_rows
