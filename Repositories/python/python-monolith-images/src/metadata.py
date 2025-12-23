from src.data_load_module import metadata_index


def get_image_metadata(image_ids):
    return [
        metadata_index[i]
        for i in image_ids
        if i in metadata_index
    ]
