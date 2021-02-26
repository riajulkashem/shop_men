# USER ROLE
ADMIN: str = 'admin'
ACCOUNTANT: str = 'accountant'
OPERATOR: str = 'operator'
TEACHER: str = 'teacher'
STUDENT: str = 'student'
GUARDIAN: str = 'guardian'
GROUP_ADMIN: str = 'group_admin'
MASTER_ADMIN: str = 'master_admin'
UPAZILA_ADMIN: str = 'upazila_admin'
UNION_ADMIN: str = 'union_admin'
VILLAGE_ADMIN: str = 'village_admin'
DISTRICT_ADMIN: str = 'district_admin'
DIVISION_ADMIN: str = 'division_admin'
SUPER_ADMIN: str = 'superuser'

AUTHORISED_STAFF = [
    TEACHER, ACCOUNTANT, OPERATOR
]
ALL_USER_ROLES = [
    SUPER_ADMIN,
    MASTER_ADMIN,
    ADMIN,
    ACCOUNTANT,
    OPERATOR,
    TEACHER,
    STUDENT,
    GUARDIAN,
    GROUP_ADMIN,
    DIVISION_ADMIN,
    DISTRICT_ADMIN,
    UPAZILA_ADMIN,
    UNION_ADMIN,
]

# CHOICES
GENDER_CHOICES = (
    ('male', "Male"),
    ('female', "Female"),
    ('others', "Others"),
)
MARITAL_STATUS_CHOICES = (
    ('married', "MARRIED"),
    ('unmarried', "UNMARRIED"),
    ('divorced', "DIVORCED"),
    ('widow', "WIDOW"),
)

RELIGION_CHOICES = (
    ('islam', "Islam"),
    ('christianity', "Christianity"),
    ('hinduism', "Hinduism"),
    ('buddhism', "Buddhism"),
    ('others', "Others"),
)

SUBJECT_TYPE = (
    ('practical', 'PRACTICAL'),
    ('theory', 'THEORY'),
    ('optional', 'OPTIONAL'),
    # optional subjects gula 4th subject hisebe show korbe
    ('group based', 'GROUP BASED'),
    ('uncountable', 'UNCOUNTABLE'),
    # mark thakbe but exam and result e count kora hobe na
)
