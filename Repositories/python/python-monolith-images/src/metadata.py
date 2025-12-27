from src.data_load_module import metadata_index


def get_image_metadata(image_ids):
    return [
        {
            "id": metadata_index[i]["id"],
            "name": metadata_index[i]["name"],
            "tags": metadata_index[i]["tags"],
        }
        for i in image_ids
        if i in metadata_index
    ]
