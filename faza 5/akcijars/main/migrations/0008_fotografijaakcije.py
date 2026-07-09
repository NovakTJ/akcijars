# SSU 10 — model FotografijaAkcije (slike pre/posle akcije).

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_akcija_geo'),
    ]

    operations = [
        migrations.CreateModel(
            name='FotografijaAkcije',
            fields=[
                ('id_fot', models.AutoField(db_column='IdFot', primary_key=True, serialize=False)),
                ('slika', models.ImageField(db_column='Putanja', upload_to='akcije/', verbose_name='Fotografija')),
                ('tip', models.CharField(choices=[('pre', 'Pre akcije'), ('posle', 'Posle akcije')], db_column='Tip', default='pre', max_length=10, verbose_name='Tip (pre/posle)')),
                ('akcija', models.ForeignKey(db_column='IdAkc', on_delete=django.db.models.deletion.CASCADE, related_name='fotografije', to='main.akcija', verbose_name='Akcija')),
            ],
            options={
                'verbose_name': 'Fotografija akcije',
                'verbose_name_plural': 'Fotografije akcija',
                'db_table': 'FotografijaAkcije',
            },
        ),
    ]
