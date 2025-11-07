import arcpy, sys, os, json, getopt, traceback
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader 

#this will load a python toolbox and make all functions available on a Python module
spec = spec_from_loader("AssetPackageToolbox", SourceFileLoader("AssetPackageToolbox", os.path.join(os.path.dirname(os.path.realpath(__file__)),"asset-package-deployment.pyt")))
AssetPackageToolbox = module_from_spec(spec)
spec.loader.exec_module(AssetPackageToolbox)

def readconfig(filelocation):
    with open(filelocation) as f:
        config = json.load(f)
    return config
    
#wrapper script which translates the command line parameters to the parameters for the python toolbox functions
def main(argv):
    in_folder = None
    out_workdir = None
    out_gdb = None
    full_export = None
    in_gdb = None
    out_folder = None
    config_file = None
    out_sde = None
    portalurl = None
    username = os.getenv('USER')
    password = os.getenv('PASSWORD')
    operation = 'ExportAssetPackage'
    operations = ['ExportAssetPackage', 'ImportAssetPackage','DeployAssetPackage']
    try:
        opts, args = getopt.getopt(argv,"o:",[
            'in_folder=', 
            'out_workdir=', 
            'out_gdb=',
            'full_export=',
            'in_gdb=',
            'out_folder=',
            'out_sde=',
            'config_file=',
            'portalurl=',
            'user=',
            'password='
            ]
        )
        for opt, arg in opts:
            if opt == '-o':
                if arg in operations:
                    operation = arg
                else:
                    raise Exception('-o {} not found in allowed operations: {}'.format(arg, operations))
            if opt == '--in_folder':
                in_folder = arg
            if opt == '--out_workdir':
                out_workdir = arg
            if opt == '--out_gdb':
                out_gdb = arg
            if opt == '--full_export':
                full_export = arg
            if opt == '--in_gdb':
                in_gdb = arg
            if opt == '--out_folder':
                out_folder = arg
            if opt == '--config_file':
                config_file = arg
            if opt == '--portalurl':
                portalurl = arg
            if opt == '--out_sde':
                out_sde = arg
            if opt == '--user':
                username = arg
            if opt == '--password':
                password = arg
        if operation == 'ImportAssetPackage':
            print('ImportAssetPackage')
            importAssetPackage = AssetPackageToolbox.ImportAssetPackage()
            params = importAssetPackage.getParameterInfo()
            print('in_folder:' + in_folder)
            params[0].value = in_folder
            print('out_workdir:' + out_workdir)
            params[1].value = out_workdir
            print('out_gdb:' + out_gdb)
            params[2].value = out_gdb
            importAssetPackage.execute(params, None)
        elif operation == 'ExportAssetPackage':
            print('ExportAssetPackage')
            exportAssetPackage = AssetPackageToolbox.ExportAssetPackage()
            params = exportAssetPackage.getParameterInfo()
            params[0].value = full_export
            print('full_export:' + full_export)
            params[1].value = in_gdb
            print('in_gdb:' + in_gdb)
            params[2].value = out_folder
            print('out_folder:' + out_folder)
            exportAssetPackage.execute(params, None)
        elif operation == 'DeployAssetPackage':
            print('DeployAssetPackage')
            config = readconfig(config_file)
            deployAssetPackage = AssetPackageToolbox.DeployAssetPackage()
            params = deployAssetPackage.getParameterInfo()

            params[0].value = in_gdb
            print('Asset package geodatabase:' + in_gdb)

            params[1].value = config['serviceterritory']
            print('Service Territory Feature Class:' + config['serviceterritory'])

            if out_folder is not None:
                params[2].value = out_folder
                print('Output Folder File Geodatabase:' + out_folder)

            if out_gdb is not None:
                params[3].value = out_gdb
                print('Output Name File Geodatabase:' + out_gdb)

            if out_sde is not None:
                params[4].value = out_sde
                print('Output SDE file:' + out_sde)

            params[5].value = config['datasetname']
            print('Dataset Name:' + config['datasetname'])
            
            params[6].value = config['utilitynetworkname']
            print('Utility network name:' + config['utilitynetworkname'])

            params[7].value = config['domainnetworks']
            print('Domain networks:' + config['domainnetworks'])

            params[8].value = config['loaddata']
            print('Load Data:' + config['loaddata'])

            params[9].value = config['postprocess']
            print('Post process:' + config['postprocess'])
            
            params[10].value = config['configurations']
            print('Configurations:' + config['configurations'])
            
            params[11].value = config['renamefield']
            print('Rename Field:' + config['renamefield'])
            
            if portalurl is not None: 
                params[12].value = portalurl
                print('PortalUrl:' + portalurl)
            
            if username is not None: 
                params[13].value = username
                print('Portal Username:' + username)
            
            if password is not None: 
                params[14].value = password
                print('Portal password is not None')

            
            params[15].value = config['version_fcs']
            print('Featureclasses to version:' + ','.join(config['version_fcs']))

            result = deployAssetPackage.execute(params, None)
            if not result:
                sys.exit(1)
        else:
            print("i dont get it")
    except getopt.GetoptError as e:
        print(str(e))
        sys.exit(2)
    except Exception as e:
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])