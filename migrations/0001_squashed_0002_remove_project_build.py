# Generated by Django 3.1.2 on 2021-02-04 12:08

from django.db import migrations, models
import django.utils.timezone
import portfolio.models
import uuid


class Migration(migrations.Migration):

    #replaces = [('portfolio', '0001_initial'), ('portfolio', '0002_remove_project_build')]

    initial = True

    dependencies = [
        #('bimblog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(editable=False, max_length=100, null=True)),
                ('title', models.CharField(blank=True, help_text='Titolo del progetto', max_length=50, null=True, verbose_name='Titolo')),
                ('intro', models.CharField(default=portfolio.models.project_default_intro, max_length=100, verbose_name='Introduzione')),
                ('body', models.TextField(null=True, verbose_name='Testo')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Data:')),
                ('last_updated', models.DateTimeField(editable=False, null=True)),
                ('site', models.CharField(blank=True, help_text='Qualcosa tipo "Roma - Monteverde"', max_length=100, null=True, verbose_name='Luogo')),
                ('category', models.CharField(choices=[('ALT', 'Altro'), ('RES', 'Residenziale'), ('TER', 'Terziario'), ('SAN', 'Sanitario'), ('PRO', 'Produttivo'), ('SCO', 'Scolastico')], default='ALT', max_length=4, verbose_name='Categoria funzionale')),
                ('type', models.CharField(choices=[('ALT', 'Altro'), ('ARR', 'Arredamento'), ('RIS', 'Ristrutturazione'), ('RES', 'Restauro'), ('AMP', 'Ampliamento'), ('COS', 'Costruzione'), ('DEM', 'Demolizione')], default='ALT', max_length=4, verbose_name='Tipo di intervento')),
                ('status', models.CharField(choices=[('ALT', 'Altro'), ('PRO', 'Progettato'), ('COR', 'In corso'), ('REA', 'Realizzato')], default='ALT', max_length=4, verbose_name="Status dell'intervento")),
                ('cost', models.CharField(choices=[('ALT', 'Altro'), ('1K', '1K'), ('10K', '10K'), ('100K', '100K'), ('1M', '1M'), ('10M', '10M')], default='ALT', max_length=4, verbose_name="Costo dell'intervento")),
            ],
            options={
                'verbose_name': 'Progetto',
                'verbose_name_plural': 'Progetti',
                'ordering': ('-date',),
            },
        ),
    ]
