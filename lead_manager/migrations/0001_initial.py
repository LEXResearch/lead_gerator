# Generated by Django 2.0.5 on 2018-05-16 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeadGerated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('author', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('id_from_manancial', models.IntegerField()),
                ('type', models.CharField(choices=[('d', 'Dissertação'), ('t', 'Tese'), ('o', 'Outro')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='LeadModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='leadgerated',
            name='lead_model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lead_manager.LeadModel'),
        ),
    ]
