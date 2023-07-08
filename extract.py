
import pyexiv2
import glob
import csv
import argparse
import sys

def parseGPS(val):
    # val is a list degrees, minutes, seconds of rational/fractional values
    ret = float(val[0])
    ret += float(val[1]) / 60
    ret += float(val[2]) / 60 / 60  

    return ret


def main(args):
    o = sys.stdout

    if not args.output is None:
        o = open(args.output, 'w')

    writer = csv.DictWriter(o, fieldnames=[
        'filename',
        'lat',
        'long'
    ])

    writer.writeheader()

    for p in glob.glob(args.pattern):
        print('reading file: {}'.format(p))
        metadata = pyexiv2.ImageMetadata(p)

        metadata.read()

        for k in metadata:
            print('{}: {}'.format(k, metadata[k]))

        writer.writerow({
            'filename': p,
            'lat': parseGPS(metadata['Exif.GPSInfo.GPSLatitude'].value),
            'long': -parseGPS(metadata['Exif.GPSInfo.GPSLongitude'].value)
        })

    if args.output is None:
        o.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", help="glob of image paths")
    parser.add_argument("--output", "-o", help="output CSV file")
    main(parser.parse_args())