# Autor: Stefan Grujičić 0030/2023
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_kategorijaclanka_clanak_slikaclanka'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponzorskaPonuda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vrednost', models.PositiveIntegerField(db_column='Vrednost', verbose_name='Vrednost (EUR)')),
                ('opis', models.TextField(db_column='Opis', max_length=1024, verbose_name='Opis doprinosa')),
                ('status', models.CharField(
                    choices=[('na_cekanju', 'Na čekanju'), ('prihvacena', 'Prihvaćena'), ('odbijena', 'Odbijena')],
                    db_column='Status',
                    default='na_cekanju',
                    max_length=20,
                    verbose_name='Status',
                )),
                ('datum_slanja', models.DateField(auto_now_add=True, db_column='DatumSlanja', verbose_name='Datum slanja')),
                ('akcija', models.ForeignKey(
                    db_column='IdAkc',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sponzorske_ponude',
                    to='main.akcija',
                    verbose_name='Akcija',
                )),
                ('sponzor', models.ForeignKey(
                    db_column='IdKor',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='ponude',
                    to='main.sponzorprofil',
                    verbose_name='Sponzor',
                )),
            ],
            options={
                'verbose_name': 'Sponzorska ponuda',
                'verbose_name_plural': 'Sponzorske ponude',
                'db_table': 'SponzorskaPonuda',
                'ordering': ['-datum_slanja'],
            },
        ),
    ]
