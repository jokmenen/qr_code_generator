import argparse
import qrcode
import qrcode.image.svg
from pathlib import Path
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

OUTPUT_FOLDER = Path() / 'output'

OUTPUT_FOLDER.mkdir()

def generate_qr_code(data, filename=None):
    factory = qrcode.image.svg.SvgPathImage
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(image_factory=factory, fill_color="black", back_color="white")
    i = 0
    if filename:
            save_path = Path(filename)
    else:
        while True:
            save_path = Path(f'qr_code_{i}.svg')
            if not save_path.is_file():
                break
            i += 1
    img.save(OUTPUT_FOLDER / save_path)

def main():
    parser = argparse.ArgumentParser(description="Generate a QR code from a provided data string. Usually a URL")
    parser.add_argument('--data', '-d', type=str, required=False, help='The data to encode in the QR code')
    parser.add_argument('--csv', '-c', type=str, required=False, help="Use this if you want to parse a csv. Assumes ; as seperator! Use the column names 'target' (for the link you're trying to process), and 'filename' for the resulting name of the qr. " )
    args = parser.parse_args()

    if args.csv:
        #use pandas to load csv. 
        items_df = pd.read_csv(args.csv, sep=';')

        if not set(['target','filename']).issubset(items_df.columns):
            print('ERROR: target and filename columns not found. Make sure to include them and format your csv with ; as seperator.')
        
        print('found items:')
        print(items_df)
        for index, row in items_df.iterrows():
            generate_qr_code(row['target'], filename=row['filename'])

        print('Done!')
         
    else:
        generate_qr_code(args.data)

if __name__ == "__main__":
    main()
