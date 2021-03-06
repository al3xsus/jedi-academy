# Generated by Django 2.1.7 on 2019-03-31 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jedi_academy_app', '0003_auto_20190331_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer1', models.BooleanField()),
                ('answer2', models.BooleanField()),
                ('answer3', models.BooleanField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedi_academy_app.Candidate')),
                ('trial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedi_academy_app.Trial')),
            ],
            options={
                'db_table': 'answers',
            },
        ),
    ]
