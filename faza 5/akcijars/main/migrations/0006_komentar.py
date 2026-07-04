import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_sponzorska_ponuda'),
    ]

    operations = [
        migrations.CreateModel(
            name='Komentar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tekst', models.TextField(db_column='Tekst', verbose_name='Tekst')),
                ('datum_komentara', models.DateTimeField(
                    auto_now_add=True,
                    db_column='DatumKomentara',
                    verbose_name='Datum komentara',
                )),
                ('clanak', models.ForeignKey(
                    db_column='IdCla',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='komentari',
                    to='main.clanak',
                    verbose_name='Članak',
                )),
                ('korisnik', models.ForeignKey(
                    db_column='IdKor',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='komentari',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Korisnik',
                )),
            ],
            options={
                'verbose_name': 'Komentar',
                'verbose_name_plural': 'Komentari',
                'db_table': 'Komentar',
                'ordering': ['-datum_komentara'],
            },
        ),
    ]
