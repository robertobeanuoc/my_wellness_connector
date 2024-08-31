import re

BASE_URL: str = "https://www.mywellness.com"
TOKEN_URL: str = f"{BASE_URL}/cloud/User/Login/"
TRAINING_URL: str = f"{BASE_URL}/cloud/Training/"
DATE_RANGE_URL: str = f"{BASE_URL}/cloud/Training/LastPerformedWorkoutSession"
EXERCISE_DETAIL_URL: str = f"{BASE_URL}/cloud/Training/PerformedExerciseDetail"
REGULAR_EXPRESSION_ACTIVITY_ID: re.Pattern = (
    r"performedPhysicalActivityId=([0-9A-Z-a-z-]+)"
)
REGULAR_EXPRESION_TOKEN: re.Pattern = r"\\\"token\\\":\\\"([A-Za-z0-9._-]+)\\\""
REGULAR_EXPRESION_ID: re.Pattern = r"\\\"id\\\":\\\"([A-Za-z0-9._-]+)\\\""
REGULAR_EXPRESION_ID_CR: re.Pattern = r'id="([0-9]+)"'
REGULAR_EXPRESION_DATE: re.Pattern = r"20\d{6}"
REGULAR_EXPRESION_TRAINING: re.Pattern = (
    r"https:\/\/[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\/[^\s]*"
)
REGULAR_EXPRESSION_DATA_POSITION: re.Pattern = r"data\-position=\"([0-9]+)\""
CELL_DATE_ATTRIBUTE: str = "cell_date"
IDCR_ATTRIBUTE: str = "sesion_idcr"
HREF_ATTRIBUTE: str = "href"
DATA_POSITION_ATTRIBUTE: str = "data_position"
MACHINE_TYPE_ATTRIBUTE: str = "machine_type"
ACTIVITY_ID_ATTRIBUTE: str = "activity_id"

VERTICAL_DATA: str = "vertical"
