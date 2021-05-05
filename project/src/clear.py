import json
from src.helper import create_timestamp

def clear_v1():
    with open("src/data.json", 'w') as FILE:
        data = {
            "users": [

            ],
            "channels": [

            ],
            "dms": [

            ],
            "messages": [

            ],
            "notifications": [
                
            ],
            "user_stats": [

            ],
            "dreams_stats": {
                "channels_exist": [
                    {
                        "num_channels_exist": 0, 
                        "time_stamp": create_timestamp()
                    }
                ], 
                "dms_exist": [
                    {
                        "num_dms_exist": 0, 
                        "time_stamp": create_timestamp()
                    }
                ], 
                "messages_exist": [
                    {
                        "num_messages_exist": 0,
                        "time_stamp": create_timestamp()
                    }
                ], 
                "utilization_rate": 0.0
            },
            "standups": [

            ],
            "reset_codes": [
                
            ]
        }
        json.dump(data, FILE, indent = 4)

    return {}
