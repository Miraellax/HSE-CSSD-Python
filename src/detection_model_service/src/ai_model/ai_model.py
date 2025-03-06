from fastapi import UploadFile


async def process(image: UploadFile) -> list[dict]:
    results = [
        {
            "class": "sphere",
             "x": 0.5,
             "y": 0.5,
             "width": 0.2,
             "height": 0.1,
             "rotation": 30
        }
    ]
    print(results)

    return results
