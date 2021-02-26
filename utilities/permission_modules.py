# from django.apps import apps
# from user.models import User
# from address.models import Division, District, Upazila, Union, Village, PostOffice
# from institute.models import Institute
# from utilities.variables import ADMIN, MASTER_ADMIN
#
# MASTER_GROUP_PERMISSIONS = {
#     MASTER_ADMIN: {
#         AcademicYear: ['add', 'change', 'delete', 'view'],
#         AcademicSession: ['add', 'change', 'delete', 'view'],
#         Institute: ['add', 'change', 'delete', 'view'],
#         Division: ['add', 'change', 'delete', 'view'],
#         District: ['add', 'change', 'delete', 'view'],
#         Upazila: ['add', 'change', 'delete', 'view'],
#         Union: ['add', 'change', 'delete', 'view'],
#         Village: ['add', 'change', 'delete', 'view'],
#         PostOffice: ['add', 'change', 'delete', 'view'],
#         User: ['add', 'change', 'view'],
#     },
# }
#
# institute_admin_modules = [
#     'academic', 'hr', 'student', 'institute', 'accounts', 'attendance', 'exam', 'payroll',
#     'student_account', 'general_account'
# ]
# hr_models = apps.all_models
#
# ADMIN_GROUP_PERMISSIONS = {
#     ADMIN: {},
# }
# module_dic = {}
# for app_label in institute_admin_modules:
#     all_models = apps.all_models[app_label]
#     for model_name in all_models:
#         module_dic[all_models[model_name]] = ['add', 'change', 'view']
# ADMIN_GROUP_PERMISSIONS[ADMIN] = module_dic
