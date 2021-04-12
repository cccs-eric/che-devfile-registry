import argparse
import os
import sys
from jinja2 import Template, Environment, FileSystemLoader

def extractRepository(line) -> dict:
    registry, namespace, image = line.split('/', 2)
    imageName, imageVersion = image.split(':')
    keys = ['registry', 'namespace', 'repositoryName', 'tagName']
    values = [registry, namespace, imageName, imageVersion]
    return dict(zip(keys, values))

def initArgparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]",
        description="Creates a PortKey configuration from an Eclipse Che devfile registry external_images.txt file."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('extImages', nargs='*')
    return parser

def main() -> None:
    parser = initArgparse()
    args = parser.parse_args()
    if not args.extImages:
        parser.print_usage()
        sys.exit(1)
    print("Start of portkey config creation")
    templateLoader = FileSystemLoader(searchpath=os.path.join(os.path.dirname(__file__), "./templates/"))
    templateEnv = Environment(loader=templateLoader)
    template = templateEnv.get_template("portkey_template.j2")
    images = []
    with open("/home/erladou/git/cccs/che-devfile-registry/external_images.txt", "r") as extImgFile:
        for line in extImgFile:
            try:
                images.append(extractRepository(line.strip()))
            except ValueError:
                print("Skipping line ", line.strip())
                continue
    quayImages = { 'registry': 'quay.io'}
    quayImages['repositories'] = [img for img in images if img['registry'] == 'quay.io']
    crImages = [img for img in images if img['registry'] == 'cranalyticalplatform.azurecr.io']
    
    print(template.render(quayImages))
    #print(quayImages)

if __name__ == "__main__":
    main()