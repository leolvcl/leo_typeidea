from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_header = 'leo_Typeidea'
    site_title = 'leo_Typeidea管理后台'
    index_title = '首页'

custom_site = CustomSite(name='cus_admin')



