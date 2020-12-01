# Generated by Django 2.2 on 2020-11-28 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('website', models.CharField(max_length=255)),
                ('note', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_person', models.CharField(max_length=50)),
                ('note', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_person', to='jobHuntBuddyApp.Company')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_applied', models.DateField(null=True)),
                ('position_applied_for', models.CharField(max_length=50)),
                ('date_declined', models.DateField(null=True)),
                ('note', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='jobHuntBuddyApp.Company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='jobHuntBuddyApp.User')),
            ],
        ),
        migrations.CreateModel(
            name='FollowUpDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_heard_back', models.DateField(null=True)),
                ('note', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contact_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_up_date', to='jobHuntBuddyApp.ContactPerson')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_up_date', to='jobHuntBuddyApp.Position')),
            ],
        ),
        migrations.AddField(
            model_name='contactperson',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_person', to='jobHuntBuddyApp.Position'),
        ),
    ]
