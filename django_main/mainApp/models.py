# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AppMainDocument(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    docname = models.CharField(db_column='DocName', max_length=255)  # Field name made lowercase.
    doc = models.FileField(db_column='Doc',upload_to="files",max_length=100, blank=True, null=True)  # Field name made lowercase.
    doctype = models.CharField(db_column='DocType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pono = models.ForeignKey('AppMainPurchaseorder', models.DO_NOTHING,max_length=255, db_column='PONO_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'app_main_document'


class AppMainPurchaseorder(models.Model):
    pono = models.CharField(db_column='PONO', primary_key=True, max_length=255)  # Field name made lowercase.
    shipdate = models.DateField(db_column='ShipDate')  # Field name made lowercase.
    customer = models.CharField(db_column='Customer', max_length=255)  # Field name made lowercase.
    iasubmissiondate = models.DateField(db_column='IaSubmissionDate', blank=True, null=True)  # Field name made lowercase.
    inspectiondate = models.DateField(db_column='InspectionDate', blank=True, null=True)  # Field name made lowercase.
    vendorno = models.ForeignKey('AppMainVendor', models.DO_NOTHING, db_column='VendorNo_id')  # Field name made lowercase.
    alerts = models.CharField(db_column='Alerts', blank=True, null=True)  # Field name made lowercase.
    inspectiondateproposed = models.DateField(db_column='InspectionDateProposed', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'app_main_purchaseorder'


class AppMainVendor(models.Model):
    vendorno = models.CharField(db_column='VendorNo', primary_key=True, max_length=255)  # Field name made lowercase.
    vendorname = models.CharField(db_column='VendorName', max_length=500)  # Field name made lowercase.
    territory = models.CharField(db_column='Territory', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iaalertdays = models.IntegerField(db_column='IaAlertDays', blank=True, null=True)  # Field name made lowercase.
    email2 = models.CharField(db_column='Email2', max_length=254, blank=True, null=True)  # Field name made lowercase.
    email3 = models.CharField(db_column='Email3', max_length=254, blank=True, null=True)  # Field name made lowercase.
    email4 = models.CharField(db_column='Email4', max_length=254, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=254)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'app_main_vendor'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
