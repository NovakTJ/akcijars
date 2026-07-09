from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_komentar'),
    ]

    operations = [
        migrations.AddField(
            model_name='akcija',
            name='geo_sirina',
            field=models.FloatField(
                blank=True,
                db_column='GeoSirina',
                null=True,
                verbose_name='Geografska širina',
            ),
        ),
        migrations.AddField(
            model_name='akcija',
            name='geo_duzina',
            field=models.FloatField(
                blank=True,
                db_column='GeoDuzina',
                null=True,
                verbose_name='Geografska dužina',
            ),
        ),
    ]
