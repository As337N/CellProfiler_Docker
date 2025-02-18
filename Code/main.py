import utils as ut
import sys

path_images = sys.argv[1]
path_savingCSV = sys.argv[2]
nameCSV = sys.argv[3]
channel_prefix = bool(int(sys.argv[4])) 

if __name__ == "__main__":

    channels_dict = {1:"Mito", 2:"AGP", 4:"RNA", 5:"ER", 6:"DNA"}
    pattern=r"^\d(?P<Column>\d{2})\d(?P<Row>\d{2})-(?P<Field>\d)-\d{4}(?P<Plane>\d{2})\d{2}(?P<Channel>\d).tif"

    metadata_constructor = ut.GenerateCPcsv(path_imagesFiles=path_images,
                                            path_savingCSV=path_savingCSV,
                                            channels_dict=channels_dict,
                                            pattern=pattern,
                                            name_CSV=nameCSV,
                                            with_illum=False,
                                            channel_prefix=channel_prefix)

    df = metadata_constructor.process_metadata()