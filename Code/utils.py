import pandas as pd
import os
import re

def get_well(col, row):
  col_corr = chr(64 + int(col))
  return f"{col_corr}{row}"

class GenerateCPcsv:
    def __init__(self, path_imagesFiles, path_savingCSV, channels_dict, pattern, name_CSV, with_illum=True, path_illumFiles=None, channel_prefix=True):
        self.path_imagesFiles = path_imagesFiles
        self.path_savingCSV = path_savingCSV
        self.channels_dict = channels_dict
        self.pattern = pattern
        self.name_CSV = name_CSV
        self.with_illum = with_illum
        self.channel_prefix = channel_prefix

        self.metadata_prefix = "Metadata"
        self.image_prefix = "Image"
        self.illum_prefix = "Illum"

        self.images = os.listdir(self.path_imagesFiles)
        #print(f"path images: {self.path_imagesFiles}")
        #print(f"images: {self.images}")

        if self.with_illum:
            self.path_illumFiles = path_illumFiles
            self.dict_illum = self._get_dict_illumFiles()

    def _get_dict_illumFiles(self):
        return {
            f"FileName_{self.illum_prefix}_{file.split('_')[-1][:-4]}": file
            for file in os.listdir(self.path_illumFiles)
            if file.endswith(".npy")
        }

    def _extract_metadata(self, filename):
        if filename.endswith(".tif") or filename.endswith(".tiff"):
            match = re.match(self.pattern, filename)
            if not match:
                print(f"Error: El formato no coincide con el regex: {filename}")
                return None

            dict_data = match.groupdict()
            dict_data["Filename"] = filename
            dict_data["Well"] = get_well(dict_data["Row"], dict_data["Column"])
            return {key: dict_data[key] for key in ["Filename", "Well", "Channel", "Field", "Plane"] if
                    key in dict_data}

    def _filter_metadata_dict(self, list_dict):
        grouped_data = {}
        if self.channel_prefix:
            channel_prefix = "Orig_"
        else:
            channel_prefix = ""
        for item in list_dict:
            key = (item["Well"], item["Field"], item["Plane"])
            channel_name = self.channels_dict.get(int(item["Channel"]), f"Unknown_{item['Channel']}")
            image_file_col = f"{self.image_prefix}_FileName_{channel_prefix}{channel_name}"
            image_path_col = f"{self.image_prefix}_PathName_{channel_prefix}{channel_name}"
            if self.with_illum:
                illum_file_col = f"FileName_{self.illum_prefix}_{channel_name}"
                illum_path_col = f"PathName_{self.illum_prefix}_{channel_name}"

            if key not in grouped_data:
                grouped_data[key] = {
                    f"{self.metadata_prefix}_Well": item["Well"],
                    f"{self.metadata_prefix}_Field": item["Field"],
                    f"{self.metadata_prefix}_Plane": item["Plane"]
                }

            grouped_data[key][image_file_col] = item["Filename"]
            grouped_data[key][image_path_col] = self.path_imagesFiles
            if self.with_illum:
                grouped_data[key][illum_file_col] = self.dict_illum.get(illum_file_col, "Missing")
                grouped_data[key][illum_path_col] = self.path_illumFiles

        return grouped_data

    def _gen_df_from_dict(self, dict_metadata_filt):
        df = pd.DataFrame.from_dict(dict_metadata_filt, orient='index').reset_index(drop=True)
        metadata_cols = [col for col in df.columns if col.startswith(self.metadata_prefix)]
        other_cols = sorted(col for col in df.columns if not col.startswith(self.metadata_prefix))

        df = df[other_cols + metadata_cols]
        file_path = os.path.join(self.path_savingCSV, self.name_CSV)
        df.to_csv(file_path, index=False)
        print(df.head())
        return df

    def process_metadata(self):
        images_metadata = list(filter(None, map(self._extract_metadata, self.images)))
        #print(f"Images metadata: {images_metadata}")
        images_metadata_filtered = self._filter_metadata_dict(images_metadata)
        #print(f"Filtered images: {images_metadata_filtered}")
        return self._gen_df_from_dict(images_metadata_filtered)