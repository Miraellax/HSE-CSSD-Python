async def process(image: bytes) -> list[dict]:
    # mock results for now, class is class id
    results = [
        {
            "class_id": 1,
             "x_coord": 0.5,
             "y_coord": 0.5,
             "width": 0.2,
             "height": 0.1,
             "rotation": 0.2,
             "probability": 0.82
        }
    ]

    return results
